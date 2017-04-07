from healthtools_api.nurses_api import find_nurse


def search_nurse(event, context):
    query = event["query"]
    return find_nurse(query)
