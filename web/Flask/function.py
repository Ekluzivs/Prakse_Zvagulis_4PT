from flask import Flask
import subprocess as su
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
        #before the for cycle, first removing the comma and the whitespace in the string, so it's just a clean IP
        #then we create a dictionary before the cycle
        IP=IP.split(", ")
        d={}
        #while on for cycle, the IP is read in the whois statement (getwhois) where it then get's outputted in a file (whoispopen)  
        #then it get's read and decoded to UTF-8 from the PIPE "file"
        for IPs in IP:
                cau=check(IPs)
                if cau==False:
                        d[IPs]={'ISPI':"Not a valid IP address", 'valst': "No information"}
                else:
                        getwhois=['whois','-h','whois.cymru.com',IPs] 
                        whoispopen=su.Popen(getwhois, stdout=su.PIPE)
                        whoispopen=whoispopen.stdout.read().decode('utf-8')
                        output=whoispopen.replace("\n","")
                        #Index is gathering the last four characters of output, meanwhile it checks if output is empty, if it is,
                        #it would update the dictionary with it's values as "No information"
                        #also it checks if the last four characters contain "| NA" in index, NA means no information, if true, outputs like the previous if statement
                        index=output[-4:]
                        if not output:
                                d[IPs]={'ISPI':"No information", 'valst': "No information"}}
                        elif "| NA" in index:
                                d[IPs]={'ISPI':"No information", 'valst': "No information"}}
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
