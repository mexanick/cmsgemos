#include "gem/hw/GEMHwInterface.h"

gem::hw::GEMHwInterface::GEMHwInterface(int type, char * hostname)
{
  switch(type) {
    case 1: std::cout << "uHAL, TBI" << std::endl;
    default:{
      // RPC hardware interface
      this->init(hostname);
    }
  };
}

uint32_t gem::hw::GEMHwInterface::init(char * hostname)
{
    try {
        rpc.connect(hostname);
    }
    catch (wisc::RPCSvc::ConnectionFailedException &e) {
        printf("Caught RPCErrorException: %s\n", e.message.c_str());
        return 1;
    }
    catch (wisc::RPCSvc::RPCException &e) {
        printf("Caught exception: %s\n", e.message.c_str());
        return 1;
    }

    try {
        ASSERT(rpc.load_module("memory", "memory v1.0.1"));
        ASSERT(rpc.load_module("extras", "extras v1.0.1"));
        ASSERT(rpc.load_module("utils", "utils v1.0.1"));
        ASSERT(rpc.load_module("optohybrid", "optohybrid v1.0.1"));
        ASSERT(rpc.load_module("amc", "amc v1.0.1"));
        ASSERT(rpc.load_module("calibration_routines", "calibration_routines v1.0.1"));
        ASSERT(rpc.load_module("vfat3", "vfat3 v1.0.1"));
    }
    STANDARD_CATCH;

    return 0;
}

uint32_t gem::hw::GEMHwInterface::update_atdb(char * xmlfilename)
{
    req = wisc::RPCMsg("utils.update_address_table");
    req.set_string("at_xml", xmlfilename);
    try {
        rsp = rpc.call_method(req);
    }
    STANDARD_CATCH;

    if (rsp.get_key_exists("error")) {
        return 1;
    }
    return 0;
}

uint32_t gem::hw::GEMHwInterface::getRegInfoDB(char * regName)
{
    uint32_t address, mask;
    std::string permissions;
    req = wisc::RPCMsg("utils.readRegFromDB");
    req.set_string("reg_name", regName);
    try {
        rsp = rpc.call_method(req);
    }
    STANDARD_CATCH;

    if (rsp.get_key_exists("error")) {
        return 1;
    }
    printf("Register %s is found \n",regName);
    try {
        address = rsp.get_word("address");
        mask = rsp.get_word("mask");
        permissions = rsp.get_string("permissions");

        printf("Address: 0x%8x, permissions: %s, mask: 0x%8x \n", address, permissions.c_str(), mask);
    }
    STANDARD_CATCH;
    return 0;
}

uint32_t gem::hw::GEMHwInterface::getReg(uint32_t address)
{
    req = wisc::RPCMsg("memory.read");
    req.set_word("address", address);
    req.set_word("count", 1);
    try {
        rsp = rpc.call_method(req);
    }
    STANDARD_CATCH;

    uint32_t result;
    try{
        if (rsp.get_key_exists("error")) {
            return 0xdeaddead;
        } else {
            ASSERT(rsp.get_word_array_size("data") == 1);
            rsp.get_word_array("data", &result);
        }
    }
    STANDARD_CATCH;

    return result;
}

uint32_t gem::hw::GEMHwInterface::getBlock(uint32_t address, uint32_t* result, ssize_t size)
{
    req = wisc::RPCMsg("extras.blockread");
    req.set_word("address", address);
    req.set_word("count", size);
    try {
        rsp = rpc.call_method(req);
    }
    STANDARD_CATCH;

    try{
        if (rsp.get_key_exists("error")) {
            return 1;
        } else {
            ASSERT(rsp.get_word_array_size("data") == size);
            rsp.get_word_array("data", result);
        }
    }
    STANDARD_CATCH;
    return 0;
}

uint32_t gem::hw::GEMHwInterface::getList(uint32_t* addresses, uint32_t* result, ssize_t size)
{
    req = wisc::RPCMsg("extras.listread");
    req.set_word_array("addresses", addresses,size);
    req.set_word("count", size);
    try {
        rsp = rpc.call_method(req);
    }
    STANDARD_CATCH;

    try{
        if (rsp.get_key_exists("error")) {
            return 1;
        } else {
            ASSERT(rsp.get_word_array_size("data") == size);
            rsp.get_word_array("data", result);
        }
    }
    STANDARD_CATCH;
    return 0;
}

uint32_t gem::hw::GEMHwInterface::putReg(uint32_t address, uint32_t value)
{
    req = wisc::RPCMsg("memory.write");
    req.set_word("address", address);
    req.set_word_array("data", &value,1);
    try {
        rsp = rpc.call_method(req);
    }
    STANDARD_CATCH;
    if (rsp.get_key_exists("error")) {
        return 0xdeaddead;
    } else return value;
}
