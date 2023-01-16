
import ipdata
import re
import json
import time
#API key
#   0fee565e02a55faab7a113c85326c51f1f7ca5fba27748f5e698ebd1
#   bdd353d3399a82ea7677b5fc0dadb498376062bc077e2862bd714d34
ipdata.api_key="0fee565e02a55faab7a113c85326c51f1f7ca5fba27748f5e698ebd1"
    #ve atver un iztukso ierakstus, gadijuma ja izmaiņas notikušas, kā arī tiek turēts vaļā lai tiek ierakstīts ciklā
    #ip ir fails kurā ir visas unikālās ip adreses
ve=open('teksti/visasvalstsIP.txt','w')
ip=open('../../unikalas_IP_adreses.txt', 'r')
ipi=ip.readlines()
    #cikls, izņem jaunas līnijas "\n", ipdata meklē ip adreses un valsts no ip txt faila
    #pēc tam tas tiek ielikts iekša atsevisķi directorejā, 
    #izmantojot json, tas tiks ierakstīts ve txt failā, ar IP un valsti'''
dicti={}
for ipip in ipi:
    adr=ipip.strip('\n')
    ipisniks=ipdata.lookup(adr,fields=['ip'])
    valsts=ipdata.lookup(adr,fields=['country_name'])
    #print(ipisniks, valsts)
    #print(ipisniks["ip"])
    dicti["IP adrese"]=ipisniks
    dicti["Valsts"]=valsts
    ve.write(json.dumps(dicti)+'\n')
ve.close()
    #tas pats princips, LV_ier noņem pārrakstīs jaunus ierakstus, LV lasīs no visas valsts IP txt faila
US=open('teksti/visasvalstsIP.txt','r').readlines()
US_ier=open('teksti/Latvijas_IP.txt','w')
    #uzsāk laika atskaiti
laiks=time.time()
    #sākas for cikls, kurā tiek meklēts konkrēta valsts un tiks izprintēts ASV IP adrese
for Uss in US:
    ASVV=re.findall(r"United States", Uss)
    if "United States" in ASVV:
        ASIP=re.findall(r"(\d[0-9]{1,3}\.\d[0-9]{1,3}\.\d[0-9]{1,3}\.\d[0-9]{1,3})", Uss)
        dicti["IP adrese"]=ASIP
        US_ier.write(json.dumps(dicti['IP adrese'])+'\n')
    #laika atskaite beidzās, pēc aprēķina, tiks izprintēts laiks
laiks_end=time.time()
pag_laik=laiks-laiks_end
print(pag_laik)

