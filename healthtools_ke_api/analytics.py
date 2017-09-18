import requests


def track_event(tracking_id, category, action, cid, label=None, value=0):
    '''
    Posts Tracking in info to Google Analytics using measurement protocol.

    Args:
        tracking_id: The tracking ID of the Google Analytics account in which these data is associated with.

        category: The name assigned to the group of similar events to track.

        action: The Specific action being tracked.

        cid: Anonymous Client Identifier. Ideally, this should be a UUID that is associated with particular user, device

        label: Label of the event.
        
        value: Value of event in this case number of results obtained

    Returns:
        No return value 
        # If the request fails, it will raise a RequestException.

    '''
    data = {
        'v': '1',
        'tid': tracking_id,
        'cid': cid,
        't': 'event',
        'ec': category,
        'ea': action,
        'el': label,
        'ev': value,
    }
    response = requests.post(
        'http://www.google-analytics.com/collect', data=data)
    response.raise_for_status()
