import tornado.web
from bitarray import bitarray

from base_handler import BaseHandler
from utils.app_util import is_valid_email, is_valid_password, hash_password
from auth.models import Auth, AuthToken


class IndexHandler(BaseHandler):
    def get(self):
        self.write(dict(message='Hello, Welcome to Issue Ticket System!'))

    def post(self):
        self.write(dict(message='Hello, Welcome to Issue Ticket System!'))


class SignupHandler(BaseHandler):
    def post(self):
        data = self.convert_argument_to_json()

        email = data.get('email', None)
        password = data.get('password', None)

        if not email or not is_valid_email(email):
            raise tornado.web.HTTPError(400, 'Invalid email')

        if not password or not is_valid_password(password):
            raise tornado.web.HTTPError(400, 'Invalid password. Min 6 characters required.')

        with self.session_scope() as session:
            # Checking if user already exists with the same email
            if session.query(Auth).filter(Auth.email == email).first():
                raise tornado.web.HTTPError(403, 'Email Already in use. Please try to sign-up using a different email.')

            hashed = hash_password(password)

            # Creating the initial permission for the user.
            # 1. Create, 2. Edit, 3. View, 4.Delete
            initial_permission = [True, False, True, False]

            permission = bitarray()
            permission.extend(initial_permission)

            user = Auth(
                email=email,
                hashed=hashed,
                permissions=permission.to01()
            )

            session.add(user)

            token = AuthToken.create_token(session, user, AuthToken.AUTHENTICATION_TOKEN)

            response = dict(
                token=str(token.uid),
                user=user.to_json()
            )

            self.write(response)


class LoginHandler(BaseHandler):
    pass
