from flask import Flask
#importē subprocess, jo lookup finckijai to vajadzēs
import subprocess as su
def check(IP):
        #sadala IP adresi, ņemot punktus nost
        l=IP.split(".")
        #pārbauda vai katra oktate nav garāka par 3 simboliem, līdz ko ir vairāk, return False
        if len(l)!=4:
                return False
        #pārbauda vai cipars ir cipars
        for x in l:
                if not x.isdigit():
                        return False
                i=int(x)
                #notiek pārbaude vai ir starp 0-255
                if i < 0 or i > 255:
                        return False
        #ja viss sakrīt no pārbaudēm, va ir IPv4, tad returno True
        return True
def lookup(IP):
        #izmantojot subprocess Popen, var dabūt IP adreses informāciju
        #stdout=su.PIPE ievada to 'failā', kurā pēc tam tas tiek returnots lasot un dekodējot to uz utf8
        wh=su.Popen(['whois','-h','whois.cymru.com',IP], stdout=su.PIPE)
        return wh.stdout.read().decode('utf-8') 
