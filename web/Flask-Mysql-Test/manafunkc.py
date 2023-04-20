from flask import Flask
import re
import subprocess as su
patterna=r"\s+"
def check(IPs):
        l=IPs.split(".")
        if len(l)!=4:
                return False
        for x in l:
                if not x.isdigit():
                        return False
                i=int(x)
                if i < 0 or i > 255:
                        return False
        return True
def lookup(IP):
        IP=[I.strip() for I in IP.split(",")]
        d={}
        for IPs in IP:
                vai_ir=re.findall(patterna, IPs)
                if any(ir.isspace() for ir in vai_ir):
                        d[IPs]={'ISPI':"Space has been detected between two or more IP address', please put a comma", 'valst': "No information"}
                else:
                        checked=check(IPs)
                        if checked==False:
                                d[IPs]={'ISPI':"Not a valid IP address", 'valst': "No information"}
                        else:
                                getwhois=['whois','-h','whois.cymru.com', IPs]
                                whoispopen=su.Popen(getwhois, stdout=su.PIPE)
                                whoispopen=whoispopen.stdout.read().decode('utf-8')
                                output=whoispopen.replace("\n","")
                                index=output[-4:]
                                if not output:
                                                d[IPs]={'ISPI':"No information", 'valst': "No information"}
                                elif "| NA" in index:
                                                d[IPs]={'ISPI':"No information", 'valst': "No information"}
                                else:
                                        output=output.replace("AS      | IP               | AS Name","")
                                        print(output)
                                        spliteris=output.split("| ")[2]
                                        print(spliteris)
                                        ISP=spliteris.split(", ")[0]
                                        valsts=output[-2:]
                                        d[IPs]={'ISPI':ISP, 'country': valsts}
        return d
