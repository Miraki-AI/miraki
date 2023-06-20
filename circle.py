CCI_API_TOKEN = "948630db8b4844fe0b558ed0bf81d368629b9d33"

import http.client

conn = http.client.HTTPSConnection("circleci.com")

headers = { 'authorization': f"Basic {CCI_API_TOKEN}" }

conn.request("GET", "/api/v2/pipeline", headers=headers)

res = conn.getresponse()
data = res.read()

print(data.decode("utf-8"))