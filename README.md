# HealthTools.KE-api
HealthTools Kenya API to retrieve, structure and return data being used by the health tools. It provides
data on the following medical officer registries anh health facilities: 

- Doctors: http://medicalboard.co.ke/online-services/retention/
- Foreign doctors: http://medicalboard.co.ke/online-services/foreign-doctors-license-register
- Clinical officers: http://clinicalofficerscouncil.org/online-services/retention/
- Health Facilities: http://kmhfl.health.go.ke
- NHIF accredited outpatient facilities for civil servants: http://www.nhif.or.ke/healthinsurance/medicalFacilities
- NHIF accredited inpatient facilities: http://www.nhif.or.ke/healthinsurance/inpatientServices
- NHIF accredited outpatient facilities: http://www.nhif.or.ke/healthinsurance/outpatientServices

### Specifications
Specification for the API is shown below. It is an open api and requires no authentication to access.


| EndPoint                            | Allowed Methods  | Functionality                                            | Parameters |
|-------------------------------------|------------------|----------------------------------------------------------|------------|
| `/doctors/search.json`              | GET              | Search a doctor by the name                              | q=[name]   |
| `/nurses/search.json`               | GET              | Search a nurse by the name                               | q=[name]   |
| `/clinical-officers/search.json`    | GET              | Search a clinical officer by the name                    | q=[name]   |
| `/health-facilities/search.json`    | GET              | Search a health facility by the name                     | q=[name]   |
| `/nhif/outpatient-cs/search.json`   | GET              | Search an nhif accredited outpatient facility for civil servants by name        | q=[name]   |
| `/nhif/outpatient/search.json`      | GET              | Search an nhif accredited outpatient facility for all kenyans by name    | q=[name]   |
| `/nhif/inpatient/search.json`       | GET              | Search an nhif accredited inpatient facility by name     | q=[name]   |


### Installation
Clone the repo from github `git@github.com:CodeForAfricaLabs/HealthTools.KE-api.git`

Change directory into package `$ cd HealthTools.KE-api`

Install the dependencies by running `$ pip install -r requirements.txt`

Install Memcached
 * If on linux follow this [link](https://github.com/memcached/memcached/wiki/Install)
 * On mac use `brew install memcached`

You can set the required environment variables like so
```<>
$ export APP_DEBUG=<False> # True or False
$ export MEMCACHED_URL=<memcache_url:port> # defaults to 127.0.0.1:8000
$ export GA_TRACKING_ID=<google-analytics-tracking-id>
$ export SMS_USER=<sms-provider-user-id>
$ export SMS_PASS=<sms-provider-passcode>
$ export SMS_SHORTCODE=<sms-provider-shortcode>
$ export SMS_SEND_URL=<url-for-sms-provider>
$ export AWS_ACCESS_KEY=<aws-access-key-id>
$ export AWS_SECRET_KEY=<aws-secret-key>
$ export ES_HOST=<elasticsearch_host_endpoint>  # Do not set this if you would like to use elastic search locally on your machine
$ export ES_PORT=<elasticsearch_port> # Do not set this if you would like to use elastic search default port 9200
$ export WEBHOOK_URL=<slack_webhook_url> # Do not set this if you don't want to post error messages on Slack
```
**If you want to use elasticsearch locally on your machine use the following instructions to set it up**

For linux and windows users, follow instructions from this [link](https://www.elastic.co/guide/en/elasticsearch/reference/current/setup.html)

For mac users run `brew install elasticsearch` on your terminal

**If you want to post messages on slack**

Set up `Incoming Webhooks` [here](https://slack.com/signin?redir=%2Fservices%2Fnew%2Fincoming-webhook) and set the global environment for the `WEBHOOK_URL`

Run memcached on your terminal `$ memcached -p <port you set MEMCACHED_URL to run on>(default: 11211)`

If you set up elasticsearch locally run it `$ elasticsearch`

You can now run the server `$ python manage.py runserver` or `gunicorn healthtools_api.wsgi` for production.



## Running the tests

Run memcached on your terminal `$ memcached -p <port you set MEMCACHED_URL to run on>(default: 11211)`

_**make sure if you use elasticsearch locally, it's running**_

Use nosetests to run tests (with stdout) like this:
```$ nosetests --nocapture```
