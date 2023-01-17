
import ipdata
import re
import time
import subprocess as su
#API key
#   0fee565e02a55faab7a113c85326c51f1f7ca5fba27748f5e698ebd1
#   bdd353d3399a82ea7677b5fc0dadb498376062bc077e2862bd714d34
ipdata.api_key="0fee565e02a55faab7a113c85326c51f1f7ca5fba27748f5e698ebd1"
    #ve atver un iztukso ierakstus, gadijuma ja no unikalajam IP adresem ir kas jauns
    #ip fails satur visas unikalas IP adreses
    #ip.readlines()[x] lasīs limitētu daudzumu
ve=open('teksti/visasvalstsIP_1.txt','w')
ip=open('../../unikalas_IP_adreses.txt', 'r')
ipi=ip.readlines()[:10]
    #izveidots cikls, kurā lasīs visas unikālās IP adreses, to informāciju un valsts kodu, izmantojot subprocess
    #Popen, kurā tiks izdrukāts uz faila IP adrešu informācija
for ipip in ipi:
    with su.Popen(['whois', '-h', 'whois.cymru.com', '-c',ipip],stdout=su.PIPE) as ipisniks:
        ve.write(ipisniks.stdout.read().decode('utf-8'))
ve.close()
    #tas pats princips, LV_ier noņem pārrakstīs jaunus ierakstus, LV lasīs no visas valsts IP txt faila
US=open('teksti/visasvalstsIP.txt','r').readlines()
US_ier=open('teksti/Latvijas_IP.txt','w')
    #uzsāk laika atskaiti
laiks=time.time()
    #sākas for cikls, kurā tiek meklēts konkrēta valsts kods un tiks izprintēts to valsts IP adrese
for Uss in US:
    ASVV=re.findall(r"CN", Uss)
    if "CN" in ASVV:
        ASIP=re.findall(r"(\d[0-9]{1,3}\.\d[0-9]{1,3}\.\d[0-9]{1,3}\.\d[0-9]{1,3})", Uss)
        US_ier.write(''.join(ASIP)+'\n')
    #laika atskaite beidzās, pēc aprēķina, tiks izprintēts laiks
laiks_end=time.time()
pag_laik=laiks-laiks_end
print(pag_laik)


