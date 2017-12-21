#!/usr/bin/python2

"""SDCToken usage example

Example of using the SDCToken module to store the consumer key and consumer secret, and then refresh the token.

Fields:
consumerkey - required - consumer key visible from SDC Application screens.
consumersecret - required - consumer secret visible from SDC Application screens.
oldtoken - required - an old token from the SDC Application screens.
validity - optional - validity periods are in seconds.  Defaults to 3600 (1 hour).
	0 set the token to never expire.
"""



import SDCToken
import urllib2

consumer_key="<CONSUMER_KEY>"
consumer_secret="<CONSUMER_SECRET>"
original_token="<ORIGINAL_TOKEN>"
validity_period="600"

# Create our token object.
my_sdc_token=SDCToken.SDCToken(consumer_key, consumer_secret)

try:
	# Execute the refresh
	my_sdc_token.refresh(original_token)
except urllib2.URLError as e:
	# Handle any access-specific errors
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


