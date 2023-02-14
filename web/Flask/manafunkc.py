from flask import Flask
import subprocess as su
def check(IP):
        #splits the comma and whitespace so it's a clean IP address
        IP=IP.split(", ")
        for K in IP:
                l=K.split(".")
        #this function checks if each octet is less than 3 numbers, if it's, let's say 2555 and not 255, it'll return a false
                if len(l)!=4:
                        return False
        #this check for each digit in the octet if there is a number, if it's, let's say 25a and not 255, it'll return a false
                for x in l:
                        if not x.isdigit():
                                return False
                        i=int(x)
                #then another if statement is made, it checks the range between 0 to 255, anything less or above that returns a false result
                        if i < 0 or i > 255:
                                return False
        #if no false result has been made, the function ends with the result True 
        return True
def lookup(IP):
        #before the for cycle, first removing the comma and the whitespace in the string, so it's just a clean IP
        #then we create a dictionary before the cycle
        IP=IP.split(", ")
        d={}
        #while on for cycle, the IP is read in the whois statement (getwhois) where it then get's outputted in a file (whoispopen)  
        #then it get's read and decoded to UTF-8 from the PIPE "file"
        #after that it replaces all the new lines (\n) with empty, where the output is then passed onto a dictionary as value, with the IP as key
        for IPs in IP
                getwhois=['whois','-h','whois.cymru.com',IPs] 
                whoispopen=su.Popen(getwhois, stdout=su.PIPE)
                whoispopen=whoispopen.stdout.read().decode('utf-8')
                output=whoispopen.replace("\n","")
                d={IPs:output}
        return d
