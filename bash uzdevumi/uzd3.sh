#!/bin/bash
#izveido teksta failus
touch vis_ip_adr.txt
touch uniq_ip_adr.txt
touch LV_IP.txt
touch kontakti.txt
#atrod visas IP adreses izmantojot EGREP, notiek pārbaude vai IP adresēm sastāv nevajadzīgi simboli pirms IP adreses, ja sastāv, netiek atlasīts
#ja nesastāv (/ . : v) tad tiek izdrukāts teksta failā
grep -o -E "\b[^/ . : v]([0-9]{1,3}\.){3}[0-9]{1,3}\b" access.log > vis_ip_adr.txt
#atlasa unikālās IP adreses no visām ip adresēm
sort -u vis_ip_adr.txt > uniq_ip_adr.txt
#iztīra teksta failu
> LV_IP.txt
> kontakti.txt
#notiek IP adrešu valsts meklēšana, ja ir Latvija, tad tiks izprintēts IP adrese kas ir no Latvijas 
echo "notiek IP meklesana"
for ip in `cat uniq_ip_adr.txt`
do
echo "$ip" >> LV_IP.txt
whois $ip | grep country | grep LV >> LV_IP.txt
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
