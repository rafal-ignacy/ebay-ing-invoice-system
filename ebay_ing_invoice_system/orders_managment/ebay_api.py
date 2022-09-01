import time
import requests
from requests.exceptions import RequestException

class EbayApi:
    def __init__(self):
        pass

    def get_access_token(self, url, headers, payload):
        loop_index = 1

        while True:
            try:
                request = requests.post(url, headers = headers, data = payload)
            except:
                if loop_index >= 3:
                    raise RequestException("Error during eBay API access token request")
                else:
                    time.sleep(5)
                    loop_index += 1
                    continue
            else:
                if loop_index >= 3:
                    raise RequestException("Error during eBay API access token request")
                elif request.status_code != 200:
                    time.sleep(5)
                    loop_index += 1
                    continue
                else:
                    request_response = request.text

                    return request_response

    def get_orders(self, url, headers):
        loop_index = 1

        while True:
            try:
                request = requests.get(url, headers = headers)
            except:
                if loop_index >= 3:
                    raise RequestException("Error during eBay API getOrders request")
                else:
                    time.sleep(5)
                    loop_index += 1
                    continue
            else:
                if loop_index >= 3:
                    raise RequestException("Error during eBay API getOrders request")
                elif request.status_code != 200:
                    time.sleep(5)
                    loop_index += 1
                    continue
                else:
                    request_response = request.text

                    return request_response

    def get_order(self, url, headers):
        loop_index = 1

        while True:
            try:
                request = requests.get(url, headers = headers)
            except:
                if loop_index >= 3:
                    raise RequestException("Error during eBay API getOrder request")
                elif request.status_code != 200:
                    time.sleep(5)
                    loop_index += 1
                    continue
                else:
                    time.sleep(5)
                    loop_index += 1
                    continue
            else:
                if request.status_code != 200:
                    time.sleep(5)
                    loop_index += 1
                    continue
                else:
                    request_response = request.text

                    return request_response