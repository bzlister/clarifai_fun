import http.client, urllib.parse, json
from urllib import request
import webbrowser
from clarifai import rest
from clarifai.rest import ClarifaiApp
from apiclient.discovery import build
import time
import random

relatibility = 0

def setup(numRuns, seed):
	f=open("api_keys.txt", "r")
	clarifai_key = f.readline().strip()
	developer_key = f.readline().strip()
	c_x = f.readline().strip()
	f.close()
	app = ClarifaiApp(api_key=clarifai_key)
	model = app.models.get('general-v1.3')
	service = build("customsearch", "v1",developerKey=developer_key)
	time.sleep(1)
	for i in range(0, numRuns):
		seed = getAttributes(model, service, seed, c_x)
	print("Done")

def getAttributes(model, service, query, c_x):
	res = service.cse().list(q=query, cx=c_x,  num=10, searchType="image", fileType="jpg").execute()
	retUrl = res['items'][random.randint(0,9)]['link']
	time.sleep(1)
	webbrowser.open_new(retUrl)
	s = ""
	data = model.predict_by_url(url=retUrl)['outputs'][0]['data']['concepts']
	for i in range (relatibility, relatibility+5):
		s = s + data[i]['name'] +" "
	if "no person" in s:
		s = s.replace("no person ", "")
	print(s)
	return s
