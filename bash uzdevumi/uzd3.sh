#!/bin/bash
#debug
  #set -x
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
# Kods, kurā tiks pārmests caur /dev/null, neizveidojot papildus rezultātu ja komandu rinda nokļūdas
#tad izveido meh=$? mainīgo
# kurā tad if statement, pārbauda vai mainīgais meh ir 0, ja ir, tad tas turpina ciklu 
    #mēģinot ielikt `whois $ip` mainīgajā veido printēšanas kļūdu, siera bloka tekstu no tā IP adrešu informācijas izmantojot whois
    #izmantojot `whois $ip` atsevišķi veido smuku rezultātu skatoties pēc `set -x`
  #whotest=`whois $ip 2>/dev/null`
  #meh=$?
  #if [ $meh -eq 0 ]; then
  #whout=$(whois $ip)
#izmantojot awk palīdzību, tiks atrasts specifisks valsts, izprintējot IP adresi teksta failā no tās valsts
         #$whout
valsts=$(whois $ip | grep -i country | awk '{if(NF>0)print $NF}')
if [ "$valsts" == "LV" ]; then
echo $ip >> LV_IP.txt
# Tiek veikta epastu pārbaude, sākumā meklējot kur ir abuse, tad epastu, kurā tad printē teksta failā
echo "$daudz" >> kontakti.txt
#$whout
whois $daudz | grep -E -i abuse | grep -E -o "\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b" >> kontakti.txt
echo "----" >> kontakti.txt
fi
fi
done
