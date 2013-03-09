#!/usr/bin/env python3

import json
import httplib2
from pprint import pprint

import urllib

class sapi(object):
	baseurl = ''

	username = ''
	token = ''

	validmethods = ['GET', 'PUT', 'POST', 'DELETE']

	def __init__(self):
		self.connection = httplib2.Http(disable_ssl_certificate_validation=True)
		
	def setCredentials(self, username, token, baseurl):
		self.connection.add_credentials(username, token)
		self.username = username
		self.token = token
		self.baseurl = baseurl

	def call(self, taxonomy, method = 'GET', data={}, parameters={}):
		if (method not in self.validmethods):
			self.error('Invalid HTTP-Method '+str(method), True)

		url = self.buildHttpQuery(taxonomy, parameters)
		response, content = self.connection.request(url, method, body=data)

		data = json.loads(content.decode('utf-8'))

		# Error handling
		if ('success' not in data):
			self.error('Invalid response')
			pprint(data)
			quit()
		elif (data['success'] is not True):
			self.error('API Request failed!')
			print(data['message'])
			quit()
		else:
			return data

	def get(self, url, params={}):
		return self.call(url, 'GET', parameters=params)

	def post(self, url, data={}, params={}):
		return self.call(url, 'POST', data, params)

	def put(self, url, data={}, params={}):
		return self.call(url, 'PUT', data, params)

	def delete(sekf, url, params={}):
		return self.call(url, 'DELETE', data, params)

	def error(self, message, exit=False):
		print('AN ERROR OCCURED:')
		print(message)
		if (exit):
			quit()

	def buildHttpQuery(self, taxonomy, parameters):
		url = self.baseurl + taxonomy;
		url_parts = list(urllib.parse.urlparse(url))
		query = dict(urllib.parse.parse_qsl(url_parts[4]))
		query.update(parameters)

		url_parts[4] = urllib.parse.urlencode(query)

		url =  urllib.parse.urlunparse(url_parts)
		return url