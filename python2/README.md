# SDCToken - python 2 module

## Syniverse Developer Community API token refresh utility

### Overview
This is a python2 module that can be used to request the current token and validity time
and refresh the token when it expires.

### Files

|Filename           |Description                                        |
|-------------------|---------------------------------------------------|
|SDCToken.py        |Token module containing the SDCToken class.        |
|SDCToken-Example.py|Example using the SDCToken class to refresh a token.|
|SDCAPI-Example.py  |Example calling a SDC API and automatically refreshing the token when it expires.|

### SDCToken module usage

To use the module, place it into the base of your project and import it:

	`import SDCToken`

Once imported, create a new token object:

	`my_sdc_token=SDCToken.SDCToken()`

Supplying the consumer key and consumer secret are not required at this stage, however are required
for the fresh.  To set them after creating the token object above:

	`my_sdc_token.set("consumer_key","my_key")`
	`my_sdc_token.set("consumer_secret","my_secret")`

Or to set them at the same time as the object creation:

	`my_sdc_token=SDCToken.SDCToken("my_key","my_secret")`


Refreshing the token is as follows:

	`my_sdc_token.refresh("my_old_token")`


### Defaults

The conusmer key and consumer secret default to `None`.  If they are not set, the refresh is going to fail.

The validity period defaults to 1 hour (3600 seconds).  It can be changed during the token refresh call:

	`my_sdc_token.refresh("my_old_token",validity_period)`
    

### Validity period Caveats

The validity period should not be shorter than 300 seconds, as there is time sync jitter compensation value added in the gateways to prevent token expiration errors in the event of a time 
synchronization problem between the gateway nodes.

### Error handling

##### HTTP/connectivity

The `refresh` function will return `urllib2` exceptions in the event of a connectivity error.  As such, it is recommended to `import urllib2` and wrap the call in a `try:/catch urllib2.URLError` block.

##### Json error

Any issues with the json content received from token refresh will result in the token and validity time fields being populated with the json error.   An exception is not generated.

