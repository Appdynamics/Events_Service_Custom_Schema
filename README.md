# Synthetics_Events_Service
Example Python script running as a Synthetic Job that tests URL endpoints reporting metrics to the Events Data Store

A Python script was developed that:

1) Creates and deletes a custom schema from the command line
python eventsServiceTest.py deleteSchema schemaA
python eventsServiceTest.py createSchema schemaA

exampleSchema = { "schema": { "testid":"integer", "status_code":"integer", "status_code_s":"string", "response_time":   "integer", "url":"string", "mesid":"string” }  }

The string representation of status_code (\_s) allowed for the status_code to be used as Legend in dashboard charts.

2) Randomly select a URL from a list of URLs scoped for testing:

Example urlList = [ "https://customer.com/login", "https://customer.com/service1", "https://customer.com/service2” ]

3) Post the tested URL response time and status_code to the Events Data Store, either running the Python script from the command line or as a Synthetic Job.

statusCode, responseTime, testedUrl = getRequestURL( testURL )
data = [ {  "testid":random.randint( 1, 1000 ), "status_code":statusCode, "status_code_s":str( statusCode ),"response_time":responseTime, "url":testedUrl, "mesid":get_measurement_id() } ]
postCustomAnalytics( auth, data )

Reporting the tested URL to the Events Store allowed for a chart to be created showing the average response time for each URL in the test set, along with a legend showing the response code.

The script can run from the command line as follows:
python synthetics_events_service.py runtest1 schemaA

The full Python script is available at: https://github.com/APPDRYDER/Synthetics_Events_Service

The Events-API-AccountName and Events-API-Key are required for the script to authenticate with the Events Service and these can applied using environment variables or inline in the code when the script runs as a  Synthetics Job
