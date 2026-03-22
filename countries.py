import sys
import requests


def find_IP():
    page = "http://ip-api.com/json/"
    try:
        resp = requests.get(page, timeout=10)
        resp.raise_for_status()
        req = resp.json()
        country = req['country']
        query = req['query']
        country_code = req['countryCode']
        return query, country, country_code
    except (requests.RequestException, KeyError, ValueError) as e:
        print("\n\033[38;5;196mFailed to fetch IP information: {}\033[0m".format(e))
        sys.exit(1)

