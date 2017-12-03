import http.client, urllib.parse, json
from urllib import request
import webbrowser
from clarifai import rest
from clarifai.rest import ClarifaiApp
import time

def setup(numRuns, seed, relatibility):
	subscriptionKey = "b52c235a432e4bf193934695fbe2db1f"
	host = "api.cognitive.microsoft.com"
	headers = {'Ocp-Apim-Subscription-Key': subscriptionKey}
	conn = http.client.HTTPSConnection(host)
	app = ClarifaiApp(api_key="c2cd1be48fc64640b485e9185accffce")
	model = app.models.get('general-v1.3')
	for i in range(0, numRuns):
		seed = getAttributes(model, seed, headers, conn, relatibility)
	print("Done")

def getAttributes(model, urlName, headers, conn, relatibility):
	s = ""
	data = model.predict_by_url(url=urlName)['outputs'][0]['data']['concepts']
	for i in range (relatibility, relatibility+5):
		s = s + data[i]['name'] +" "
	if "no person" in s:
		s = s.replace("no person ", "")
	print(s)
	path = "/bing/v7.0/images/search"
	term = "Microsoft Cognitive Services"

	query = urllib.parse.quote(s)
	conn.request("GET", path + "?q=" + query, headers=headers)
	time.sleep(1)
	response = conn.getresponse()
	headers = [k + ": " + v for (k, v) in response.getheaders() if k.startswith("BingAPIs-") or k.startswith("X-MSEdge-")]
	w = json.loads(response.read().decode("utf8"))['value'][0]['contentUrl']
	
	webbrowser.open_new(w)
	return w;