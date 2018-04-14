from auth import handlers
def get_app_routes():
    return [
        (r"/api/sign-up", handlers.SignupHandler),
        (r"/api/sign-in", handlers.LoginHandler)
    ]