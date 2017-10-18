import os
#import sys
#BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
#sys.path.append(BASE_DIR)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "gempython.utils.db.settings")
import django
django.setup()
import datetime
from time import sleep
from gempython.utils.db.ldqm_db.models import *
from gempython.utils.db.ldqm_db.amcmanager import *

#from gempython.utils.gemlogger import GEMLogger
#
#gemlogger = GEMLogger("query").gemlogger
#gemlogger.setLevel(GEMLogger.DEBUG)

def configure_db(station="CERNP5",setuptype="slicetest",runperiod="2017", runnumber = 2):
  #gebtypes = { "GTX-1":"Short",
  #             "GTX-2":"Short",
  #             "GTX-3":"Short",
  #             "GTX-4":"Short",
  #             "GTX-5":"Long",
  #             "GTX-6":"Long",
  #             "GTX-7":"Short",
  #             "GTX-8":"Short",
  #             "GTX-9":"Long",
  #             "GTX-10":"Long"}

  #gebs = { "GTX-1":["0xfebb", "0xfec0", "0xfe38", "0xf957", "0xf774", "0xff74", "0xfebc", "0xf77c", "0xfec4", "0xfef4", "0xffb3", "0xfa0c", "0xff94", "0xfe28", "0xf9b7", "0xf92b", "0xf737", "0xfeb3", "0xf9a0", "0xf993", "0xf75c", "0xfedb", "0xffd4", "0xfe24"],
  #         "GTX-2":["0xffac", "0xfa38", "0xff7f", "0xfefb", "0xff73", "0xf71c", "0xfff7", "0xfe2c", "0xf9eb", "0xfed7", "0xfa37", "0xf9bb", "0xf96b", "0xfef3", "0xff78", "0xf9bc", "0xfecc", "0xff34", "0xf6bb", "0xfa47", "0xff30", "0xf74b", "0xff9f", "0xfed4"],
  #         "GTX-3":["0xf758", "0xff68", "0xff2b", "0xf73c", "0xff27", "0xff7c", "0xf72c", "0xff14", "0xff6f", "0xf788", "0xffaf", "0xf73b", "0xf6ac", "0xf6d8", "0xf97b", "0xfec3", "0xf750", "0xfff3", "0xf76f", "0xffd0", "0xffc0", "0xfe3b", "0xf9fc", "0xf9ac"],
  #         "GTX-4":["0xff97", "0xf9c4", "0xf6f3", "0xfa03", "0xf964", "0xf6c3", "0xfa53", "0xf99f", "0xf718", "0xf9a7", "0xf6b3", "0xf9f4", "0xf93f", "0xf9f3", "0xf748", "0xf70b", "0xff18", "0xfa48", "0xf9dc", "0xfa4f", "0xf988", "0xf723", "0xff38", "0xf730"],
  #         "GTX-5":["0xf943", "0xf743", "0xf787", "0xf6cb", "0xffdf", "0xff44", "0xf783", "0xfa13", "0xf9f7", "0xf6b0", "0xf6cc", "0xfe27", "0xf920", "0xf968", "0xf77b", "0xff3c", "0xf6ec", "0xff67", "0xffc7", "0xf6dc", "0xf9c8", "0xf6a4", "0xff58", "0xffd7"],
  #         "GTX-6":["0xfe47", "0xf6b4", "0xf6a3", "0xf72f", "0xfa07", "0xff9c", "0xf77f", "0xff98", "0xf98b", "0xf6e3", "0xff64", "0xffbb", "0xfe43", "0xf98f", "0xf784", "0xf940", "0xff54", "0xff17", "0xf944", "0xf6bf", "0xf9e8", "0xf6ff", "0xf720", "0xf770"],
  #         "GTX-7":["0xfebf", "0xfe34", "0xffb8", "0xffd3", "0xf9d4", "0xfedf", "0xff1c", "0xfe1f", "0xf738", "0xf9cc", "0xffeb", "0xff70", "0xfa14", "0xff0c", "0xfa24", "0xffe0", "0xff57", "0xfee7", "0xfe37", "0xf9ff", "0xfff8", "0xf707", "0xf9f8", "0xf724"],
  #         "GTX-8":["0xf6b8", "0xfa10", "0xf9c0", "0xffc8", "0xfe3c", "0xf773", "0xf9b8", "0xffa0", "0xfa2b", "0xfa33", "0xf708", "0xf71f", "0xf767", "0xff10", "0xf96f", "0xfe4b", "0xfee8", "0xf714", "0xfe3f", "0xf6f8", "0xf973", "0xfe20", "0xfee0", "0xf6d4"],
  #         "GTX-9":["0xf6e7", "0xfec8", "0xf98c", "0xf9e0", "0xffc4", "0xf704", "0xff5f", "0xf978", "0xfe44", "0xf78b", "0xf6df", "0xf777", "0xfa5b", "0xf91b", "0xfed0", "0xfe23", "0xfa1f", "0xf6e8", "0xfa1c", "0xff28", "0xfe2b", "0xffa3", "0xff6c", "0xf953"],
  #         "GTX-10":["0xf950", "0xf6a8", "0xfed8", "0xf763", "0xf977", "0xf6ab", "0xfa50", "0xf9cb", "0xfeec", "0xf733", "0xfee4", "0xf717", "0xfef8", "0xf734", "0xf924", "0xffb4", "0xf6f4", "0xfa34", "0xf6b7", "0xf72b", "0xffa7", "0xf95f", "0xf6af", "0xff3f"]}
 
  ##amc = AMC.objects.get(Type="eagle33")
  ##print "Chambers %s"%(amc.gebs.all())
  #amc = AMC(Type="eagle33", BoardID = "AMC-3")
  #print "Adding AMC eagle33 "
  #amc.save()

  #for gebname in gebs.keys():
  #  chipids = gebs[gebname]
  #  gebtype = gebtypes[gebname]
  #  geb = GEB(Type=gebtype, ChamberID = gebname)
  #  #geb = GEB.objects.get(Type=gebtype, ChamberID = gebname)
  #  #print "GEB %s contains VFATS: \n %s" %(geb, list(geb.vfats.all()))
  #  print "Adding GEB %s %s" %(gebname, gebtype)
  #  geb.save()
  #  for slot, chipid in enumerate(chipids):
  #    #print "Trying to get %s, %s" %(chipid, slot)
  #    vfat = VFAT(ChipID = chipid, Slot = slot)
  #    #print "Retrieved VFAT %s" %(vfat)
  #    print "Adding VFAT %s %s" %(slot, chipid)
  #    vfat.save()
  #    geb.vfats.add(vfat)
  #  amc.gebs.add(geb)

  # create a new run. Some values are hard-coded for now
  amc = AMC.objects.get(Type="eagle33")
  t_date = str(datetime.datetime.utcnow()).split(' ')[0]
  nrs = u'%s'%(runnumber)
  nrs = nrs.zfill(6)
  m_filename = "run"+str(nrs)+""+"_"+setuptype+"_"+station+"_"+t_date
  newrun = Run(Name=m_filename, Type = setuptype, Number = str(nrs), Date = t_date, Period = runperiod, Station = station)
  newrun.save()
  newrun.amcs.add(amc)

if __name__ == '__main__':
  configure_db()
