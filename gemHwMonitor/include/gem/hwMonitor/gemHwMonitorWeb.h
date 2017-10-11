/** @file gemHwMonitorWeb.h */

#ifndef GEM_HWMONITOR_GEMHWMONITORWEB_H
#define GEM_HWMONITOR_GEMHWMONITORWEB_H

#include <string>
#include <vector>
#include <sys/stat.h>

#include "cgicc/HTMLClasses.h"

#include "xdaq/WebApplication.h"
#include "xgi/framework/Method.h"

//#include "gemHwMonitorBase.h"
//#include "gemHwMonitorHelper.h"

namespace cgicc {
  BOOLEAN_ELEMENT(section, "section");
}
namespace gem {

  namespace hwMonitor {
    class gemHwMonitorWeb: public xdaq::WebApplication
      {
      public:
        XDAQ_INSTANTIATOR();
        gemHwMonitorWeb(xdaq::ApplicationStub* s)
          throw (xdaq::exception::Exception);
        ~gemHwMonitorWeb();
        void Default(xgi::Input* in, xgi::Output* out )
          throw (xgi::exception::Exception);
        void controlPanel(xgi::Input* in, xgi::Output* out)
          throw (xgi::exception::Exception);
        void help(xgi::Input* in, xgi::Output* out)
          throw (xgi::exception::Exception);

      //private:

      };  // class gemHwMonitorWeb
  }  // namespace gem::hwMonitor
}  // namespace gem

#endif  // GEM_HWMONITOR_GEMHWMONITORWEB_H
