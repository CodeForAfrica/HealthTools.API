[![Build Status](https://travis-ci.org/CodeForAfricaLabs/HealthTools.API.svg?branch=master)](https://travis-ci.org/CodeForAfricaLabs/HealthTools.API)

# HealthTools.API

_Providing actionable health information._

The HealthTools API is a free to access, open, and structured service for newsrooms, civic organizations, and governments to access health information.

This API provides a simple wrapper around Elasticsearch data being made available through the [HealthTools Scraper](https://github.com/CodeForAfrica-SCRAPERS/healthtools_ke) and as a cached proxy for websites unable to be reliably scraped such as Kenya's nursing council website.

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

<!-- TODO: make the specifications a lot less by only listing the static endpoints -->

<!-- TODO: add standards we are using for API provision -->

## Requirments

<!-- TODO: Add requirements for the API to run e.g Elastic-->

---

## Development

To get started with developing on HealthTools.API, do the following:

```sh
$ git clone https://github.com/CodeForAfricaLabs/HealthTools.API.git`
$ cd HealthTools.API
$ pip install -r requirements.txt
```

### Configuration

TODO

### Run server

Finally run the Flask server:

```sh
$ python healthtools\manage.py
```

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

The following endpoint is used to run wit.ai on healthtools.API

| URL Endpoint | HTTP Method | Functionality | Parameter |
|--------------|-------------|---------------|-----------|
| /search/wit  | GET         | Search Query  | q=[query] |


## Contributing

?

---

## License

MIT License

Copyright (c) 2017 Code for Africa

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
