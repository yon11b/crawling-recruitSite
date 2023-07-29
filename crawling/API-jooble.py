import http.client

host = 'jooble.org'
key = '5e6ff65c-54bb-49c6-acf2-e7d53dc3cb55'

connection = http.client.HTTPConnection(host)
#request headers
headers = {"Content-type": "application/json"}
#json query
body = '{ "keywords": "it", "location": "Bern"}'
connection.request('POST','/api/' + key, body, headers)
response = connection.getresponse()
print(response.status, response.reason)
print(response.read())