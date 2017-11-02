import os, signal, sys, time
sys.path.append('${GEM_PYTHON_PATH}')

from gempython.tools.amc_user_functions_xhal import *
from gempython.utils.gemlogger import colormsg
from gempython.utils.nesteddict import nesteddict

import logging

#class scanmode:
#    THRESHTRG = 0 # Threshold scan
#    THRESHCH  = 1 # Threshold scan per channel
#    LATENCY   = 2 # Latency scan
#    SCURVE    = 3 # s-curve scan
#    THRESHTRK = 4 # Threshold scan with tracking data
#    pass

class HwOptoHybrid:
    def __init__(self, slot, link, shelf=1, debug=False):
        """
        Initialize the HW board an open an RPC connection
        """
        # Debug flag
        self.debug = debug
        
        # Logger
        self.ohlogger = logging.getLogger(__name__)

        # Store HW info
        self.link = link
        self.nVFATs = 24
        self.parentAMC = HwAMC(slot, shelf, debug)

        # Define broadcast read
        self.bRead = self.parentAMC.lib.broadcastRead
        self.bRead.argtypes = [c_uint, c_char_p, c_uint, POINTER(c_uint32)]
        self.bRead.restype = c_uint

        # Define broadcast write
        self.bWrite = self.parentAMC.lib.broadcastWrite
        self.bWrite.argtypes = [c_uint, c_char_p, c_uint, c_uint]
        self.bWrite.restype = c_uint
       
        # Define the scan module
        self.genScan = self.parentAMC.lib.genScan
        self.genScan.restype = c_uint
        self.genScan.argtypes = [c_uint, c_uint, c_uint, c_uint, 
                                 c_uint, c_uint, c_uint, c_uint, 
                                 c_char_p, c_bool, POINTER(c_uint32)]

        self.KnownV2bElScanRegs = [
                    "Latency",
                    "VCal",
                    "VThreshold1",
                    "VThreshold1PerChan",
                    "VThreshold1Trk"
                ]

        return

    def broadcastRead(self,register,mask=0xff000000):
        """
        Perform a broadcast RPC read on the VFATs specified by mask
        Will return when operation has completed
        """
        outData = (c_uint32 * self.nVFATs)()

        try:
            if 0 != self.bRead(self.link, register, mask, outData):
                print("broadcastRead failed for device %i; reg: %s; with mask %x"%(self.link,register,mask))
                sys.exit(os.EX_SOFTWARE)
        except Exception as e:
            print e

        return outData
    
    def broadcastWrite(self,register,value,mask=0xff000000):
        """
        Perform a broadcast RPC write on the VFATs specified by mask
        Will return when operation has completed
        """
        
        rpcResp = 0

        try:
            rpcResp = self.bWrite(self.link, register, value, mask)

            if 0 != rpcResp:
                print("broadcastWrite failed for device %i; reg: %s; with mask %x"%(self.link,register,mask))
                sys.exit(os.EX_SOFTWARE)
        except Exception as e:
            print e

        return rpcResp

    def performCalibrationScan(ohN, chan, scanReg, outData, enableCal=1, nevts=1000, dacMin=0, dacMax=254, stepSize=1, mask=0x0, useUltra=True):
        """
        Performs either a v2b ultra scan or a v3 generic scan

        ohN         - Optohybrid number (e.g. link)
        chan        - VFAT channel to be scanned
        scanReg     - Name of register to be scanned.  For v3
                      electronics consult the address table.
                      For v2b electronics see self.KnownV2bElScanRegs
        outData     - Array of type c_uint32, array size must be:
                      ((dacMax - dacMin + 1) / stepSize) * 24.
                      The first ((dacMax - dacMin + 1) / stepSize)
                      array positions are for VFAT0, the next
                      ((dacMax - dacMin + 1) / stepSize) are for VFAT1,
                      etc...  If a VFAT is masked entries in the array
                      are still allocated but assigned a 0 value.
        enableCal   - V3 electronics only. Enable cal pulse
        nevts       - Number of events for each dac value in scan
        dacMin      - Starting dac value of the scan
        dacMax      - Ending dac value of the scan
        stepSize    - Step size for moving from dacMin to dacMax
        mask        - VFAT mask to use
        useUltra    - V2b electronics only, perform an ultra scan 
                      instead of a FW scan.  Note if false the VFAT
                      to be scanned is taken as the first non-masked
                      VFAT defined in mask
        """

        if self.parentAMC.fwVersion < 3:
            if scanReg not in self.KnownV2bElScanRegs:
                print("Parent AMC Major FW Version: %i"%(self.parentAMC.fwVersion))
                print("V2b Electronics Behavior Detected")
                print("scanReg %s Not Known")
                print("Available scanReg values are:", self.KnownV2bElScanRegs)
                sys.exit(os.EX_USAGE)
        else:
            if "CFG_" in scanReg:
                scanReg = str.replace("CFG_","")

        return self.genScan(nevts, ohN, dacMin, dacMax, stepSize, chan, enableCal, mask, scanReg, useUltra, outData)

    def setDebug(self, debug):
        self.debug = debug
        return
