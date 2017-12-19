#!/usr/bin/python
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

consumer_key="hESRWCFBOMeuztNkWEqXmSOdQIAa"
consumer_secret="k9AV6fbWDkV2XW21_nk_gxef3RUa"
original_token="9a393ebeba33918a29941a7b64587195"
validity_period="0"

my_sdc_token=SDCToken.SDCToken(consumer_key, consumer_secret)

# reset base url
my_sdc_token.SDC_BASE_URL="https://beta-api.syniverse.com"
#my_sdc_token.SDC_BASE_URL="https://beta.api.syniverse.com"
#my_sdc_token.SDC_BASE_URL="https://betaapi.syniverse.com"

try:
	my_sdc_token.refresh(original_token)
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
print("new token: " + my_sdc_token.token)
print("new validity: " + str(my_sdc_token.validity_period))


