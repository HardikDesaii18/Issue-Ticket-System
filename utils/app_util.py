import uuid
import tornado.web
import re
import bcrypt


def convert_uuid_or_400(uidstr):
    try:
        return uuid.UUID(uidstr)

    except ValueError:
        raise tornado.web.HTTPError(
            400, log_message="Bad uuid format")


def is_valid_email(email):
    EMAIL_REGEX = re.compile(r"[^@]+@[^@]+\.[^@]+")
    return EMAIL_REGEX.match(email)


def hash_password(password):
    return bcrypt.hashpw(password.encode('utf8'), bcrypt.gensalt())


def match_password(password, hashed_password):
    canditate = password.encode('utf-8')
    return bcrypt.hashpw(canditate, hashed_password) == hashed_password


def is_valid_password(password):
    return len(password) >= 6