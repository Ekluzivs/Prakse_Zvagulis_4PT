from flask import Flask
import requests as req
import re
import subprocess as su
import validators
import json
#creates a pattern for whitespace
patterna="\s+"
# Function group used for checking whether or not the data the user has inputted is valid
def check_dom(doms):
	#using regex pattern, checking whether or not the domain is correctly written
	#False: hyphen at the beginning or end of domain, more than 63 characters
	reg_pat="^((?!-)[A-Za-z0-9-]"+"{1,63}(?<!-)\\.)"+"[A-Za-z]{2,6}"
	if len(doms) > 64:
		return False
	#validator checks for trailing dots and underscores, can't identify sub-domains
	elif(re.search(reg_pat, doms)) and validators.domain(doms):
		return True
	else:
		return False

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

def hash_lookup(hash):
	hash=[I.strip() for I in hash.split(",")]
	hash_dict={}
	flagged_Hash=[]
	for hashs in hash:
		vai_hash_ir=re.findall(patterna, hashs)
		if any(hash_ir.isspace() for hash_ir in vai_hash_ir):
#			hash_dict[hashs]={'drosiba': 'Atstarpe eksistē starp divām vai vairākām ievadēm, lūdzu ievadiet komatu(s)', 'VT_hash': "N/A"}
			flagged_Hash.append(hashs)
			continue
		elif len(hashs) != 32 and len(hashs) != 40 and len(hashs) != 64:
#			hash_dict[hashs]={'drosiba': 'Ievade nav jaucējvērtība (MD5, SHA-1, SHA-256)', 'VT_hash': "N/A"}
			flagged_Hash.append(hashs)
			continue
		else:
			url_hyper="https://www.virustotal.com/gui/file/"+hashs
			url="https://www.virustotal.com/api/v3/files/"+hashs
			headers={
				"accept": "application/json",
				"x-apikey": "001e6e4cca586655d6f9e36dcb8338115c61f47e39a48fbea08500ddefd25035"
			}
			get_data=req.get(url, headers=headers)
			data=get_data.json()
			if re.search("NotFoundError", get_data.text) or re.search("BadRequestError", get_data.text):
				hash_dict[hashs]={'drosiba': "Nav informācijas", 'VT_hash': "N\A"}
			else:
				malicious=data["data"]["attributes"]["last_analysis_stats"]["malicious"]
				if malicious > 0:
					hash_dict[hashs]={'drosiba': "Jaucējvērtība nav droša", 'VT_hash': url_hyper}
				else:
					hash_dict[hashs]={'drosiba': "Jaucējvērtība ir droša", 'VT_hash': url_hyper}
	return hash_dict, flagged_Hash


def lookup(IP):
	#in this loop cycle, it removes all commas if exists and whitespaces
	IP=[I.strip() for I in IP.split(",")]
	d={}
	flagged_IP=[]
	#the first if statement checks each IP address, if there exists IP addresses with a whitespace, then Error message will appear
	for IPs in IP:
		print(IPs)
		vai_ir=re.findall(patterna, IPs)
		if any(ir.isspace() for ir in vai_ir):
#			d[IPs]={'ISPI':"Atstarpe eksistē starp divām vai vairākām ievadēm, lūdzu ievadiet komatu(s)", 'country': "N/A"}
			flagged_IP.append(IPs)
			continue
		else:
			#gathers information from check function if the IP address is a valid IPv4 address
			checked=check(IPs)
			if checked==False:
#				d[IPs]={'ISPI':"Nav derīga IPv4 adrese", 'country': "N/A"}
				flagged_IP.append(IPs)
				continue
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
	return d, flagged_IP

def dom_lookup(dom):
	dom=[I.strip() for I in dom.split(",")]
	dom_dict={}
	flagged_Dom=[]
	for doms in dom:
		vai_dom_ir=re.findall(patterna, doms)
		if any(ir_doms.isspace() for ir_doms in vai_dom_ir):
#			dom_dict[doms]={'IP': "Atstarpe starp divām vai vairākām domēnām, lūdzu ievadiet komatu(s)", 'VT-LINK': "N/A"}
			flagged_Dom.append(doms)
		else:
			checked_dom=check_dom(doms)
			if checked_dom == False:
#				dom_dict[doms]={'IP':"Nav derīga domēnu adrese", 'VT-LINK': "N/A"}
				flagged_Dom.append(doms)
			else:
				getdomain=['dig','+short', doms]
				doms_popen=su.Popen(getdomain, stdout=su.PIPE)
				doms_popen=doms_popen.stdout.read().decode('utf-8')
				output=doms_popen.strip().split("\n")[0]
				if output == '':
					dom_dict[doms]={'IP':"Nav informācijas", 'VT-LINK': "N/A"}
				else:
					link="https://www.virustotal.com/gui/domain/"+doms
					dom_dict[doms]={'IP': output, 'VT-LINK': link}
	return dom_dict, flagged_Dom
