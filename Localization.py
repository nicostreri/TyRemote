import json
import os
from requests import get, post, RequestException
import WiFI


class FailedLocalization(Exception):
    """
    Raised when get localization fail.
    """
    pass


def get_location_by_ip():
    """
    Get location of this PC using the IP network
    :return: tuple (lat, lng)
    """
    data = get('http://ip-api.com/json/').json()
    return data['lat'], data['lon']


def get_location_by_wifi():
    """
    Get location of this PC using the Wifi networks
    :return: tuple (lat, lng)
    """
    body_request = {"wlan": WiFI.get_wifi_networks()}
    url = 'https://pos.ls.hereapi.com/positioning/v1/locate?apiKey=' + os.getenv("TYR_HERE_API_KEY")
    try:
        response = post(url, data=json.dumps(body_request), headers={"content-type": "application/json"})
        response.raise_for_status()
    except RequestException:
        raise FailedLocalization

    response_localization = json.loads(response.text)
    return response_localization['location']['lat'], response_localization['location']['lng']
