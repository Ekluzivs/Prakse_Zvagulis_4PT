#!/bin/bash
touch vis_ip_adr.txt
touch uniq_ip_adr.txt
touch LV_IP.txt
touch kontakti.txt
grep -o -m 5000 -E "\b[^/ . : v]([0-9]{1,3}\.){3}[0-9]{1,3}\b" access.log > vis_ip_adr.txt
sort -u vis_ip_adr.txt > uniq_ip_adr.txt
> LV_IP.txt
> kontakti.txt
echo "notiek IP meklesana"
for ip in `cat uniq_ip_adr.txt`
do
echo "$ip" >> LV_IP.txt
whois $ip | grep country | grep CN >> LV_IP.txt
done
echo "notiek epastu meklesana un drukasana"
for daudz in `cat uniq_ip_adr.txt`
do
echo "$daudz" >> kontakti.txt
whois $daudz | grep -E -i abuse | grep -E -o "\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b" >> kontakti.txt
echo "----" >> kontakti.txt
done
