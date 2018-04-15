from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.dialects import postgresql
from sqlalchemy.orm import relationship

from utils.dbbase import Base
from utils.mixins import UIDMixin, UUID, DeletableMixin


class Ticket(UIDMixin, DeletableMixin, Base):
    """    Ticket is an identity that can be against a Product
    """
    __tablename__ = 'ticket'

    ENHANCEMENT = 'enhancement'
    BUG = 'bug'
    FEATURE = 'feature'

    SELECTED_FOR_DEV = 'select_dev'
    IN_PROGRESS = 'in_progess'
    DONE = 'done'

    VALID_TICKET_TYPES = [ENHANCEMENT, BUG, FEATURE]
    VALID_TICKET_STATUS = [SELECTED_FOR_DEV, IN_PROGRESS, DONE]

    auth_uid = Column(UUID, ForeignKey('auth.uid'), nullable=False)
    auth = relationship('Auth', backref='tickets')

    product_uid = Column(UUID, ForeignKey('product.uid'), nullable=False)

    status = Column(String(20), nullable=False, default=SELECTED_FOR_DEV, server_default=SELECTED_FOR_DEV )
    type = Column(String(20), nullable=False, default=BUG, server_default=BUG)

    description = Column(postgresql.JSON, nullable=False)

    @staticmethod
    def convert_to_dict(tickets):
        data = []
        for ticket in tickets:
            data.append(
                dict(
                    uid=str(ticket.uid),
                    description=ticket.description,
                    type=ticket.type,
                    status=ticket.status,
                    product_uid=str(ticket.product_uid)
                )
            )

        return data

