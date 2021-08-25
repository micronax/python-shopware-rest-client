=============
shopware_rest
=============


A Python REST Client for Shopware 5 (https://developers.shopware.com/developers-guide/rest-api/)


Usage
=====
.. code-block:: python

    from shopware_rest import rest
    client = rest.sapi()
    client.setCredentials('username', 'token', 'api_base_url')
    articles = client.get('articles/1')
    client.post('articles/1', {'name': 'New Article Name'})


Contribution
============
This is just an experimental release - Feel free to contribute your ideas and improvements using pull request


License
=======
Licensed under the MIT License (see LICENSE.txt)


Note
====
This project has been set up using PyScaffold 2.4.2. For details and usage
information on PyScaffold see http://pyscaffold.readthedocs.org/.
