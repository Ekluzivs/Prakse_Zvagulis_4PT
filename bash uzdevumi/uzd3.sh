#!/bin/bash
#izveido teksta failus
touch vis_ip_adr.txt
touch uniq_ip_adr.txt
touch LV_IP.txt
touch kontakti.txt
#atrod visas IP adreses izmantojot egrep (grep -E)
#tiek izvilkta IPv4, tiek pārbaudīta katra oktate paternā
grep -o -E "(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)" access.log > vis_ip_adr.txt
#atlasa unikālās IP adreses no visām ip adresēm
sort -u vis_ip_adr.txt > uniq_ip_adr.txt
#iztīra teksta failu
> LV_IP.txt
> kontakti.txt
#notiek IP adrešu valsts meklēšana, ja ir Latvija, tad tiks izprintēts IP adrese kas ir no Latvijas 
echo "notiek IP meklesana"
for ip in `cat uniq_ip_adr.txt`
do
#izmantojot awk palīdzību, tiks atrasts specifisks valsts, izprintējot IP adresi teksta failā no tās valsts
valsts=$(whois $ip | grep -i country | awk '{if(NF>0)print $NF}')
if [ "$valsts" == "LV" ]; then
echo $ip >> LV_IP.txt
fi
done
# Notiek Epastu meklēšana, izmantojot līdzīgu metodi, atrod IP, atrod kur ir abuse līnijā, tad atrod E pasta adresi no tās līnijas, kas tiks izprintēts
# Tiek izprintēti ja satur vairākas IP adreses
echo "notiek epastu meklesana un drukasana"
for daudz in `cat uniq_ip_adr.txt`
do
echo "$daudz" >> kontakti.txt
whois $daudz | grep -E -i abuse | grep -E -o "\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b" >> kontakti.txt
echo "----" >> kontakti.txt
done
