from datetime import datetime
import json

from ebay_api import EbayApi

class OrdersManagment:
    def __init__(self):
        pass

    def get_ebay_oauth_data(self, data_file_path):
        with open(data_file_path, "r") as data_file:
            data_file_content = data_file.read()
            data_json = json.loads(data_file_content)

            url = data_json["oauth"]["url"]
            headers = data_json["oauth"]["headers"]
            payload = data_json["oauth"]["payload"]

            return url, headers, payload

    def get_ebay_get_orders_data(self, data_file_path):
        with open(data_file_path, "r") as data_file:
            data_file_content = data_file.read()
            data_json = json.loads(data_file_content)

        url = data_json["get_orders"]["url"]
        headers = data_json["get_orders"]["headers"]

        return url, headers

    def request_response_fetch_token(self, request_response):
        request_response_json = json.loads(request_response)
        access_token = request_response_json["access_token"]

        return access_token

    def set_ebay_get_orders_time(self):
        current_utc_time = datetime.utcnow()
        utc_time_one_hour_ago = current_utc_time - datetime.timedelta(hours = 1)
        get_orders_time_string = utc_time_one_hour_ago.strftime("%Y-%m-%dT%H:%M:%S.000Z")

        return get_orders_time_string