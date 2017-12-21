# TokenRefresh - Java

## Syniverse Developer Community API token refresh utility

### Overview
This is a Java program that can be used to request the current token and validity time
and refresh the token when it expires.

### Files

|Filename           |Description                                        |
|-------------------|---------------------------------------------------|
|TokenRefresh.java|Java main class demonstrating a refresh.|
|pom.xml|Maven definition file.|


### Usage

The java source file and the pom.xml file can be used to generate a maven project.  The pom.xml file will provide the required library files.

Once compiled, the progam can then be run from a command line, with the following parameters provided in this order:

	consumer key
	consumer secret
	old (possibly expired) token
	the requested validity period

The main() method constructs a RefreshRequest object from the provided parameters, and calls the refresh method, passsing that object.  The 
refresh method will return a RefreshResponse object with the new token and remaining validity.


### Validity period Caveats

The validity period should not be shorter than 300 seconds, as there is time sync jitter compensation value added in the gateways to prevent token expiration errors in the event of a time 
synchronization problem between the gateway nodes.

### Error handling

Any errors encountered will result in an exception from the refresh method.
