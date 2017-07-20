import json
from django.http import HttpResponse


def jsonify(response, sort_keys=False):
    '''Serialize response to json format'''
    if sort_keys:
        return HttpResponse(json.dumps(response, indent=4, sort_keys=True), content_type='application/json')
    else:
        return HttpResponse(json.dumps(response, indent=4), content_type='application/json')