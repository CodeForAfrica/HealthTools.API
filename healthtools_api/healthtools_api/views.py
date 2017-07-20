import json
from django.http import HttpResponse


def index(request):
    '''Landing Endpoint'''
    msg = {
        "name": "HealthTools.KE-API",
        "authentication": [],
        "endpoints": {
            "/nurses": {"methods": ["GET"]},
            "/doctors": {"methods": ["GET"]},
            "/clinical-officers": {"methods": ["GET"]},
            "/nhif": {"methods": ["GET"]}
        }
    }
    return HttpResponse(json.dumps(msg, indent=4, sort_keys=True), content_type='application/json')
