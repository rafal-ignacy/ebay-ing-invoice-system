import pandas as pd
from enum import Enum

class OrderIndex(Enum):
    orderId = 0
    creationDate = 1
    orderPaymentStatus = 2
    priceSummary_total_value = 3
    priceSummary_total_currency = 4
    priceSummary_delivery_value = 5
    priceSummary_delivery_currency = 6
    items = 7
    fullName = 8
    addressLine1 = 9
    addressLine2 = 10
    city = 11
    countryCode = 12
    postalCode = 13
    stateOrProvince = 14

class ItemsIndex(Enum):
    sku = 0
    quantity = 1
    itemCost_value = 2
    itemCost_currency = 3

class OrderProcessing:
    def __init__(self):
        pass

    def get_data_from_ebay_order_list(self, ebay_order_list): #fetching data from ebay parsed response, divided to smaller functions
        ebay_order_list_normalized = pd.json_normalize(ebay_order_list)

        order_list = []
        for order_index in range(len(ebay_order_list_normalized)):
            order = []

            self.get_order_details(ebay_order_list_normalized, order, order_index)
            self.get_items_details(ebay_order_list_normalized, order, order_index)
            self.get_customer_details(ebay_order_list_normalized, order, order_index)
            order_list.append(tuple(order))
            order_list.reverse()

        return order_list

    def get_order_details(self, ebay_orders_normalized, order, order_index): #fetching order details from ebay parsed API response
        for key in ["orderId", "creationDate", "orderPaymentStatus", "pricingSummary.priceSubtotal.value", "pricingSummary.priceSubtotal.currency", "pricingSummary.deliveryCost.value", "pricingSummary.deliveryCost.currency"]:
            order.append(ebay_orders_normalized[key][order_index])

    def get_items_details(self, ebay_orders_normalized, order, order_index):
        items_list_normalized = pd.json_normalize(ebay_orders_normalized["lineItems"][order_index])
        items_list = []
        for item_index in range(len(items_list_normalized)):
            item = []
            if "sku" in items_list_normalized.keys():
                item.append(items_list_normalized["sku"][item_index])
            else:
                item.append(None)
            for key in ["quantity", "lineItemCost.value", "lineItemCost.currency"]:
                item.append(items_list_normalized[key][item_index])
            items_list.append(tuple(item))
        order.append(tuple(items_list))

    def get_customer_details(self, ebay_orders_normalized, order, order_index):
        fulfillment_instructions_normalized = pd.json_normalize(ebay_orders_normalized["fulfillmentStartInstructions"][order_index])
        for key in ["shippingStep.shipTo.fullName", "shippingStep.shipTo.contactAddress.addressLine1", "shippingStep.shipTo.contactAddress.city", "shippingStep.shipTo.contactAddress.countryCode"]:
            order.append(fulfillment_instructions_normalized[key][0])
        for conditional_key in ["shippingStep.shipTo.contactAddress.addressLine2", "shippingStep.shipTo.contactAddress.postalCode", "shippingStep.shipTo.contactAddress.stateOrProvince"]:
            if conditional_key in fulfillment_instructions_normalized.keys():
                order.append(fulfillment_instructions_normalized[conditional_key][0])
            else:
                order.append(None)

    def add_data_to_database(self, orders, database):
        for order in orders:
            SQL_command = f"SELECT COUNT(orderId) FROM orders WHERE orderId = \"{order[OrderIndex.orderId.value]}\""
            order_id_amount = database.get_data(SQL_command)[0][0]

            if order_id_amount == 0:
                order_id = self.add_order_to_database(database, order)
                self.add_customer_to_database(database, order, order_id)
                self.add_items_to_database(database, order, order_id)

    def add_order_to_database(self, order, database):
        SQL_command = "INSERT INTO orders(orderId, creationDate, orderPaymentStatus, `priceSummary.total.value`, `priceSummary.total.currency`, `priceSummary.delivery.value`, `priceSummary.delivery.currency`) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        SQL_values = (
            order[OrderIndex.orderId.value],
            order[OrderIndex.creationDate.value],
            order[OrderIndex.orderPaymentStatus.value],
            order[OrderIndex.priceSummary_total_value.value],
            order[OrderIndex.priceSummary_total_currency.value],
            order[OrderIndex.priceSummary_delivery_value.value],
            order[OrderIndex.priceSummary_delivery_currency.value]
        )
        order_id = database.insert_data(SQL_command, SQL_values)

        return order_id

    def add_customer_to_database(self, database, order, order_id):
        SQL_command = "INSERT INTO customers(fullName, addressLine1, city, countryCode, addressLine2, postalCode, stateOrProvince, order_id) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
        SQL_values = (
            order[OrderIndex.fullName.value],
            order[OrderIndex.addressLine1.value],
            order[OrderIndex.addressLine2.value],
            order[OrderIndex.city.value],
            order[OrderIndex.countryCode.value],
            order[OrderIndex.postalCode.value],
            order[OrderIndex.stateOrProvince.value],
            order_id
        )
        database.insert_data(SQL_command, SQL_values)

    def add_items_to_database(self, database, order, order_id):
        items = order[OrderIndex.items.value]
        SQL_command = "INSERT INTO items(sku, quantity, `itemCost.value`, `itemCost.currency`, order_id) VALUES (%s, %s, %s, %s, %s)"
        for item in items:
            SQL_values = (
                item[ItemsIndex.sku.value],
                item[ItemsIndex.quantity.value],
                item[ItemsIndex.itemCost_value.value],
                item[ItemsIndex.itemCost_currency.value],
                order_id
            )
            database.insert_data(SQL_command, SQL_values)

    def get_orders_without_invoices(self, database):
        SQL_command = "SELECT id FROM orders WHERE invoiceId IS NULL"
        database_orders = database.get_data(SQL_command)

        orders_without_invoices = []
        for database_order in database_orders:
            orders_without_invoices.append(database_order[0])

        return orders_without_invoices