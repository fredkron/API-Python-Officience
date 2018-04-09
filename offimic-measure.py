#!/usr/bin/env python2.7

# crontab:
# */10 * * * * /home/fred/Src/PYTHON-API/offimic-measure.py


import os, sys, urllib, subprocess

os.system("ping 192.168.1.255 -b -c5 -W1 -q")
iface = "wlan0"
p = subprocess.Popen(
    ("/usr/sbin/arp -ani %s | wc -l" % iface), 
    stdout=subprocess.PIPE, 
    shell=True
)
(out, err)=p.communicate()
count=out.rstrip()


print("Detected %s machines" % count)
urllib.urlopen("http://localhost:5000/count/"+count)
print("success")


#arp -a

#home:
#192.168.0.254
#wls35

#offi:
#192.168.1.255
#wlan0