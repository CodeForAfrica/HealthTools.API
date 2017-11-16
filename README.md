# HealthTools.API

The HealthTools API provides a simple wrapper around Elasticsearch data being made available through the [HealthTools Scrapers](https://github.com/CodeForAfrica-SCRAPERS/healthtools_ke).

Through the API you can access data that we've scraped from:

1. Doctors: http://medicalboard.co.ke/online-services/retention/
2. Foreign Doctors: http://medicalboard.co.ke/online-services/foreign-doctors-license-register
3. Clinical Officers: http://clinicalofficerscouncil.org/online-services/retention/
4. Health Facilities: http://kmhfl.health.go.ke
5. NHIF accredited outpatient facilities for civil servants: http://www.nhif.or.ke/healthinsurance/medicalFacilities
6. NHIF accredited inpatient facilities: http://www.nhif.or.ke/healthinsurance/inpatientServices
7. NHIF accredited outpatient facilities: http://www.nhif.or.ke/healthinsurance/outpatientServices


## Usage

To use the HealthTools.API, checkout our API docs here:

    https://healthtools.codeforafrica.org


## Development

HealthTools.API is a simple [Flask app](http://flask.pocoo.org) that you can set up by following these steps:

```
$ git clone https://github.com/CodeForAfricaLabs/HealthTools.API.git
$ cd HealthTools.API
$ python setup.py develop
```

Once done, you can run the Flask app server:

```
$ python healthtools/manage.py runserver
```


### Tests

Use nosetests to run tests (with stdout) like this:
```$ nosetests --nocapture```


## Contributing

If you'd like to contribute to HealthTools.API, check out the [CONTRIBUTING.md](CONTRIBUTING.md) file on how to get started. 

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
