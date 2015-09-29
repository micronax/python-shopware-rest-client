#!/usr/bin/env python

import json
import httplib2
from pprint import pprint
import sys

import urllib
from urllib import urlencode
# TODO: urllib.parse.parse_qsl for python 3
from urlparse import urlparse, parse_qsl, urlunparse


class sapi(object):
    baseurl = ''

    username = ''
    token = ''

    debug = False

    validmethods = ['GET', 'PUT', 'POST', 'DELETE']

    def __init__(self):
        self.connection = httplib2.Http(disable_ssl_certificate_validation=True)

    def setCredentials(self, username, token, baseurl):
        self.connection.add_credentials(username, token)
        self.username = username
        self.token = token
        self.baseurl = baseurl

    def call(self, taxonomy, method='GET', data={}, parameters={}):
        if (method not in self.validmethods):
            self.error('Invalid HTTP-Method ' + str(method), True)

        url = self.buildHttpQuery(taxonomy, parameters)
        response, content = self.connection.request(url, method, body=json.dumps(data))

        if (response['status'] == '302'):
            # We have the special case that the call was successful, but no content was submitted, return true
            return True

        try:
            data = json.loads(content.decode('utf-8'))
        except:
            print(response)
            print()
            print(content)


        # Error handling
        if 'success' not in data:
            self.error('Invalid response')
            pprint(data)
            sys.exit(1)
        elif bool(data['success'] is not True):
            if self.debug:
                print(data['message'])
            return False
        else:
            if 'data' in data:
                return data['data']
            else:
                return True

    def get(self, url, data={}, params={}):
        return self.call(url, 'GET', parameters=params, data=data)

    def post(self, url, data={}, params={}):
        return self.call(url, 'POST', data, params)

    def put(self, url, data={}, params={}):
        return self.call(url, 'PUT', data, params)

    def delete(self, url, params={}):
        return self.call(url, 'DELETE', {}, params)

    def error(self, message, exit=False):
        print('AN ERROR OCCURED:')
        print(message)
        if (exit):
            sys.exit(1)

    def buildHttpQuery(self, taxonomy, parameters):
        url = self.baseurl + taxonomy;
        url_parts = list(urlparse(url))
        query = dict(parse_qsl(url_parts[4]))
        query.update(parameters)

        url_parts[4] = urlencode(query)

        url = urlunparse(url_parts)
        return url
