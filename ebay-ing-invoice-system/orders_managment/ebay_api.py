import json
import requests
import time

class EbayApi:
    def __init__(self):
        pass

    def get_ebay_oauth_data(self, data_file_path):
        with open(data_file_path, "r") as data_file:
            data_file_content = data_file.read()
            data_json = json.loads(data_file_content)
        
            url = data_json["url"]
            headers = data_json["headers"]
            payload = data_json["payload"]

            return url, headers, payload

    def get_access_token(self, url, headers, payload):
        loop_index = 1

        while True:
            try:
                request = requests.post(url, headers = headers, data = payload)
            except:
                if loop_index >= 3:
                    raise Exception()
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
                    request_response = request.text()
                    access_token = self.request_response_fetch_token(request_response)

                    return access_token

    def request_response_fetch_token(self, request_response):
        request_response_json = json.loads(request_response)

        access_token = request_response_json["access_token"]

        return access_token