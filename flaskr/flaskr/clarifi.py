import http.client, urllib.parse, json
from urllib import request
import webbrowser
import clarifai
from clarifai import rest
from clarifai.rest import ClarifaiApp
from apiclient.discovery import build
from flask import Flask
import time
import random

c_x = "009171367015975864750:tzgp6vvag9k"
def imageSearch(text, numRuns, relatibility):
	seed = text
	f=open("C:/Users/bzlis/api_keys.txt", "r")
	clarifai_key = f.readline().strip()
	developer_key = f.readline().strip()
	c_x = f.readline().strip()
	f.close()
	app = ClarifaiApp(api_key=clarifai_key)
	model = app.models.get('general-v1.3')
	service = build("customsearch", "v1",developerKey=developer_key)
	lastImage = ''
	for i in range(0, numRuns):
		attr = getAttributes(model, service, seed, relatibility)
		seed = attr['s']
		lastImage = attr['img']
	return {'lastImage': lastImage, 'seed': seed}
		

def getAttributes(model, service, query, relatibility):
	time.sleep(0.1)
	res = service.cse().list(q=query, cx=c_x,  num=1, searchType="image").execute()
	retUrl = res['items'][0]['link']
	s = ""
	data = None
	while (data == None):
		try:
			data = model.predict_by_url(url=retUrl)['outputs'][0]['data']['concepts']
		except clarifai.errors.ApiError:
			res = service.cse().list(q=query, cx=c_x,  num=10, searchType="image").execute()
			retUrl = res['items'][random.randint(0,9)]['link']
	for i in range (relatibility, relatibility+5):
		s = s + data[i]['name'] +" "
	if "no person" in s:
		s = s.replace("no person ", "")
	print(s)

	return {'s': s, 'img': retUrl}