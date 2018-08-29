"""

    Mininet-WiFi: A simple networking testbed for Wireless OpenFlow/SDWN!

author: Ramon Fontes (ramonrf@dca.fee.unicamp.br)


"""

from subprocess import (check_output as co)

import os
import glob

from mininet.log import info
from mininet.clean import killprocs, sh, Cleanup as wired_cleanup
from mn_wifi.sixLoWPAN.clean import Cleanup as sixlowpan

class Cleanup(object):
    "Wrapper for cleanup()"

    @classmethod
    def cleanup_wifi(cls):
        wired_cleanup.cleanup(cls)
        Cleanup.NDN_cleanup(cls)
        """Clean up junk which might be left over from old runs;
           do fast stuff before slow dp and link removal!"""

        info("***  Removing WiFi module and Configurations\n")

        try:
            co("lsmod | grep mac80211_hwsim", shell=True)
            os.system('rmmod mac80211_hwsim')
        except:
            pass

        try:
            co("lsmod | grep ifb", shell=True)
            os.system('rmmod ifb')
        except:
            pass

        killprocs('hostapd')

        if glob.glob("*.apconf"):
            os.system('rm *.apconf')
        if glob.glob("*.staconf"):
            os.system('rm *.staconf')
        if glob.glob("*wifiDirect.conf"):
            os.system('rm *wifiDirect.conf')
        if glob.glob("*.nodeParams"):
            os.system('rm *.nodeParams')

        try:
            os.system('pkill -f \'wpa_supplicant -B -Dnl80211\'')
        except:
            pass

        info("*** Killing wmediumd\n")
        sh('pkill wmediumd')

        sixlowpan.cleanup_6lowpan()

    @classmethod
    def NDN_cleanup(cls):
        program_list = ("nfd", "minindn")
        for program in program_list:
            try:
                print("*** Killing {}\n".format(program))
                co("pkill -9 {}".format(program))
            except:
                pass

cleanup_wifi = Cleanup.cleanup_wifi
