#!/usr/bin/env python2.7

# crontab:
# */10 * * * * /home/fred/Src/PYTHON-API/offimic-measure-sqlite.py


import os, sys, urllib, subprocess, hashlib

#os.system("ping 192.168.1.255 -b -c5 -W1 -q")
os.system("ping 192.168.0.255 -b -c5 -W1 -q > /dev/null 2>&1")
#iface = "wlan0"
iface = "wls35"
p = subprocess.Popen(
    ("/usr/sbin/arp -ani %s | cut -f4 --delim=' '" % iface), 
    stdout=subprocess.PIPE, 
    shell=True
)
(out, err)=p.communicate() # Executer le shell, recuperer la sortie dans "out"

macs=out.split("\n") # Transformer en tableau de lignes
macs=[x for x in macs if x] # Supprimer elements vides
count=len(macs) # Compter les entrees

# Etape 1: inserer dans capture, recuperer l'ID de la nouvelle entree
response=urllib.urlopen("http://localhost:5000/count/"+str(count))
lastrowid=int(response.read().rstrip())

# Etape 2: inserer les MAC une par une
for mac in macs:
    macHash=hashlib.md5(mac).hexdigest()
    urllib.urlopen("http://localhost:5000/presence/"+str(lastrowid)+"/"+macHash)

#arp -a

#home:
#192.168.0.254
#wls35

#offi:
#192.168.1.255
#wlan0