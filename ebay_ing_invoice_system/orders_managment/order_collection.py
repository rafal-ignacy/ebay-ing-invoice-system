from datetime import datetime, timedelta
import json

from .ebay_api import EbayApi

class OrderCollection:
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

    def get_ebay_get_order_data(self, data_file_path):
        with open(data_file_path, "r") as data_file:
            data_file_content = data_file.read()

        data_json = json.loads(data_file_content)
        url = data_json["get_order"]["url"]
        headers = data_json["get_order"]["headers"]

        return url, headers

    def set_ebay_get_orders_time(self):
        current_utc_time = datetime.utcnow()
        utc_time_one_hour_ago = current_utc_time - timedelta(hours=1)
        get_orders_time_string = utc_time_one_hour_ago.strftime("%Y-%m-%dT%H:%M:%S.000Z")
        get_orders_time_string = "2022-08-25T16:00:00.000Z"

        return get_orders_time_string

    def prepare_ebay_get_orders_request_url(self, url, time_string):
        url = url.replace("{time_string}", time_string)

        return url

    def prepare_ebay_get_order_request_url(self, url, order_id):
        url = url.replace("{order_id}", order_id)

        return url

    def prepare_ebay_request_headers(self, headers, access_token):
        headers_string = json.dumps(headers)
        headers_string = headers_string.replace("{access_token}", access_token)
        headers = json.loads(headers_string)

        return headers

    def request_response_fetch_token(self, request_response):
        request_response_json = json.loads(request_response)
        access_token = request_response_json["access_token"]

        return access_token

    def get_access_token(self):
        url, headers, payload = self.get_ebay_oauth_data("data/ebay_data.json")
        ebay_api = EbayApi()
        request_response = ebay_api.get_access_token(url, headers, payload)
        access_token = self.request_response_fetch_token(request_response)

        return access_token

    def get_orders(self):
        access_token = self.get_access_token()

        url, headers = self.get_ebay_get_orders_data("data/ebay_data.json")
        time_string = self.set_ebay_get_orders_time()
        url = self.prepare_ebay_get_orders_request_url(url, time_string)
        headers = self.prepare_ebay_request_headers(headers, access_token)

        ebay_api = EbayApi()
        request_response = ebay_api.get_orders(url, headers)
        orders = self.request_response_fetch_orders(request_response)

        return orders

    def get_order(self, order_id):
        access_token = self.get_access_token()

        url, headers = self.get_ebay_get_order_data("data/ebay_data.json")
        url = self.prepare_ebay_get_order_request_url(url, order_id)
        headers = self.prepare_ebay_request_headers(headers, access_token)

        ebay_api = EbayApi()
        request_response = ebay_api.get_order(url, headers)
        order = json.loads(request_response)

        return order

    def request_response_fetch_orders(self, request_response):
        request_response_json = json.loads(request_response)
        orders_list = request_response_json["orders"]

        return orders_list
