import getpass
import json
import requests
from datetime import datetime

from ..settings import SLACK


def print_error(message):
    """
    print error messages in the terminal
    if slack webhook is set up, post the errors to slack
    """
    print("[{0}] - ".format(datetime.now().strftime("%Y-%m-%d %H:%M:%S")) + message)
    response = None
    if SLACK["url"]:
        response = requests.post(
            SLACK["url"],
            data=json.dumps(
                {
                    "attachments":
                        [
                            {
                                "author_name": "HealthTools API - Kenya",
                                "color": "danger",
                                "pretext": "[SCRAPER] New Alert for HealthTools API - Kenya SMS Endpoint",
                                "fields": [
                                    {
                                        "title": "Message",
                                        "value": message,
                                        "short": False
                                        },
                                    {
                                        "title": "Machine Location",
                                        "value": "{}".format(getpass.getuser()),
                                        "short": True
                                        },
                                    {
                                        "title": "Time",
                                        "value": "{}".format(datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
                                        "short": True},
                                    {
                                        "title": "Severity",
                                        "value": message,
                                        "short": True
                                        }
                                    ]
                                }
                            ]
                    }),
            headers={"Content-Type": "application/json"})
    return response
