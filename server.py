import tornado.web
import tornado.ioloop
import logging


from auth import routes as auth_routes
from ticket import routes as ticket_routes
from product import routes as product_routes
from utils.db import Db
from settings import settings
from auth.handlers import IndexHandler

class ApiApplication(tornado.web.Application):
    pass


def create(settings):
    routes = [
        (r"/api", IndexHandler),
    ]

    # Adding the routes of all the modules

    routes += auth_routes.get_app_routes()
    routes += ticket_routes.get_app_routes()
    routes += product_routes.get_app_routes()

    print("Creating Application... ")

    application = ApiApplication(routes, **settings['tornado'])

    application.db = Db(**settings['db'])
    application.all_settings = settings

    return application


def start(application):
    print('Starting the Application...')

    application.listen(8998, **application.all_settings['tornado_server_settings'])
    logging.info("Listening at port %d", 8998)
    tornado.ioloop.IOLoop.instance().start()


if __name__ == "__main__":
    settings = settings

    # Start the app
    application = create(settings)
    start(application)
