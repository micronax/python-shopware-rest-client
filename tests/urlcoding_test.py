# -*- coding: utf-8 -*-
from shopware_rest import sapi

client = sapi()
client.setCredentials(
    'username',
    'SOME_TOKEN',
    'http://localhost/shopware/api'
)

def test_buildHttpQuery():
    # use tox to make sure this works with python 2 and 3
    url = client.buildHttpQuery(taxonomy='/articles', parameters={})
    assert url == 'http://localhost/shopware/api/articles'
