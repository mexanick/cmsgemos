import sys, os, time, signal, random
sys.path.append('${GEM_PYTHON_PATH}')
sys.path.append('${XHAL_PYTHON_PATH}')

from rw_reg.py import *

from gemlogger import GEMLogger
gemlogger = GEMLogger("registers_uhal").gemlogger

gMAX_RETRIES = 5
gRetries = 0

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
        print colors.MAGENTA,"NODE NOT FOUND",colors.ENDC
        return 0x0
    if debug:
        print """Trying to read register %s (%s)\n
              address 0x%08x  mask 0x%08x  permission %s  \n
              """%(register,
                 m_node.name,
                 m_node.real_address,
                 m_node.mask,
                 m_node.permission
                 )
        pass
    while (nRetries < gMAX_RETRIES):
	reg_val_s = readReg(m_node)
        if reg_val_s == 'Bus Error':
            print colors.MAGENTA,"Bus error encountered (%s), retrying operation (%d,%d)"%(register,nRetries,gRetries),colors.ENDC
        else:
            return parseInt(reg_val_s)
    return 0x0

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
    while (nRetries < gMAX_RETRIES):
        results = {}
        for reg in registers:
            results[reg] = readRegister(device, reg,debug)
            pass
        return results
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
        print colors.MAGENTA,"NODE NOT FOUND",colors.ENDC
        return 0x0

    if debug:
        print """Trying to read register %s (%s)\n
              address 0x%08x  mask 0x%08x  permission %s  \n
              """%(register,
                 m_node.name,
                 m_node.real_address,
                 m_node.mask,
                 m_node.permission
                 )
        pass
 
    words = []
    while (nRetries < gMAX_RETRIES):
        if (debug):
            print "reading %d words from register %s"%(nwords,register)
            pass
        for i in range(nwords):
            address = m_node.real_address + i
            word = rReg(address)
            words.append(word)
        if (debug):
            print words
            pass
        return words
        if ((nRetries % 10)==0):
            print colors.MAGENTA,"read error encountered (%s), retrying operation (%d,%d)"%(register,nRetries,gRetries),e,colors.ENDC
        continue
        pass
    # print colors.RED, "error encountered, retried read operation (%d)"%(nRetries)
    return []
    # return 0x0

def writeRegister(device, register, value, debug=False):
    """
    write value 'value' into register 'register' using remote procedure call
    """
    global gRetries
    nRetries = 0
    m_node = getNode(register)
    if m_node is None:
        print colors.MAGENTA,"NODE NOT FOUND",colors.ENDC
        return 0x0

    if debug:
        print """Trying to read register %s (%s)\n
              address 0x%08x  mask 0x%08x  permission %s  \n
              """%(register,
                 m_node.name,
                 m_node.real_address,
                 m_node.mask,
                 m_node.permission
                 )
        pass
 
    while (nRetries < gMAX_RETRIES):
        rsp = writeReg(m_node, value)
        if "permission" in rsp:
            print colors.MAGENTA,"NO WRITE PERMISSION",colors.ENDC
            return
        elif "Error" in rsp:
            print colors.MAGENTA,"write error encountered (%s), retrying operation (%d,%d)"%(register,nRetries,gRetries),colors.ENDC
            nRetries += 1
            gRetries += 1
            continue
        else: return 
        pass
    # print colors.RED, "error encountered, retried test write operation (%d)"%(nRetries)
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
        device.dispatch()
        return
    pass
