## Gravity Integration Description
A very Basic Long Running Integration with a configurable listener that you can use to:
- Create a new incident
- Set the integration context
- Get the integration context
- Query an object (the object can be anything that the integration has access to)

I have also replicated the context set and get functions to two integration commands (gravity-set-context, gravity-get-context)

## To test the integration
You need to set these two headers in all your requests, and they have to match the integration settings:
- "X-App-ID"
- "X-App-Secret"

Below are some example requests:

### Set the integration context
curl --location --request POST 'https://192.168.20.20:200/context' \
--header 'X-App-ID: something' \
--header 'X-App-Secret: something' \
--header 'Content-Type: application/json' \
--data-raw '{
    "test":"test"
}'

### Get the integration context
curl --location --request GET 'https://192.168.20.20:200/context' \
--header 'X-App-ID: something' \
--header 'X-App-Secret: something' \

### Query the objects endpoint
curl --location --request GET 'https://192.168.20.20:200/objects?name=Cygnus%20X-3&type=black-hole' \
--header 'X-App-ID: something' \
--header 'X-App-Secret: something' \

### Create a new incident
curl --location --request POST 'https://192.168.20.20:200/incidents' \
--header 'X-App-ID: something' \
--header 'X-App-Secret: something' \
--header 'Content-Type: application/json' \
--data-raw '{
    "name":"Test Incident"
}'
