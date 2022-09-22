from ebay_ing_invoice_system.orders_managment.order_collection import OrderCollection
from ebay_ing_invoice_system.orders_managment.order_processing import OrderProcessing
from ebay_ing_invoice_system.database import Database

if __name__ == '__main__':
    order_collection = OrderCollection()
    access_token = order_collection.ebay_get_access_token()
    orders_list = order_collection.ebay_get_orders()

    order_processing = OrderProcessing()
    orders = order_processing.get_data_from_ebay_order_list(orders_list)

    database = Database()
    order_processing.add_data_to_database(orders, database)

    orders_without_invoice = order_processing.get_orders_without_invoices(database)