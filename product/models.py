from sqlalchemy import Column, String

from utils.dbbase import Base
from utils.mixins import UIDMixin


class Product(UIDMixin, Base):
    """    Product is an identity for which tickets can be created
    """
    __tablename__ = 'product'

    HEALTH_CARE = 'health_care'
    BANKING = 'banking'
    OTHERS = 'others'

    VALID_PRODUCT_TYPES = [HEALTH_CARE, BANKING, OTHERS]

    name = Column(String(20), nullable=False, unique=True)
    type = Column(String(20), nullable=False, default=OTHERS, server_default=OTHERS)

    owner_email = Column(String(30), nullable=False)
