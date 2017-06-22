# HealthTools.KE-api
HealthTools Kenya API to retrieve, structure and return data being used by the health tools. It provides
data on the following medical officer registries: 

- Doctors: http://medicalboard.co.ke/online-services/retention/
- Foreign doctors: http://medicalboard.co.ke/online-services/foreign-doctors-license-register
- Clinical officers: http://clinicalofficerscouncil.org/online-services/retention/

### Specifications
Specification for the API is shown below. It is an open api and requires no authentication to access.


| EndPoint                            | Allowed Methods  | Functionality                                            | Parameters |
|-------------------------------------|------------------|----------------------------------------------------------|------------|
| `/doctors/search.json`              | GET              | Search a doctor by the name                              | q=[name]   |
| `/nurses/search.json`               | GET              | Search a nurse by the name                               | q=[name]   |
| `/clinical-officers/search.json`    | GET              | Search a clinical officer by the name                    | q=[name]   |


### Installation
Clone the repo from github `$ git clone git@github.com:RyanSept/HealthTools.KE-api.git`

Change directory into package `$ cd HealthTools.KE-api`

Install the dependencies by running `$ pip install requirements.txt`

Install Memcached
 * If on linux follow this [link](https://github.com/memcached/memcached/wiki/Install)
 * On mac use `brew install memcached`

You can set the required environment variables like so
```<>
$ export MEMCACHED_URL=<memcache_url:port> # defaults to 127.0.0.1:8000
$ export GA_TRACKING_ID=<google-analytics-tracking-id>
$ export SMS_USER=<sms-provider-user-id>
$ export SMS_PASS=<sms-provider-passcode>
$ export SMS_SHORTCODE=<sms-provider-shortcode>
$ export SMS_SEND_URL=<url-for-sms-provider>
$ export CONFIG=<config-mode>  # eg. "healthtools_ke_api.settings.DevConfig"
$ export AWS_ACCESS_KEY_ID=<aws-access-key-id>
$ export AWS_SECRET_KEY=<aws-secret-key>
$ export AWS_REGION=<aws-region>
$ export ES_HOST=<elasticsearch_host_endpoint> (DO NOT SET THIS IF YOU WOULD LIKE TO USE ELASTIC SEARCH LOCALLY ON YOUR MACHINE)
```
**If you want to use elasticsearch locally on your machine use the following instructions to set it up**

For linux and windows users, follow instructions from this [link](https://www.elastic.co/guide/en/elasticsearch/reference/current/setup.html)

For mac users run `brew install elasticsearch` on your terminal

Run memcached on your terminal `$ memcached -p <port you set MEMCACHED_URL to run on>(default: 8000)`

If you set up elasticsearch locally run it `$ elasticsearch`

You can now run the server `$ python manage.py` or `gunicorn manage:app` for production.



## Running the tests

Run memcached on your terminal `$ memcached -p <port you set MEMCACHED_URL to run on>(default: 8000)`

_**make sure if you use elasticsearch locally, it's running**_

Use nosetests to run tests (with stdout) like this:
```$ nosetests --nocapture```