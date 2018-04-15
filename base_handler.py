import tornado.web
import tornado.escape
import functools

from auth.models import AuthToken
from utils.app_util import convert_uuid_or_400

class BaseHandler(tornado.web.RequestHandler):
    @property
    def db(self):
        return self.application.db

    def session_scope(self):
        return self.db.session_scope()

    def access_token_from_query_string(self):
        return self.get_query_argument('access_token', None)

    def access_token_from_authorization_header(self):
        header_token = self.request.headers.get("Authorization")

        if header_token:
            token_type, header_token = str(header_token).split(' ')
            if token_type == 'Bearer' and header_token:
                return header_token
        return None

    def convert_argument_to_json(self):
        data = tornado.escape.json_decode(self.request.body)
        return data


def authenticated(method):
    """ Decorate API methods with this to require that token is passed against Authorization.
        If the token is missing , 401 HTTP error is thrown
    """

    @functools.wraps(method)
    def wrapper(self, *args, **kwargs):
        token = self.access_token_from_authorization_header()

        if token is None:
            raise tornado.web.HTTPError(401, 'Unauthorized Access. Auth token missing.')

        with self.session_scope() as session:
            token = convert_uuid_or_400(token)

            token = session.query(AuthToken).filter(AuthToken.uid == token).one_or_none()

            if not token or token.is_expired() or token.is_deleted:
                raise tornado.web.HTTPError(403, 'Auth token invalid or expired. Please login.')

        return method(self, *args, **kwargs)

    return wrapper
