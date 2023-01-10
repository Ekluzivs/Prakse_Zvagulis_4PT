import requests as r
import re
#komanda lai iztiritu teksta failu, lai ievaditu iespejami jaunas IP adreses
open('visas_IP_adreses.txt','w').close()
open('unikalas_IP_adreses.txt','w').close()
#requestot majaslapu
url=r.get('http://www.inees.org/fileadmin/inees.org/files/logs/access.log.1')
log=url.text
#atradiis visus IP adreses no log majaslapas, izmantojot re.findall
#[^/] tiek izmantots lai nonemtu kuri ir log faila, bet nav ip adreses
def getallip(log):
    return re.findall(r'\b[^/]\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b',log)
#atver teksta failu un printes visas atrastas ip adreses no getallip(log) funkcijas
with open('visas_IP_adreses.txt', 'w') as ip:
    for i in getallip(log):
        ip.write(i+'\n')
ip.close()

#funkcija, kas parbaudis teskta unikalas adreses
def unikip(log):
    rez=re.findall(r'\b[^/]\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b',log)
    return set(rez)
#printes ara rezultatus bet ar unikalam ip adresem
with open('unikalas_IP_adreses.txt', 'w') as uip:
    for id in unikip(log):
        uip.write(id+'\n')