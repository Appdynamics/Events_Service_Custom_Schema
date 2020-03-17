# Synthetics_Events_Service
Example Python script running as a Synthetic Job that tests URL endpoints reporting metrics to the Events Store

The Python script creates a custom schema from the command line, examples:

```python eventsServiceTest.py deleteSchema schemaA```
```python eventsServiceTest.py createSchema schemaA```

Using the schemea: 
  ```exampleSchema = { "schema": { "testid":"integer", "status_code":"integer", "status_code_s":"string", "response_time":   "integer", "url":"string", "mesid":"string” }  }```

The string representation of status_code (\_s) allows for the status_code to be used as a Legend in dashboard charts.

For demonstration purposes the script randomly selects a URL from a list of URLs scoped for testing:

`Example urlList = [ "https://customer.com/login", "https://customer.com/service1", "https://customer.com/service2” ]`

And then posts the tested URL response time and status_code to the Events Data Store. Once the metrics are reported to the Events Store alerts can be enabled and dashboards created.

The Python script can be run from the command line or as a Synthetic Job. Run the script from the command line as follows:

```python synthetics_events_service.py runtest1 schemaA```

The full Python script is available here: [synthetics_events_service.py](https://github.com/APPDRYDER/Synthetics_Events_Service/blob/master/synthetics_events_service.py)

The `Events-API-AccountName` and `Events-API-Key` are required for the script to authenticate with the Events Service and these can applied using environment variables or inline in the code when the script runs as a  Synthetics Job
