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
## Wit.ai
Wit.ai is a simple natural language processing API that helps developers turn speech and text into actionable data. In healthtools.API, we use it to distinguish the doc_type and the query param from the parameters being sent to the API. 
For example: `dr mary`

```
{
    "msg_id": "0csXmLxhRzgowQFJI",
    "_text": "dr mary",
    "entities": {
        "doctors": [
            {
                "confidence": 0.96676127393653,
                "value": "dr",
                "type": "value"
            }
        ],
        "query": [
            {
                "suggested": true,
                "confidence": 0.99538476989175,
                "value": "mary",
                "type": "value"
            }
        ]
    }
}
```
The doc_type has been identified as `doctors` and `mary` has been identified as query param.
To configure wit.ai:
- Sign up on wit.ai website with either your github or facebook account
- Create an app with the name you prefer to use.
- Detect your first entities:

![Alt text](images/teach.gif?raw=true "Title")   

Improve the detection

This will be done by continuously training your app to identify keyword or sentences. Input a message and check its prediction, if wrong, correct it if right validate it. 

![Alt text](images/training.gif?raw=true "Title")

Configure Server Access Token in the ENV.

The token can be found from the settings tab, API details segment.
![Alt text](images/at.png?raw=true "Title")

To set it in the ENV, run  `export WIT_ACCESS_TOKEN='Token'`

The following endpoint is used to run wit.ai on healthrools.API

| URL Endpoint | HTTP Method | Functionality | Parameter |
|--------------|-------------|---------------|-----------|
| /search/wit  | GET         | Search Query  | q=[query] |


## Contributing

?

---

## License

?

