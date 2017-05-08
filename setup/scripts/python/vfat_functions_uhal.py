import sys, os, time, signal, random

import uhal
from registers_uhal import *
from optohybrid_user_functions_uhal import *
from gemlogger import GEMLogger

gemlogger = GEMLogger("vfat_functions_uhal").gemlogger

def readVFAT(device, gtx, chip, reg, debug=False):
    baseNode = "GEM_AMC.OH.OH%d.GEB.VFATS.VFAT%d"%(gtx,chip)
    vfatVal = readRegister(device,"%s.%s"%(baseNode,reg))
    # do check on status
    if ((vfatVal >> 26) & 0x1) :
        msg = "error on VFAT transaction (chip %d, %s)"%(chip, reg)
        gemlogger.debug(msg)
        return -1
    elif ((vfatVal >> 25) & 0x0):
        msg = "invalid VFAT transaction (chip %d, %s)"%(chip, reg)
        gemlogger.debug(msg)
        return -1
    elif ((vfatVal >> 24) & 0x0):
        msg = "wrong type of VFAT transaction (chip %d, %s)"%(chip, reg)
        gemlogger.debug(msg)
        return -1
    else :
        return vfatVal

def readAllVFATs(device, gtx, reg, mask=0x0, debug=False):
    vfatVals = broadcastRead(device,gtx,reg,mask,debug)
    if (debug and vfatVals):
        for i,val in enumerate(vfatVals):
            print "%d: value = 0x%08x"%(i,val)
            pass
        pass
    ## do check on status, maybe only do the check in the calling code
    #if ((vfatVals >> 26) & 0x1) :
    #    msg = "error on block VFAT transaction (%s)"%(reg)
    #    gemlogger.debug(msg)
    #    return -1
    #elif ((vfatVals >> 25) & 0x0):
    #    msg = "invalid block VFAT transaction (%s)"%(reg)
    #    gemlogger.debug(msg)
    #    return -1
    #elif ((vfatVals >> 24) & 0x0):
    #    msg = "wrong type of block VFAT transaction (%s)"%(reg)
    #    gemlogger.debug(msg)
    #    return -1
    #else :
    #    return vfatVals
    return vfatVals

def writeVFAT(device, gtx, chip, reg, value, debug=False):
    baseNode = "GEM_AMC.OH.OH%d.GEB.VFATS.VFAT%d"%(gtx,chip)
    writeRegister(device,"%s.%s"%(baseNode,reg), value)

def writeVFATRegisters(device, gtx, chip, regs_with_values, debug=False):
    baseNode = "GEM_AMC.OH.OH%d.GEB.VFATS.VFAT%d"%(gtx,chip)
    registers = {}
    for reg in regs_with_values.keys():
        registers["%s.%s"%(baseNode,reg)] = regs_with_values[reg]
        pass
    writeRegisterList(device,registers)

def readVFATRegisters(device, gtx, chip, regs, debug=False):
    baseNode = "GEM_AMC.OH.OH%d.GEB.VFATS.VFAT%d"%(gtx,chip)
    registers = []
    for reg in regs:
        registers.append("%s.%s"%(baseNode,reg))
        pass
    return readRegisterList(device,registers)

def writeAllVFATs(device, gtx, reg, value, mask=0x0, debug=False):
    broadcastWrite(device,gtx,reg,value,mask,debug)

def setupDefaultCRs(device, gtx, chip, sleep=False, debug=False):
    registers = {
        "ContReg1": 0x00,
        "ContReg2": 0x30,
        "ContReg3": 0x00
        }
    if not sleep:
        registers["ContReg0"]= 0x36
    else:
        registers["ContReg0"]= 0x37
        pass
    writeVFATRegisters(device, gtx, chip, registers)
    return

def setRunMode(device, gtx, chip, enable, debug=False):
    regVal = readVFAT(device, gtx, chip, "ContReg0")
    if (regVal < 0):
        return
    if (enable):
        writeVFAT(device, gtx, chip, "ContReg0", regVal|0x01)
    else:
        writeVFAT(device, gtx, chip, "ContReg0", regVal&0xFE)
        pass
    return

def setChannelRegister(device, gtx, chip, chan,
                       mask=0x0, pulse=0x0, trim=0x0, debug=False):
    if (chan not in range(0,128)):
        print "Invalid VFAT channel specified %d"%(chan)
        return
    chanReg = ((pulse&0x1) << 6)|((mask&0x1) << 5)|(trim&0x1f)
    writeVFAT(device, gtx, chip, "VFATChannels.ChanReg%d"%(chan+1),chanReg)
    return

def getChannelRegister(device, gtx, chip, chan, debug=False):
    if (chan not in range(0,128)):
        print "Invalid VFAT channel specified %d"%(chan)
        return
    return readVFAT(device, gtx, chip, "VFATChannels.ChanReg%d"%(chan+1))

def setVFATThreshold(device, gtx, chip, vt1, vt2=0, debug=False):
    writeVFATRegisters(device, gtx, chip,
                       {"VThreshold1": vt1,
                        "VThreshold2": vt2
                        })
    return

def getVFATThreshold(device, gtx, chip, vt1, vt2=0, debug=False):
    thresholds = readVFATRegisters(device, gtx, chip, ["VThreshold1","VThreshold2"])
    vt1 = 0
    vt2 = 0
    for reg in thresholds.keys():
        if (reg.find("VThreshold1") > 0):
            vt1 = thresholds[reg]
        elif (reg.find("VThreshold2") > 0):
            vt2 = thresholds[reg]
            pass
        pass
    return vt2-v21

def biasVFAT(device, gtx, chip, enable=True, debug=False):
    registers = {
        "ContReg1":    0x00,
        "ContReg2":    0x30,
        "ContReg3":    0x00,
        # "Latency":      156,
        # "IPreampIn":    168,
        # "IPreampFeed":   80,
        # "IPreampOut":   150,
        # "IShaper":      150,
        # "IShaperFeed":  100,
        # "IComp":         90,
        # "VCal":           0,
        # # "VThreshold1":   25,
        # "VThreshold2": 0x00,
        # "CalPhase":    0x00
        }
    if (enable):
        registers["ContReg0"] = 0x37
    else:
        #what about leaving any other settings?
        #not now, want a reproducible routine
        registers["ContReg0"] = 0x36
        pass

    for chan in range(128):
        #writeRegister(device,"%s.VFATChannels.ChanReg%d"%(baseNode,chan+1),0x40)
        #mask no channels, as this seems to affect the output data packets, not just the triggers
        # disable cal pulses to all channels
        registers["VFATChannels.ChanReg%d"%(chan+1)] = 0x00
        pass
    writeVFATRegisters(device,gtx,chip,registers)
    return

def biasAllVFATs(device, gtx, mask=0x0, enable=True, debug=False):
    if (enable):
        writeAllVFATs(device, gtx, "ContReg0",    0x37, mask=mask)
    else:
        #what about leaving any other settings?
        #not now, want a reproducible routine
        writeAllVFATs(device, gtx, "ContReg0",    0x36, mask=mask)
        pass
    writeAllVFATs(device, gtx, "ContReg1",    0x00, mask=mask)
    writeAllVFATs(device, gtx, "ContReg2",    0x30, mask=mask)
    writeAllVFATs(device, gtx, "ContReg3",    0x00, mask=mask)
    writeAllVFATs(device, gtx, "Latency",      156, mask=mask)
    writeAllVFATs(device, gtx, "IPreampIn",    168, mask=mask)
    writeAllVFATs(device, gtx, "IPreampFeed",   80, mask=mask)
    writeAllVFATs(device, gtx, "IPreampOut",   150, mask=mask)
    writeAllVFATs(device, gtx, "IShaper",      150, mask=mask)
    writeAllVFATs(device, gtx, "IShaperFeed",  100, mask=mask)
    writeAllVFATs(device, gtx, "IComp",         90, mask=mask)
    writeAllVFATs(device, gtx, "VCal",           0, mask=mask)
    # writeAllVFATs(device, gtx, "VThreshold1",   25, mask=mask)
    writeAllVFATs(device, gtx, "VThreshold2", 0x00, mask=mask)
    writeAllVFATs(device, gtx, "CalPhase",    0x00, mask=mask)

    if debug:
        print "biased VFATs, zeroing channel registers"
    for chan in range(128):
        #writeRegister(device,"%s.VFATChannels.ChanReg%d"%(baseNode,chan+1),0x40)
        #mask no channels, as this seems to affect the output data packets, not just the triggers
        # disable cal pulses to all channels
        writeAllVFATs(device, gtx, "VFATChannels.ChanReg%d"%(chan),0x00, mask=mask,debug=debug)
    return

def getChipID(device, gtx, chip, debug=False):
    thechipid = 0x0000
    #baseNode = "GEM_AMC.OH.OH%d.GEB.VFATS.VFAT%d"%(chip)
    emptyMask = 0xffff
    ebmask = 0x000000ff
    thechipid  = readVFAT(device, gtx, chip, "ChipID1")
    if (thechipid < 0):
        thechipid = 0xdead
    elif (((thechipid>>16)&emptyMask) != ((0x050<<4)+(chip))):
        thechipid  = (thechipid & ebmask)<<8
        thechipid |= (readVFAT(device, gtx, chip, "ChipID0") & ebmask)
    else:
        thechipid = 0xdead
        pass

    return thechipid

def getAllChipIDs(device, gtx, mask=0xff000000, debug=False):
    """Returns a map of slot number to chip ID, for chips enabled in the mask
    Currently does not only return the unmasked values, but all values
    To be fixed in a future version"""
    chipID0s = readAllVFATs(device, gtx, "ChipID0", mask, debug)
    chipID1s = readAllVFATs(device, gtx, "ChipID1", mask, debug)
    ##make unknown chips report 0xdead
    return dict(map(lambda slotID: (slotID, (((chipID1s[slotID])&0xff)<<8)|(chipID0s[slotID]&0xff)
                                    #if (((chipID1s[slotID]>>16)&0xffff) != ((0x050<<4)+(slotID))) else 0xdead),
                                    if (((chipID1s[slotID]>>16)&0xffff) == 0x0000) else 0xdead),
                    range(0,24)))

def displayChipInfo(device, gtx, regkeys, mask=0xff000000, debug=False):
    """Takes as an argument a map of slot number to chip IDs and prints
    out all the information for the selected chips, would like for 0xdead
    chips to be red, but don't have time to really do this now """
    slotbase = "GEB%d SlotID::"%(gtx)
    base     = "     ChipID::"
    perslot  = "%3d"
    perchip  = "0x%04x"
    perreg   = "0x%02x"
    registerList = [
	"ContReg0","ContReg1","ContReg2","ContReg3",
	"Latency",
	"IPreampIn","IPreampFeed","IPreampOut",
	"IShaper","IShaperFeed",
	"IComp",
	"VCal",
	"VThreshold1",
	"VThreshold2",
	"CalPhase",
        ]

    slotmap = map(lambda slotID: perslot%(slotID), regkeys.keys())
    msg = "%s   %s%s%s"%(slotbase,colors.GREEN,'    '.join(map(str, slotmap)),colors.ENDC)
    gemlogger.info(msg)
    chipmap = map(lambda chipID: perchip%(regkeys[chipID]), regkeys.keys())
    msg = "%s%s%s%s"%(base,colors.CYAN,' '.join(map(str, chipmap)),colors.ENDC)
    gemlogger.info(msg)
    for reg in registerList:
        #regmap = map(lambda chip: perreg%(readVFAT(device, gtx, chip,reg)&0xff), regkeys.keys())
        regValues = readAllVFATs(device, gtx, reg, mask, debug)
        regmap = map(lambda chip: perreg%(chip&0xff), regValues)
        msg = "%11s::  %s"%(reg, '   '.join(map(str, regmap)))
        gemlogger.info(msg)
        pass
    return
