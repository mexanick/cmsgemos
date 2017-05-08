import sys, os, time, signal, random
sys.path.append('${GEM_PYTHON_PATH}')
sys.path.append('${XHAL_PYTHON_PATH}')

from ctypes import *
from rw_reg import *

from gemlogger import GEMLogger
gemlogger = GEMLogger("registers_uhal").gemlogger

gMAX_RETRIES = 5
gRetries = 5

class colors:
    WHITE   = '\033[97m'
    CYAN    = '\033[96m'
    MAGENTA = '\033[95m'
    BLUE    = '\033[94m'
    YELLOW  = '\033[93m'
    GREEN   = '\033[92m'
    RED     = '\033[91m'
    ENDC    = '\033[0m'


def readRegister(device, register, debug=False):
    """
    read register 'register' using remote procedure call
    returns value of the register
    """
    global gRetries
    nRetries = 0
    m_node = getNode(register)
    if m_node is None:
        print colors.MAGENTA,"NODE %s NOT FOUND" %(register),colors.ENDC
        return 0x0
    elif 'r' not in m_node.permission:
        print colors.MAGENTA,"No read permission for register %s" %(register),colors.ENDC
        return 0x0
    if debug:
        print "Trying to read\n"
        print m_node.output()
        pass
    while (nRetries<gRetries):
        res = rReg(parseInt(m_node.real_address))
        if res == 0xdeaddead:
            print colors.MAGENTA,"Bus error encountered while reading (%s), retrying operation (%d,%d)"%(register,nRetries,gRetries),colors.ENDC
            continue
            #return 0xdeaddead
        else:
            if m_node.mask is not None:
                shift_amount=0
                for bit in reversed('{0:b}'.format(m_node.mask)):
                    if bit=='0': shift_amount+=1
                    else: break
                fin_res = (res&m_node.mask)>>shift_amount
            else:
                fin_res = res
            if debug: print "Read register result: %s" %(fin_res)
            return fin_res
    return 0xdeaddead

def readRegisterList(device, registers, debug=False):
    """
    read registers 'registers' using remote procedure call
    returns values of the registers in a dict
    """
    global gRetries
    nRetries = 0
    if debug:
        print registers
        pass
    addresses = []
    masks = []
    for reg in registers:
      m_node = getNode(reg)
      if m_node is None:
          print colors.MAGENTA,"NODE NOT FOUND",colors.ENDC
          return 0x0
      addresses.append(m_node.real_address)
      masks.append(m_node.mask)
 
    c_addr = (c_uint32 * len(addresses))(*addresses)
    p = (c_uint32 * len(addresses))()
    words = []
    while (nRetries < gMAX_RETRIES):
    	if (debug):
    	    print "reading register list %s"%(registers)
    	    pass
        res = rList(c_addr,p,len(p))
        if (res == 0):
            words = apply_masks(list(p),masks)
            results = {}
            for i,reg in enumerate(registers):
                results[reg] = words[i]
                pass
            return results
        else:
            print colors.RED, "error encountered, retried read operation (%d)"%(nRetries),colors.ENDC
            nRetries += 1
    return 0x0

def readBlock(device, register, nwords, debug=False):
    """
    read block 'register' from uhal device 'device'
    returns 'nwords' values in the register
    """
    global gRetries
    nRetries = 0
    m_node = getNode(register)
    if m_node is None:
        print colors.MAGENTA,"NODE %s NOT FOUND" %(register),colors.ENDC
        return 0x0

    #if debug:
    #    print "Trying to read block of %d words\n" %(nwords)
    #    print m_node.output()
 
    p = (c_uint32*nwords)()
    words = []
    #while (nRetries < gMAX_RETRIES):
    if (debug):
        print "reading %d words from register %s"%(nwords,register)
        pass
    #for i in range(nwords):
    #   words.append(readRegister(device,register, False))
    #if (debug):
    #    print "reading result: %s" %(words)
    #    pass
    res = rBlock(m_node.real_address,p,len(p))
    if (res == 0):
        words = list(p)
        if (debug):
            print "ReadBlock result:\n"
            print words
            pass
        return words
    else:
        print colors.RED, "error encountered, retried read operation (%d)"%(nRetries),colors.ENDC
        nRetries += 1
    return words

def writeRegister(device, register, value, debug=False):
    """
    write value 'value' into register 'register' using remote procedure call
    """
    global gRetries
    nRetries = 0
    m_node = getNode(register)
    if m_node is None:
        print colors.MAGENTA,"NODE %s NOT FOUND"%(register),colors.ENDC
        return 0x0

    if debug:
        print "Trying to write\n"
        print m_node.output()
        pass
 
    while (nRetries < gMAX_RETRIES):
        rsp = writeReg(m_node, value)
        if "permission" in rsp:
            print colors.MAGENTA,"NO WRITE PERMISSION",colors.ENDC
            return
        elif "Error" in rsp:
            print colors.MAGENTA,"write error encountered (%s), retrying operation (%d,%d)"%(register,nRetries,gRetries),colors.ENDC
            return
        elif "0xdeaddead" in rsp:
            print colors.MAGENTA,"0xdeaddead found (%s), retrying operation (%d,%d)"%(register,nRetries,gRetries),colors.ENDC
            return
        else: 
            return 
        pass
    pass

def writeRegisterList(device, regs_with_vals, debug=False):
    """
    write value 'value' into register 'register' using remote procedure call
    from an input dict
    """
    global gRetries
    nRetries = 0
    while (nRetries < gMAX_RETRIES):
        for reg in regs_with_vals.keys():
            writeRegister(device,reg, regs_with_vals[reg],debug)
            pass
        return
    pass

def apply_masks(values, masks):
    f_vals = []
    for val, mask in zip(values,masks):
        if mask is not None:
            shift_amount=0
            for bit in reversed('{0:b}'.format(mask)):
                if bit=='0': shift_amount+=1
                else: break
            f_vals.append((val&mask)>>shift_amount)
        else: f_vals.append(val)
    return f_vals

