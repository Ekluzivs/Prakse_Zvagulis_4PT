from flask import Flask
import subprocess as su
import re
#creating a pattern using regex to find whitespaces in string
patterna=r"\s+"
def check(IPs):
        #splits the comma and whitespace so it's a clean IP address
        l=IPs.split(".")
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
        #before the loop cycle, IP.split splits the IP addresses where then the I strips of all trailing and leading whitespaces
        IP=[I.strip() for I in IP.split(",")]
        d={}
        for IPs in IP:
                #vai_ir uses a re.findall to find any occurances of whitespaces within the string
                #if it finds it, it'll update the dictionary and start over with new string
                vai_ir=re.findall(patterna, IPs)
                if any(ir.isspace() for ir in vai_ir):
                        d[IPs]={'ISPI':"Space has been detected between two or more IP address', please put a comma", 'valst': "No information"}
                else:
                        #if no whitespace, then begins the IP check, if check(IPs) returns a false,then it updates the dictionary and starts a new IP address
                        checked=check(IPs)
                        if checked==False:
                                d[IPs]={'ISPI':"Not a valid IP address", 'valst': "No information"}
                        else:
                                #getwhois and whoispopen is used to get the information (if exists) from the inputted IP address
                                #whoispopen is then read and decoded from the "PIPE" file and decoded to UTF-8, where it then replaces
                                #all of the new lines with empty
                                getwhois=['whois','-h','whois.cymru.com',IPs] 
                                whoispopen=su.Popen(getwhois, stdout=su.PIPE)
                                whoispopen=whoispopen.stdout.read().decode('utf-8')
                                output=whoispopen.replace("\n","")
                                #Index is gathering the last four characters of output, meanwhile it checks if output is empty, if it is,
                                #it would update the dictionary with it's values as "No information"
                                #also it checks if the last four characters contain "| NA" in index, NA means no information, if true, outputs like the previous if statement
                                index=output[-4:]
                                if not output:
                                        d[IPs]={'ISPI':"No information", 'valst': "No information"}
                                elif "| NA" in index:
                                        d[IPs]={'ISPI':"No information", 'valst': "No information"}
                                #if all is well, else command begins manipulating the data
                                #output replaces all of the unnecessary data with empty, after that, spliteris removes all cases of "| " where it then gathers the information
                                #from the 3rd element in the string, where the ISP variable removes all instances of commas and gathers the information from the 1st element
                                else:
                                        output=output.replace("AS      | IP               | AS Name","")
                                        spliteris=output.split("| ")[2]
                                        ISP=spliteris.split(", ")[0]
                                        #finally valsts variable gathers the last 2 characters from the output to use as a country code
                                        valsts=output[-2:]
                                        d[IPs]={'ISPI':ISP, 'country': valsts}
        return d
