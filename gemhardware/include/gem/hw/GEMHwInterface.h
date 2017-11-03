#ifndef GEM_HW_HWINTERFACE_H
#define GEM_HW_HWINTERFACE_H

#include "uhal/uhal.hpp"
#include "uhal/Utilities.hpp"

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <memory>
#include "xhal/rpc/wiscrpcsvc.h"

#define STANDARD_CATCH \
	catch (wisc::RPCSvc::NotConnectedException &e) { \
		printf("Caught NotConnectedException: %s\n", e.message.c_str()); \
		return 1; \
	} \
	catch (wisc::RPCSvc::RPCErrorException &e) { \
		printf("Caught RPCErrorException: %s\n", e.message.c_str()); \
		return 1; \
	} \
	catch (wisc::RPCSvc::RPCException &e) { \
		printf("Caught exception: %s\n", e.message.c_str()); \
		return 1; \
	} \
	catch (wisc::RPCMsg::BadKeyException &e) { \
		printf("Caught exception: %s\n", e.key.c_str()); \
		return 0xdeaddead; \
	} 

#define ASSERT(x) do { \
    if (!(x)) { \
    	printf("Assertion Failed on line %u: %s\n", __LINE__, #x); \
    	return 1; \
    } \
} while (0)


typedef uhal::exception::exception uhalException;

namespace uhal {
  class HwInterface;
}

namespace gem {
  namespace hw {

    class GEMHwInterface
    {

    public:
      /*
       * @param type: 0 - RPC, 1 - uHAL
       */
      GEMHwInterface(int type, char * hostname); 
      ~GEMHwInterface(){}
      uint32_t readReg(std::string regName);
      uint32_t writeReg(std::string regName, uint32_t value);

    private:
      wisc::RPCSvc rpc;
      wisc::RPCMsg req, rsp;
      
      uint32_t init(char * hostname);
      uint32_t getReg(uint32_t address);
      uint32_t putReg(uint32_t address, uint32_t value);
      uint32_t getList(uint32_t* addresses, uint32_t* result, ssize_t size);
      uint32_t getBlock(uint32_t address, uint32_t* result, ssize_t size);
      uint32_t update_atdb(char * xmlfilename);
      uint32_t getRegInfoDB(char * regName);
    };
  }
}
#endif
