[![Build Status](https://travis-ci.org/CodeForAfricaLabs/HealthTools.API.svg?branch=master)](https://travis-ci.org/CodeForAfricaLabs/HealthTools.API)

# HealthTools.API

_The HealthTools API. Providing actionable health information._

The HealthTools API provides a simple wrapper around Elasticsearch data being made available through the [HealthTools Scrapers](https://github.com/CodeForAfrica-SCRAPERS/healthtools_ke).

## Usage

Specification for the API are:


| URL Endpoint               | HTTP  Methods | Functionality                                                          | Parameters                |
|----------------------------|---------------|------------------------------------------------------------------------|---------------------------|
| /search/doctors            | GET           | Search a doctor by the name                                            | q=[name]                  |
| /search/nurses             | GET           | Search a nurse by the name                                             | q=[name]                  |
| /search/clinical-officers  | GET           | Search a clinical officer by the name                                  | q=[name]                  |
| /search/health-facilities  | GET           | Search a health facility by the name                                   | q=[name]                  |
| /search/nhif-outpatient    | GET           | Search a NHIF accredited outpatient facility by the name               | q=[name]                  |
| /search/nhif-outpatient-cs | GET           | Search a NHIF accredited outpatient  facility for civil servants       | q=[name]                  |
| /search/nhif-inpatient     | GET           | Search a NHIF accredited inpatient facility by the name                | q=[name]                  |
| /search                    | GET           | Search a query that contains a keyword Eg. HF Kitale                   | q=[query]                 |
| /sms                       | GET           | Search a query received from sms Eg. Dr Jane                           | q=[phoneNumber,  message] |
| /sms/[adapter]             | GET           | Search a query received from sms using the specified adapter Eg. mtech | q=[query]                 |

## Development

Clone the repo from github `$ git clone https://github.com/CodeForAfricaLabs/HealthTools.API.git`

Change directory into package `$ cd HealthTools.API`

Install the dependencies by running `$ pip install -r requirements.txt`

Run the server by running `$ python healthtools\manage.py runserver`

### Tests

Use nosetests to run tests (with stdout) like so:

```
$ nosetests --nocapture
$ nosetests healthtools/tests
$ nosetests healthtools/tests/doctor.py
$ nosetests healthtools/tests/nurse.py
$ nosetests healthtools/tests/clinical_officer.py
$ nosetests healthtools/tests/health_facilities.py
$ nosetests healthtools/tests/nhif_inpatient.py
$ nosetests healthtools/tests/nhif_outpatient.py
$ nosetests healthtools/tests/nhif_outpatient_cs.py
```

## Contributing

?

---

## License

?

