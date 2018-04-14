import uuid
import tornado.web


def convert_uuid_or_400(uidstr):
    try:
        return uuid.UUID(uidstr)

    except ValueError:
        raise tornado.web.HTTPError(
            400, log_message="Bad uuid format")
