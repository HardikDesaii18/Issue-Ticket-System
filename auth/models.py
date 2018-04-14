import datetime
from sqlalchemy.dialects import postgresql
from sqlalchemy import Column, String, LargeBinary, ForeignKey, Integer, DateTime
from sqlalchemy.orm import relationship

from utils.dbbase import Base
from utils.mixins import UIDMixin, UUID, DeletableMixin


class Auth(UIDMixin, Base):
    """    Auth in an authentication identity.
    """
    __tablename__ = 'auth'

    email = Column(String, nullable=False, unique=True)

    # hashed contains bcrypt'ed password.
    # LargeBinary column will be bytea type
    hashed = Column(LargeBinary(60), nullable=False)

    # set the bit for the type of permission
    # CREATE_TICKET - bit 0
    # EDIT_TICKET - bit 1
    # VIEW_TICKET - bit 2
    # DELETE_TICKET - bit 3

    permissions = Column(postgresql.BIT(4), nullable=False)


# Auth token table with token type, that is usable for different purposes:
# password reset etc.
class AuthToken(UIDMixin, DeletableMixin, Base):
    __tablename__ = 'auth_token'

    AUTHENTICATION_TOKEN = "auth_token"

    # For now the type is only AUTHENTICATION_TOKEN
    token_type = Column(String(15), nullable=False, index=True)

    auth_uid = Column(UUID, ForeignKey('auth.uid'), nullable=False)
    auth = relationship('Auth', backref='auth_tokens')

    expire_timeout_seconds = Column(Integer, nullable=False, default=24 * 60 * 60)

    def revoke(self):
        self.mark_deleted()

    @staticmethod
    def create_token(session, user, token_type):
        token = AuthToken(auth=user, token_type=token_type)
        session.add(token)
        return token

    @staticmethod
    def get(session, token_uid, token_type):
        stored = session \
            .query(AuthToken) \
            .filter(AuthToken.uid == token_uid,
                    AuthToken.token_type == token_type,
                    AuthToken.is_deleted == False) \
            .first()
        return stored

    def expires_at(self):
        return self.created_at + datetime.timedelta(seconds=self.expire_timeout_seconds)

    def is_expired(self):
        now = datetime.datetime.utcnow()
        return self.expires_at() < now