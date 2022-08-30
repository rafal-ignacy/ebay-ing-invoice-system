from ebay_ing_invoice_system.orders_managment.orders_managment import OrdersManagment

if __name__ == '__main__':
    orders_managment = OrdersManagment()
    access_token = orders_managment.ebay_api_get_access_token()
    orders = orders_managment.ebay_api_get_orders()