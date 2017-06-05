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

You can set the required environment variables like so
```<>
$ export GA_TRACKING_ID=<google-analytics-tracking-id>
$ export SMS_USER=<sms-provider-user-id>
$ export SMS_PASS=<sms-provider-passcode>
$ export SMS_SHORTCODE=<sms-provider-shortcode>
$ export SMS_SEND_URL=<url-for-sms-provider>
$ export CONFIG=<config-mode>  # eg. "healthtools_ke_api.settings.DevConfig"
$ export AWS_ACCESS_KEY_ID=<aws-access-key-id>
$ export AWS_SECRET_KEY=<aws-secret-key>
$ export AWS_REGION="<aws-region>
```

You can now run the server `$ python manage.py` or `gunicorn manage:app` for production.


## Running the tests

Use nosetests to run tests (with stdout) like this:
```$ nosetests --nocapture```