from sqlalchemy import Column, String

from utils.dbbase import Base
from utils.mixins import UIDMixin, DeletableMixin


class Product(UIDMixin, DeletableMixin, Base):
    """    Product is an identity for which tickets can be created
    """
    __tablename__ = 'product'

    HEALTH_CARE = 'health_care'
    BANKING = 'banking'
    OTHERS = 'others'

    VALID_PRODUCT_TYPES = [HEALTH_CARE, BANKING, OTHERS]

    name = Column(String(20), nullable=False)
    type = Column(String(20), nullable=False, default=OTHERS, server_default=OTHERS)

    owner_email = Column(String(30), nullable=False)

    @staticmethod
    def convert_to_dict(products):
        data = []

        for product in products:
            data.append(
                dict(
                    name=product.name,
                    type=product.type,
                    owner=product.owner_email,
                    uid=str(product.uid),
                    created_at=product.created_at.isoformat()
                )
            )

        return data
