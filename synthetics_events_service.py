#
# Maintainer: David Ryder, David.Ryder@AppDynamics.com
#
# Executes a GET request to a URL and posts metrics to a custom
# schema in the AppDynamics Analytics Events Service using the
# Analytics Events API https://analytics.api.appdynamics.com
# Metrics posted include response_time and status_code from the GET request
#
# Runs from the command line for testing purposes, or as
# an Appdynamics Synthetic Agent custom script
# Command line options: runtest1, createCustomSchema, deleteSchema
#
import os
import sys
import requests
import datetime
import random
import json

def createHeaders( auth ):
    return { "X-Events-API-AccountName": auth['globalAccountName'],
             "X-Events-API-Key": auth['analyticsKey'],
             "Content-type": "application/vnd.appd.events+json;v=2"}

exampleSchema = { "schema": { "testid":           "integer",
                              "status_code":      "integer",
                              "status_code_s":    "string",
                              "response_time":    "integer",
                              "url":              "string",
                              "mesid":            "string" } }

def createCustomSchema( schema=exampleSchema, auth=[] ):
    r = requests.post( auth['endPoint'] + "/events/schema/" + auth['schemaName'],
                       data=json.dumps( schema ),
                       headers=createHeaders( auth ) )


def deleteCustomSchema( auth ):
    r = requests.delete( auth['endPoint'] + "/events/schema/" + auth['schemaName'],
                         headers=createHeaders( auth ) )


def postCustomAnalytics( auth, data ):
    r = requests.post( auth['endPoint'] + "/events/publish/" + auth['schemaName'],
                       data=json.dumps( data ),
                       headers=createHeaders( auth ))
    print( "Post metrics ", r.status_code, auth['schemaName'] )
    if r.status_code != 200:
        print( r.text )
        print( auth )

def getRequestURL( testUrl ):
    status_code = 0
    startTime = datetime.datetime.now()
    try:
        r = requests.get( testUrl )
        statusCode = r.status_code
    except Exception as e:
        print( "E ", e )
        statusCode = 503 # 503 Service Unavailable
    responseTime = int((datetime.datetime.now() - startTime).total_seconds() * 1000)
    print( "Test URL ", testUrl, statusCode )
    return int( statusCode ), responseTime, testUrl


def runTestCase1( auth, testURL ):
    statusCode, responseTime, testedUrl = getRequestURL( testURL )
    data = [ {  "testid":           random.randint( 1, 1000 ),
                "status_code":      statusCode,
                "status_code_s":    str( statusCode ),
                "response_time":    responseTime,
                "url":              testedUrl,
                "mesid":            get_measurement_id() } ]
    postCustomAnalytics( auth, data )

# List of URL endpoints to test GET request against
urlList = [ "https://google.com",
             "https://yahoo.com",
             "https://appdynamics.com",
             "https://google.com/TESTERROR" ]



testURL = urlList[ random.randint( 0, len(urlList)-1 ) ]

if "driver" not in dir(): # Execute as script from command line
    print( "Running as script")

    # Source authentication credentials from environment variables
    auth = { "endPoint":            os.environ.get('APPD_ANALYTICS_END_POINT'),
             "globalAccountName":   os.environ.get('APPD_GLOBAL_ACCOUNT_NAME'),
             "analyticsKey":        os.environ.get('APPD_ANALYTICS_KEY'),
             "schemaName":          "" }

    def get_measurement_id():
        return "U"

    cmd = sys.argv[1] if len(sys.argv) > 1 else "unknown command"
    if cmd == "runtest1": # runtest1 <schema name>
        auth['schemaName'] = sys.argv[2]
        runTestCase1( auth, testURL )

    elif cmd == "createSchema": # createSchema <schema name>
        auth['schemaName'] = sys.argv[2]
        createCustomSchema(auth=auth)

    elif cmd == "deleteSchema": # deleteSchema <schema name>
        auth['schemaName'] = sys.argv[2]
        deleteCustomSchema(auth=auth)

    else:
        print( "Commands: runtest1, createSchema, deleteSchema")

else: # Assume running within AppDynamics Synthetic Agent Framework
    print( "Running in AppDynamics Synthetic Agent Framework")

    # Custom Events Schema created in AppDynamics Analytics Events Store
    schemaName = "ddrtest3"
    # Source authentication credentials inline
    auth = { "endPoint":            "https://analytics.api.appdynamics.com",
             "globalAccountName":   "<APPD_GLOBAL_ACCOUNT_NAME>",
             "analyticsKey":        "<APPD_ACCESS_KEY>",
             "schemaName":          schemaName }

    def get_measurement_id():
        if (driver.capabilities.has_key('appdynamicsCapability')):
            if (driver.capabilities['appdynamicsCapability'].has_key('testId')):
                measurement_id = driver.capabilities['appdynamicsCapability']['testId']
        else:
            measurement_id = "UNDEFINED"
        return measurement_id

    runTestCase1( auth, testURL )
