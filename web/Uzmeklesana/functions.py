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
	#splits any inputs from the comma to be each element (input: abc,dcb to ['abc','dcb']) and removes any whitespace in the element
	hash=[I.strip() for I in hash.split(",")]
	hash_dict={}
	flagged_Hash=[]
	#over each iteration, the vai_hash_ir checks for any whitespace in the input
	for hashs in hash:
		vai_hash_ir=re.findall(patterna, hashs)
		#checks if any whitespace has been found by the check, if true, it gets flagged and a new iteration starts
		if any(hash_ir.isspace() for hash_ir in vai_hash_ir):
			flagged_Hash.append(hashs)
			continue
		#Since hash is being checked, 32 is MD5, 40 is SHA-1 and 64 is SHA-256, if they're less or more than specified, it gets flagged
		elif len(hashs) != 32 and len(hashs) != 40 and len(hashs) != 64:
			flagged_Hash.append(hashs)
			continue
		#if all is well, create a variable that creates the API request
		else:
			url_hyper="https://www.virustotal.com/gui/file/"+hashs
			url="https://www.virustotal.com/api/v3/files/"+hashs
			headers={
				"accept": "application/json",
				"x-apikey": "001e6e4cca586655d6f9e36dcb8338115c61f47e39a48fbea08500ddefd25035"
			}
			#sends data to the service using API request, gathering information in JSON format
			get_data=req.get(url, headers=headers)
			data=get_data.json()
			#if any error has been found or bad request, then it'll print out that no information has been found
			if re.search("NotFoundError", get_data.text) or re.search("BadRequestError", get_data.text):
				hash_dict[hashs]={'drosiba': "Nav informācijas", 'VT_hash': "N\A"}
			else:
				#malicious gathers the data from the json format and then checks if there is more than one malicious in the hash
				malicious=data["data"]["attributes"]["last_analysis_stats"]["malicious"]
				if malicious > 0:
					hash_dict[hashs]={'drosiba': "Jaucējvērtība nav droša", 'VT_hash': url_hyper}
				else:
					hash_dict[hashs]={'drosiba': "Jaucējvērtība ir droša", 'VT_hash': url_hyper}
	return hash_dict, flagged_Hash

def IPs_lookup(IP_safe):
	#this line first splits values into each element that has a comma (example: 1.1.1.1, 2.2.2.2 to ['1.1.1.1','2.2.2.2']) and removes any whitespace in the elements
	IP_safe=[I.strip() for I in IP_safe.split(",")]
	IP_dict={}
	flagged_IP_s=[]
	#over each iteration it assigns a new variable with an IP address and checks if the element has any whitespace
	for IPss in IP_safe:
		IPs=IPss
		vai_IPss_ir=re.findall(patterna, IPss)
		#if whitespace has been detected, it gets flagged and new iterations starts
		if any(IP_ir.isspace() for IP_ir in vai_IPss_ir):
			flagged_IP_s.append(IPss)
			continue
		else:
			#sends the IP address to another function that verifies if the IP address is an IPv4 address, if False, it gets flagged and new iteration starts
			checked=check(IPs)
			if checked==False:
				flagged_IP_s.append(IPss)
				continue
			else:
				#creates an API request
				url_hyper="https://www.virustotal.com/gui/file/"+IPss
				url="https://www.virustotal.com/api/v3/ip_addresses/"+IPss
				headers={
					"accept": "application/json",
					"x-apikey": "001e6e4cca586655d6f9e36dcb8338115c61f47e39a48fbea08500ddefd25035"
				}
				#once the connection has been made, it sends the API request for the information and back-end receives it as json format
				get_data=req.get(url, headers=headers)
				data=get_data.json()
				#using regex, it finds if checks whether the data received has any errors, if error has been found, it prints out that it has no information
				if re.search("NotFoundError", get_data.text) or re.search("BadRequestError", get_data.text):
					IP_dict[IPss]={'IP_issafe': "Nav informācijas", 'VT_IP': "N\A"}
				else:
					#checks whether the IP is malicious by checking the count, if there's at least one instance of malicious, then it is likely not safe
					malicious=data["data"]["attributes"]["last_analysis_stats"]["malicious"]
					if malicious > 0:
						IP_dict[IPss]={'IP_issafe': "IP adrese, iespējams, nav droša", 'VT_IP': url_hyper}
					else:
						IP_dict[IPss]={'IP_issafe': "IP adrese ir droša", 'VT_IP': url_hyper}
	return IP_dict, flagged_IP_s


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
			flagged_IP.append(IPs)
			continue
		else:
			#gathers information from check function if the IP address is a valid IPv4 address
			checked=check(IPs)
			if checked==False:
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
	#splits domain into each element by splitting the commas (example input: delfi.lv, github.com to ['delfi.lv','github.com']) and removes any whitespace in the element
	dom=[I.strip() for I in dom.split(",")]
	dom_dict={}
	flagged_Dom=[]
	#over each new iteration, it checks whether the element has a whitespace
	for doms in dom:
		vai_dom_ir=re.findall(patterna, doms)
		#if the element contains a whitespace, it flags it and starts a new iteration
		if any(ir_doms.isspace() for ir_doms in vai_dom_ir):
			flagged_Dom.append(doms)
			continue
		else:
			#checks whether it is a domain, if false, it flags it and starts a new iteration
			checked_dom=check_dom(doms)
			if checked_dom == False:
				flagged_Dom.append(doms)
			else:
				#this uses a linux command line called "dig", it digs up the information about the domain, but making the output easier,
				#+short flag is entered, only outputting IP address from the inputting domain
				#after information about domain is gathered, it then puts that information in a "file" and then is read and decoded to utf-8
				#since there can be multiple outputs and duplicates, the first IP address that is outputted is selected
				getdomain=['dig','+short', doms]
				doms_popen=su.Popen(getdomain, stdout=su.PIPE)
				doms_popen=doms_popen.stdout.read().decode('utf-8')
				output=doms_popen.strip().split("\n")[0]
				#if the output is empty, means that there is no information about this domain
				if output == '':
					dom_dict[doms]={'IP':"Nav informācijas", 'VT-LINK': "N/A"}
				else:
					link="https://www.virustotal.com/gui/domain/"+doms
					dom_dict[doms]={'IP': output, 'VT-LINK': link}
	return dom_dict, flagged_Dom
