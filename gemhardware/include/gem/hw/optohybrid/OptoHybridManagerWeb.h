#ifndef GEM_HW_OPTOHYBRID_OPTOHYBRIDMANAGERWEB_H
#define GEM_HW_OPTOHYBRID_OPTOHYBRIDMANAGERWEB_H

#include "gem/base/GEMWebApplication.h"

namespace gem {
  namespace hw {
    namespace optohybrid {

      class OptoHybridManager;

      class OptoHybridManagerWeb : public gem::base::GEMWebApplication
        {
          //friend class OptoHybridMonitor;
          //friend class OptoHybridManager;

        public:
          OptoHybridManagerWeb(OptoHybridManager *optohybridApp);

          virtual ~OptoHybridManagerWeb();

        protected:

          virtual void webDefault(  xgi::Input *in, xgi::Output *out )
            throw (xgi::exception::Exception);

          virtual void monitorPage(xgi::Input *in, xgi::Output *out)
            throw (xgi::exception::Exception);

          virtual void expertPage(xgi::Input *in, xgi::Output *out)
            throw (xgi::exception::Exception);

          virtual void applicationPage(xgi::Input *in, xgi::Output *out)
            throw (xgi::exception::Exception);

          virtual void jsonUpdate(xgi::Input *in, xgi::Output *out)
            throw (xgi::exception::Exception);

          void boardPage(xgi::Input *in, xgi::Output *out)
            throw (xgi::exception::Exception);

        private:
          size_t activeBoard;

          //OptoHybridManagerWeb(OptoHybridManagerWeb const&);

        };

    }  // namespace gem::optohybrid
  }  // namespace gem::hw
}  // namespace gem

#endif  // GEM_HW_OPTOHYBRID_OPTOHYBRIDMANAGERWEB_H
