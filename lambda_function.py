from healthtools_api.nurses_api import find_nurse


def lambda_handler(event, context):
    query = event["query"]
    return find_nurse(query)
