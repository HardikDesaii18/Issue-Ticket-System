from base_handler import BaseHandler


class IndexHandler(BaseHandler):
    def get(self):
        self.write(dict(message='Hello, Welcome to Issue Ticket System!'))