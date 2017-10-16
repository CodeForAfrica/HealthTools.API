[![Build Status](https://travis-ci.org/CodeForAfricaLabs/HealthTools.API.svg?branch=master)](https://travis-ci.org/CodeForAfricaLabs/HealthTools.API)

# HealthTools.API

_The HealthTools API. Providing actionable health information._

The HealthTools API provides a simple wrapper around Elasticsearch data being made available through the [HealthTools Scrapers](https://github.com/CodeForAfrica-SCRAPERS/healthtools_ke).

## Usage

| URL Endpoint                        | HTTP Methods |
|-------------------------------------|--------------|
| /search/doctors?q=<name>            | GET          |
| /search/doctors                     | GET          |
| /search/nurses?q=<name>             | GET          |
| /search/nurses                      | GET          |
| /search/clinical-officers?q=<name>  | GET          |
| /search/clinical-officers           | GET          |
| /search/health-facilities?q=<name>  | GET          |
| /search/health-facilities           | GET          |
| /search/nhif-outpatient?q=<name>    | GET          |
| /search/nhif-outpatient             | GET          |
| /search/nhif-outpatient-cs?q=<name> | GET          |
| /search/nhif-outpatient-cs          | GET          |
| /search/nhif-inpatient?q=<name>     | GET          |
| /search/nhif-inpatient              | GET          |
| /search?q=<query>                   | GET          |
| /wit_search?q=<query>               | GET          |


## Development

Clone the repo from github `$ git clone https://github.com/CodeForAfricaLabs/HealthTools.API.git`

Change directory into package `$ cd HealthTools.KE-api`

Install the dependencies by running `$ pip install -r requirements.txt`

?


### Tests

Use nosetests to run tests (with stdout) like this:
```$ nosetests --nocapture```


## Contributing

?

---

## License

?

