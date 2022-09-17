import pandas as pd

class OrderProcessing:
    def __init__(self):
        pass

    def get_data_from_ebay_order_list(self, ebay_order_list):
        ebay_order_list_normalized = pd.json_normalize(ebay_order_list)

        order_list = []
        for order_index in range(len(ebay_order_list_normalized)):
            order = []

            self.get_order_details(ebay_order_list_normalized, order, order_index)
            self.get_items_details(ebay_order_list_normalized, order, order_index)
            self.get_customer_details(ebay_order_list_normalized, order, order_index)
            order_list.append(tuple(order))

        return order_list

    def get_order_details(self, ebay_orders_normalized, order, order_index):
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