# gtdm-api
An API to expose a database, used to manage events.

# How to run
Install all dependencies first:
    `pip install -r requirements.txt`

You can then run app.py. This will create the database and start a local server.

# Using the API
The API supports 4 HTTP methods: GET, POST, PATCH and DELETE on two endpoints, /api/event and /api/type. The event endpoint is for managing events, while the type endpoint is for adding new event types.

POST, PATCH and DELETE require setting a header `'X-Secret-Key'` in the request, with the API key as value.

## GET:  
    `./api/event` will return all events  
    `./api/event/$id` will return the event with the specified id.  

## POST:  
A post request contains a JSON object and is posted to `./api/event`. Headers sent should always contain `'X-Secret-Key'` and `'Content-Type: application/json'`. The JSON object in the request should contain the following keys: type, name, location, host and time (as UNIX timestamp).

## PATCH:  
A PATCH request can be sent to update a specified event:  
    `./api/event/$id`  
    The request should look like the POST request, but not all keys need to be specified in the json, only the pieces that need to be updated.

## DELETE:  
A DELETE request removes the specified id:  
    `./api/event/$id`  
All it needs to contain is the 'X-Secret-Key' header.  

### Example POST via python requests:  
``` python
requests.post("./api/event", data=json.dumps({"type": 1, "name": "Test", "location": "Location", "host": "Host", "time": 0000000000}), headers={'content-type': 'application/json', 'X-Secret-Key': ''})
```

### Config file
Named config.ini. Looks like this:

```
[main]
secret = your key
```
