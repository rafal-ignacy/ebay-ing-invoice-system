from ebay_ing_invoice_system.orders_managment.order_collection import OrderCollection
from ebay_ing_invoice_system.orders_managment.order_processing import OrderProcessing

if __name__ == '__main__':
    order_collection = OrderCollection()
    access_token = order_collection.ebay_get_access_token()
    orders_list = order_collection.ebay_get_orders()

    order_processing = OrderProcessing()
    orders = order_processing.get_data_from_ebay_order_list(orders_list)
    print(orders)