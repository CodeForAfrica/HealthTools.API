.. HealthToolsApi documentation master file, created by
   sphinx-quickstart on Wed Sep 13 16:40:03 2017.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.
 
HealthTools.KE-api doc
=================================

HealthTools Kenya API to retrieve, structure and return data being used by the health tools. It provides data on the following medical officer registries:

* Doctors: http://medicalboard.co.ke/online-services/retention/
* Foreign doctors: http://medicalboard.co.ke/online-services/foreign-doctors-license-register
* Clinical officers: http://clinicalofficerscouncil.org/online-services/retention/

.. toctree::
   :maxdepth: 2

   telegram_bot
   utilities   
   views
   views_util



Indices and tables
==================
 
* :ref:`genindex` 
* :ref:`genindex` 
* :ref:`search`


Specifications
------------------
Specification for the API is shown below. It is an open api and requires no authentication to access.


.. list-table::
   :header-rows: 1

   * - EndPoint
     - Allowed Methods
     - Functionality
     - Parameters
   * - `/doctors/search.json`
     - GET
     - Search a doctor by the name 
     - q=[name]
   * - `/nurses/search.json`
     - GET
     - Search a nurse by the name 
     - q=[name]
   * - `/clinical-officers/search.json`
     - GET
     - Search a clinical officer by the name
     - q=[name]
  

Installation
------------
Clone the repo from github
``$ git clone git@github.com:RyanSept/HealthTools.KE-api.git``

Change directory into package ``$ cd HealthTools.KE-api``

Install the dependencies by running ``$ pip install -r requirements.txt``

Install Memcached
 * If on linux follow this `link <https://github.com/memcached/memcached/wiki/Install>`_
 * On mac use ``brew install memcached``

You can set the required environment variables like so

.. code:: bash

  $ export APP_DEBUG=<False> # True or False
  $ export MEMCACHED_URL=<memcache_url:port> # defaults to 127.0.0.1:8000
  $ export GA_TRACKING_ID=<google-analytics-tracking-id>
  $ export SMS_USER=<sms-provider-user-id>
  $ export SMS_PASS=<sms-provider-passcode>
  $ export SMS_SHORTCODE=<sms-provider-shortcode>
  $ export SMS_SEND_URL=<url-for-sms-provider>
  $ export AWS_ACCESS_KEY=<aws-access-key-id>
  $ export AWS_SECRET_KEY=<aws-secret-key>
  $ export ES_HOST=<elasticsearch_host_endpoint> (DO NOT SET THIS IF YOU WOULD LIKE TO USE ELASTIC SEARCH LOCALLY ON YOUR MACHINE)
  $ export ES_PORT=<elasticsearch_port>
  $ export ES_INDEX=<elasticsearch_index>


**If you want to use elasticsearch locally on your machine use the following instructions to set it up**

For linux and windows users, follow instructions from this `elastic <https://www.elastic.co/guide/en/elasticsearch/reference/current/setup.html>`_

For mac users run ``brew install elasticsearch`` on your terminal

Run memcached on your terminal ``$ memcached -p <port you set MEMCACHED_URL to run on>(default: 8000)``

If you set up elasticsearch locally run it ``$ elasticsearch``

You can now run the server ``$ python manage.py`` or ``gunicorn manage:app`` for production.



Running the tests
-----------------

Run memcached on your terminal ``$ memcached -p <port you set MEMCACHED_URL to run on>(default: 8000)``

.. note:: Make sure if you use elasticsearch locally, it's running.


Use nosetests to run tests (with stdout) like this:
``$ nosetests --nocapture``
