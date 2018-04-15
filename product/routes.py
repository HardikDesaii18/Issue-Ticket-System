from product import handlers


def get_app_routes():
    return [
        (r"/api/product", handlers.CreateProductHandler),
        (r"/api/product/([-0-9a-fA-F]*)", handlers.ProductHandler)
    ]