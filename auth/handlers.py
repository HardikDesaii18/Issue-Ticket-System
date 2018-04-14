import tornado.web
from bitarray import bitarray

from base_handler import BaseHandler, authenticated
from utils.app_util import is_valid_email, is_valid_password, hash_password, match_password, convert_uuid_or_400
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
    def post(self):
        data = self.convert_argument_to_json()

        email = data.get('email', None)
        password = data.get('password', None)

        if not email or not password:
            raise tornado.web.HTTPError(400, 'Invalid username or password')

        with self.session_scope() as session:
            user = session.query(Auth).filter(Auth.email == email).one_or_none()

            if not user:
                raise tornado.web.HTTPError(400, 'Incorrect email. No user found for {}'.format(email))

            if not match_password(password, user.hashed):
                raise tornado.web.HTTPError(400, 'Incorrect password for {}'.format(email))

            token = AuthToken.create_token(session, user, AuthToken.AUTHENTICATION_TOKEN)

            response = dict(
                token=str(token.uid),
                user=user.to_json()
            )

            self.write(response)


class EditPermissionHandler(BaseHandler):
    """
    PUT Handler to change the permission of the user. Pass the user access token in the Authorization Header
    """

    @authenticated
    def put(self):
        token = self.access_token_from_authorization_header()

        data = self.convert_argument_to_json()

        permissions = data['permissions']

        if len(permissions) is not 4:
            raise tornado.web.HTTPError(400, 'Some permissions are missing. Permissions count must be 4.')

        for ix, permission in enumerate(permissions):

            try:
                permission = int(permission)

                if permission not in [0, 1]:
                    raise Exception('Permission must be either of 0 or 1.')

                permissions[ix] = int(permission)

            except Exception as ex:
                raise tornado.web.HTTPError(400, 'Permission must be integer')

        with self.session_scope() as session:
            token = convert_uuid_or_400(token)

            token = session.query(AuthToken).filter(AuthToken.uid == token).one_or_none()

            user = token.auth
            updated_permission = bitarray()

            updated_permission.extend(permissions)

            user.permissions = updated_permission.to01()

            session.flush()

            response = user.to_json()
            self.write(response)
