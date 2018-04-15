from ticket import handlers

def get_app_routes():
    return [
        (r"/api/ticket", handlers.CreteTicketHandler),
        (r"/api/ticket/([-0-9a-fA-F]*)", handlers.TicketHandler)
    ]