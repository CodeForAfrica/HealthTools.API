[![Build Status](https://travis-ci.org/CodeForAfricaLabs/HealthTools.API.svg?branch=master)](https://travis-ci.org/CodeForAfricaLabs/HealthTools.API)

# HealthTools.API

_The HealthTools API. Providing actionable health information._

The HealthTools API provides a simple wrapper around Elasticsearch data being made available through the [HealthTools Scrapers](https://github.com/CodeForAfrica-SCRAPERS/healthtools_ke).

## Usage

?

## Development

Clone the repo from github `$ git clone https://github.com/CodeForAfricaLabs/HealthTools.API.git`

Change directory into package `$ cd HealthTools.KE-api`

Install the dependencies by running `$ pip install -r requirements.txt`

?

### Tests

Use nosetests to run tests (with stdout) like so:

```sh
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

