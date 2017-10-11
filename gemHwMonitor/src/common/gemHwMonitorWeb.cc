#include "gem/hwMonitor/gemHwMonitorWeb.h"
#include <fstream>
#include <cstdlib>
#include "boost/algorithm/string.hpp"

XDAQ_INSTANTIATOR_IMPL(gem::hwMonitor::gemHwMonitorWeb);

gem::hwMonitor::gemHwMonitorWeb::gemHwMonitorWeb(xdaq::ApplicationStub* s)
  throw (xdaq::exception::Exception):
  xdaq::WebApplication(s)
{
  xgi::framework::deferredbind(this, this, &gemHwMonitorWeb::Default,                "Default"               );
  xgi::framework::deferredbind(this, this, &gemHwMonitorWeb::controlPanel,           "ControlPanel"         );
  xgi::framework::deferredbind(this, this, &gemHwMonitorWeb::help,                   "Help"                  );
  }

gem::hwMonitor::gemHwMonitorWeb::~gemHwMonitorWeb()
{
}

void gem::hwMonitor::gemHwMonitorWeb::Default(xgi::Input* in, xgi::Output* out )
  throw (xgi::exception::Exception)
{
  this->controlPanel(in, out);
}

/* Generates the main page interface. Allows to choose the configuration file, then
* shows the availability of crates corresponding to this configuration.
* Allows to launch the test utility to check the crates state.
* */
void gem::hwMonitor::gemHwMonitorWeb::controlPanel(xgi::Input* in, xgi::Output* out )
  throw (xgi::exception::Exception)
{
  try {
    *out << "<link rel=\"stylesheet\" type=\"text/css\" "
         << "href=\"/gemdaq/gemHwMonitor/html/css/bootstrap.css\">"
         << std::endl
         << "<link rel=\"stylesheet\" type=\"text/css\" "
         << "href=\"/gemdaq/gemHwMonitor/html/css/bootstrap-theme.css\">"
         << std::endl;
    *out << cgicc::script().set("type", "text/javascript")
      .set("src", "/gemdaq/gemHwMonitor/html/js/jquery.js")
         << cgicc::script() << std::endl;
    *out << cgicc::script().set("type", "text/javascript")
      .set("src", "/gemdaq/gemHwMonitor/html/js/bootstrap.min.js")
         << cgicc::script() << std::endl;
    *out << toolbox::toString("<base href=\"/%s/\" />",getApplicationDescriptor()->getURN().c_str()) << std::endl;


    std::ifstream myfile(std::getenv("BUILD_HOME")+std::string("/cmsgemos/gemHwMonitor/html/templates/nav.html"));
    std::string line;
    if (myfile.is_open()){
      while ( getline (myfile,line) )
        {
          *out << line;
          *out << std::endl;
        }
        myfile.close();
    } else{
      *out << "Unable to open file";
    }
    myfile.open(std::getenv("BUILD_HOME")+std::string("/cmsgemos/gemHwMonitor/html/templates/system_overview.html"));
    if (myfile.is_open()){
      while ( getline (myfile,line) )
        {
          *out << line;
          *out << std::endl;
        }
        myfile.close();
    } else{
      *out << "Unable to open file SYSTEM_OVERVIEW";
    }
  } catch (const xgi::exception::Exception& e) {
    LOG4CPLUS_INFO(this->getApplicationLogger(), "Something went wrong displaying ControlPanel xgi: "
                   << e.what());
    XCEPT_RAISE(xgi::exception::Exception, e.what());
  } catch (const std::exception& e) {
    LOG4CPLUS_INFO(this->getApplicationLogger(), "Something went wrong displaying the ControlPanel: "
                   << e.what());
    XCEPT_RAISE(xgi::exception::Exception, e.what());
  }
}

void gem::hwMonitor::gemHwMonitorWeb::help(xgi::Input* in, xgi::Output* out )
  throw (xgi::exception::Exception)
{
  try {
    *out << "<link rel=\"stylesheet\" type=\"text/css\" "
         << "href=\"/gemdaq/gemHwMonitor/html/css/bootstrap.css\">"
         << std::endl
         << "<link rel=\"stylesheet\" type=\"text/css\" "
         << "href=\"/gemdaq/gemHwMonitor/html/css/bootstrap-theme.css\">"
         << std::endl;
         *out << cgicc::script().set("type", "text/javascript")
           .set("src", "/gemdaq/gemHwMonitor/html/js/jquery.js")
              << cgicc::script() << std::endl;
         *out << cgicc::script().set("type", "text/javascript")
           .set("src", "/gemdaq/gemHwMonitor/html/js/bootstrap.min.js")
              << cgicc::script() << std::endl;


    std::ifstream myfile(std::getenv("BUILD_HOME")+std::string("/cmsgemos/gemHwMonitor/html/templates/nav.html"));
    std::string line;
    if (myfile.is_open()){
      while ( getline (myfile,line) )
        {
          *out << line;
        }
        myfile.close();
      *out << "THIS IS A HELP PAGE";
    } else{
      *out << "Unable to open file";
    }
  } catch (const xgi::exception::Exception& e) {
    LOG4CPLUS_INFO(this->getApplicationLogger(), "Something went wrong displaying ControlPanel xgi: "
                   << e.what());
    XCEPT_RAISE(xgi::exception::Exception, e.what());
  } catch (const std::exception& e) {
    LOG4CPLUS_INFO(this->getApplicationLogger(), "Something went wrong displaying the ControlPanel: "
                   << e.what());
    XCEPT_RAISE(xgi::exception::Exception, e.what());
  }
}
