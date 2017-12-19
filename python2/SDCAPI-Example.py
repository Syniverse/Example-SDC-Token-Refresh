#!/usr/bin/python2

# Name: SDCToken-Example.py
# Purpose: Example useage of SDCToken library
#
#
# Fields:
# consumerkey - required - consumer key visible from SDC Application screens.
# consumersecret - required - consumer secret visible from SDC Application screens.
# oldtoken - required - an old token from the SDC Application screens.
# validity - optional - validity periods are in seconds.  Defaults to 3600 (1 hour).
#		0 set the token to never expire.
# 

import SDCToken
import urllib2
import time
import sys

def sdc_refresh(sdctoken,original_token,validity_period=None):
	# reset base url
	sdctoken.SDC_BASE_URL="https://beta-api.syniverse.com"
#	sdctoken.SDC_BASE_URL="https://beta.api.syniverse.com"
#	sdctoken.SDC_BASE_URL="https://betaapi.syniverse.com"

	try:
		sdctoken.refresh(original_token,validity_period)
	except urllib2.URLError as e:
		if hasattr(e,'code'):
			print('HTTP ' + e.code)
			print(''.join(e.readlines()))
		else:
			print('ERROR: ' + str(e))
			print(e)
		#endif
		exit()
	#endtry

	print("old token: " + original_token)
	print("new token: " + sdctoken.token)
	print("new validity: " + str(sdctoken.validity_period))
#enddef

def sdc_api_call(run,url):
	myreq=urllib2.Request(url,'{"Test":"This"}');
	myreq.add_header('Authorization','Bearer ' + my_sdc_token.token)
	myreq.add_header('Content-Type','application/json')
	myreq.add_header('Accept','application/json')

	try:
		myresp=urllib2.urlopen(myreq)
		print("Ran call " + str(run) + ": token: " + my_sdc_token.token + ", validity: " + str(my_sdc_token.validity_period) + ", response: " + ''.join(myresp.readlines()))
	except urllib2.URLError, e:
		if hasattr(e, 'code'):
			# check if the code is "unauth"... At which point we need to refresh the token.
			print(e)
			if e.code == 401:
				# Refresh the token
				sdc_refresh(my_sdc_token,my_sdc_token.token,my_validity_period)
				# Re-run the request.
				sdc_api_call(run,url)
			else:
				print("ERROR: " + str(e))
				print(e)
			#endif
		else:
			print("ERROR: " + str(e))
			print(e)
			exit()
		#endif
	except:
		print("ERROR: " + str(sys.exc_info()[0]))
		print(sys.exc_info()[:2])
		exit()
	#endtry
#enddef

my_consumer_key="hESRWCFBOMeuztNkWEqXmSOdQIAa"
my_consumer_secret="k9AV6fbWDkV2XW21_nk_gxef3RUa"
my_original_token="9a393ebeba33918a29941a7b64587195"
my_validity_period="600"
my_api_url="https://beta-api.syniverse.com/saop_mock/v1/hello/testpost-ntv"

my_sdc_token=SDCToken.SDCToken(my_consumer_key, my_consumer_secret)

sdc_refresh(my_sdc_token,my_original_token,my_validity_period)

loop_cntr=0

while loop_cntr<=100:
	sdc_api_call(loop_cntr,my_api_url)
	time.sleep(1)
	loop_cntr+=1;
#endwhile

