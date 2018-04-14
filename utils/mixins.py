import datetime
import uuid

from sqlalchemy import Column, DateTime, Boolean
from sqlalchemy import func
from sqlalchemy.dialects import postgresql

UUID = postgresql.UUID(as_uuid=True)


class UIDMixin(object):
    """ A base model with a
        uid 128-bit
        created_at date
    """
    uid = Column(UUID, primary_key=True, default=uuid.uuid4, nullable=False)
    created_at = Column(DateTime, default=func.now(), nullable=False, index=True)

    def __init__(self, *args, **kwargs):
        super(UIDMixin, self).__init__(*args, **kwargs)
        if self.uid is None:
            self.uid = uuid.uuid4()
        if self.created_at is None:
            self.created_at = datetime.datetime.utcnow()

    def to_json(self):
        return dict(uid=str(self.uid),
                    created_at=self.created_at.isoformat())


class DeletableMixin(object):
    """
    Model that can be deleted. We don't delete anything from the database,
    we just mark rows as deleted.
    """
    is_deleted = Column(Boolean, default=False, server_default='f', nullable=False)
    deleted_at = Column(DateTime, nullable=True)

    def mark_deleted(self):
        self.is_deleted = True
        if self.deleted_at is None:
            self.deleted_at = datetime.datetime.utcnow()
