import tornado.web
import tornado.escape


class BaseHandler(tornado.web.RequestHandler):
    @property
    def db(self):
        return self.application.db

    def session_scope(self):
        return self.db.session_scope()

    def access_token_from_query_string(self):
        return self.get_query_argument('access_token', None)

    def access_token_from_authorization_header(self):
        header_token_spec = self.request.headers.get("Authorization")
        if header_token_spec:
            token_type, _, header_token = header_token_spec.partition(' ')
            if token_type == 'Bearer' and header_token:
                return header_token
        return None

    def convert_argument_to_json(self):
        data = tornado.escape.json_decode(self.request.body)
        return data
