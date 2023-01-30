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
count=0
for ip in `cat uniq_ip_adr.txt`
do
# Kods, kurā tiks pārmests caur /dev/null, neizveidojot papildus rezultātu ja komandu rinda nokļūdas
#tad izveido meh=$? mainīgo
# kurā tad if statement, pārbauda vai mainīgais meh ir 0, ja ir, tad tas turpina ciklu 
#Neieliekot mainīgajā, bet rakstot iekšā "failā", vari izvilkt rezultātu izmantojot cat, lai izlasa whois.out failu
whois $ip > whois.out
whotest=$(cat whois.out 2>/dev/null)
meh=$?

# bija mēģināts 10 dažādos veidos, šis pēdējais:
#if ! [[ $(cat whois.out | grep -E -i connect) ]]; then
#, taču tas tik un tā laida IP adreses uz LV_IP.txt

if [ $meh -eq 0 ]; then
#izmantojot awk palīdzību, tiks atrasts specifisks valsts, izprintējot IP adresi teksta failā no tās valsts
valsts=$(cat whois.out | grep -i country | awk '{if(NF>0)print $NF}')
if [ "$valsts" == "LV" ]; then
let "count+=1"
echo $ip >> LV_IP.txt
# Tiek veikta epastu pārbaude, sākumā meklējot kur ir abuse, tad epastu, kurā tad printē teksta failā
echo "$ip" >> kontakti.txt
cat whois.out | grep -E -i abuse | grep -E -o "\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b" >> kontakti.txt
echo "----" >> kontakti.txt
fi
fi
done
echo "To valsts IP adreses: $count"
