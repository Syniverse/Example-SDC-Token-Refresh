#!/usr/bin/python

# Name: SDCToken
# Purpose: object to handle token retreival/refresh for Syniverse Developer Community APIs.
#
# Example curl access
# curl -vks 'https://api.syniverse.com/saop-rest-data/v1/apptoken-refresh?consumerkey=<consumer_key>&consumersecret=<consumer_secret>&oldtoken=<original_token>&validity=<validity_period>'
#
# Fields:
# consumerkey - required - consumer key visible from SDC Application screens.
# consumersecret - required - consumer secret visible from SDC Application screens.
# oldtoken - required - an old token from the SDC Application screens.
# validity - optional - validity periods are in milliseconds.  Defaults to 3600000 (1 hour)
# 		0 sets a non-expring token.
# The validity returned by the refresh call will be either the length for a new token,
# or the remaining duration for an existing token.  If a valid active token exists, that token
# is the one that will be returned.

import sys

import urllib2
import json

class SDCToken():

	"""SDC Token utilities"""

	SDC_BASE_URL="https://api.syniverse.com"
	REFRESH_URI="/saop-rest-data/v1/apptoken-refresh"
	DEFAULT_VALIDITY_PERIOD=3600
	VALID_PARAMS=("consumer_key","consumer_secret","validity_period")
#	?consumerkey=" + consumer_key + "&consumersecret=" + consumer_secret + "&oldtoken=" + original_token + "&validity=" + validity_period

	token_refresh_headers = [(
		'Accept', 'application/json'
	)]

	def __init__(self, consumer_key=None, consumer_secret=None):
		self.DATA={}
		self.DATA['consumer_key']=consumer_key
		self.DATA['consumer_secret']=consumer_secret
		self.DATA['validity_period']=None
	#enddef

	def set(self, param=None, value=None):
		if param is None:
			raise(ValueError, "Parameter not specified")
		if param not in self.VALID_PARAMS:
			raise(ValueError, "Parameter not valid")
		self.DATA[param]=value
	#enddef

	def get(self, param=None):
		if param not in self.VALID_PARAMS:
			raise(ValueError, "Parameter not valid")
		return self.DATA[param]
	#enddef

	def refresh(self,token,validity_period=None):
		token_refresh_url=self.token_url(token,validity_period)

		req=urllib2.Request(token_refresh_url)
		req.add_header('Accept','application/json')

		response=urllib2.urlopen(req)

		try:
			response_json=json.loads(response.read(256))
		except:
			response_json['accessToken']=sys.exc_info()[0]
			response_json['validityTime']=sys.exc_info()[:2]
		#endtry
		self.token=response_json['accessToken']
		self.validity_period=response_json['validityTime']
	#enddef

	def token_url(self,token,validity_period=None):
		consumer_key=self.get('consumer_key')
		consumer_secret=self.get('consumer_secret')

		if consumer_key is None:
			raise(ValueError, "consumer_key is not set")
		if consumer_secret is None:
			raise(ValueError, "consumer_secret is not set")

		if validity_period is None:
			if self.validity_period is None:
				self.validity_period=self.DEFAULT_VALIDITY_PERIOD

			validity_period=self.validity_period

		return(self.SDC_BASE_URL + self.REFRESH_URI + "?consumerkey=" + consumer_key + "&consumersecret=" + consumer_secret + "&oldtoken=" + token + "&validity=" + str(validity_period))
#	?consumerkey=" + consumer_key + "&consumersecret=" + consumer_secret + "&oldtoken=" + original_token + "&validity=" + validity_period
	#enddef

	def get_token(self):
		return(self.token)
	#enddef

	def get_validity_period(self):
		return(self.validity_period)
	#enddef

#endclass
