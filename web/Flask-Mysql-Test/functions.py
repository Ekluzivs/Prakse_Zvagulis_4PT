from flask import Flask
import re
import subprocess as su
#creates a pattern for whitespace
patterna=r"\s+"

def check(IPs):
	#this function checks if the data is a valid IPv4 address
	#splits each number in to their own element, then checks if it's less than 4 elements, after which it checks if it is a digit, then the range between 0 and 255
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
	#in this loop cycle, it removes all commas if exists and whitespaces
	IP=[I.strip() for I in IP.split(",")]
	d={}
	#the first if statement checks each IP address, if there exists IP addresses with a whitespace, then Error message will appear
	for IPs in IP:
		vai_ir=re.findall(patterna, IPs)
		if any(ir.isspace() for ir in vai_ir):
			d[IPs]={'ISPI':"Atstarpe eksistē starp divām vai vairākām ievadēm, lūdzu ievadiet komatu(s)", 'country': "N/A"}
		else:
			#gathers information from check function if the IP address is a valid IPv4 address
			checked=check(IPs)
			if checked==False:
				d[IPs]={'ISPI':"Nav derīga IPv4 adrese", 'country': "N/A"}
			else:
				#getwhois gathers ASN information from IPv4 address, whoispopen stores it in a "file" which then decodes it and reads the information
				#output variable replaces all the whoispopen variable with empty
				getwhois=['whois','-h','whois.cymru.com', IPs]
				whoispopen=su.Popen(getwhois, stdout=su.PIPE)
				whoispopen=whoispopen.stdout.read().decode('utf-8')
				output=whoispopen.replace("\n","")
				#Index then gathers the last 4 elements from the output, if "| NA exists in index variable, then No information has been gathered"
				index=output[-4:]
				if not output:
					d[IPs]={'ISPI':"Nav informācijas", 'country': "N/A"}
				elif "| NA" in index:
					d[IPs]={'ISPI':"Nav informācijas", 'country': "N/A"}
				else:
				#removes unnecessary stuff, for cleaner output, splitting the "| " into each element, but getting the information from the 3rd element
                                #ISP splits the comma of AS Name (*company name*, *country*) and gathers information from the first element, in this case company name
				#valsts gathers the last 2 characters from output for the country name
					output=output.replace("AS      | IP               | AS Name","")
					spliteris=output.split("| ")[2]
					ISP=spliteris.split(", ")[0]
					valsts=output[-2:]
					d[IPs]={'ISPI':ISP, 'country': valsts}
	return d

def dom_lookup(dom):
	dom_dict={}
	for doms in dom:
		vai_dom_ir=re.findall(patterna, doms)
		if any(ir_doms.isspace() for ir_doms in vai_dom_ir):
			dom_dict[doms]={'IP': "Atstarpe starp divām vai vairākām domēnām, lūdzu ievadiet komatu(s)", 'VT-LINK': "N/A"}
		else:
			getdomain=['dig','+short', doms]
			doms_popen=su.Popen(getdomain, stdout=su.PIPE)
			doms_popen=doms_popen.stdout.read().decode('utf-8')
			output=doms_popen.strip().split("\n")[0]
			print(output)
			if output == '':
				dom_dict[doms]={'IP':"Nav informācijas", 'VT-LINK': "N/A"}
			else:
				link=f"https://www.virustotal.com/gui/domain/{doms}"
				dom_dict[doms]={'IP': output, 'VT-LINK': link}
				print(dom_dict)
	return dom_dict
