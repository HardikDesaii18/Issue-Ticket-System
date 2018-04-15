import tornado.web
from sqlalchemy import and_

from base_handler import BaseHandler, authenticated
from product.models import Product
from utils.app_util import is_valid_email, convert_uuid_or_400


class CreateProductHandler(BaseHandler):
    @authenticated
    def get(self):
        """
            Handler to list all the products
            route - /api/product

            :return: list of non-deleted products
        """
        with self.session_scope() as session:
            products = session.query(Product).filter(Product.is_deleted == False).all()

            response = Product.convert_to_dict(products)

            self.write(response)

    @authenticated
    def post(self):
        """
            Handler to create new product
            Route - /api/product

            :param:
                name - Name of the product
                type - Type of the product, Must be health_care, banking, others
                email - Owners email of the Product.


        :return: uid, timestamp of the product created.
        """
        data = self.convert_argument_to_json()

        name = data.get('name', None)
        type = data.get('type', None)
        owners_email = data.get('email', None)

        if not name or len(name) < 3:
            raise tornado.web.HTTPError(400, 'Invalid name. Min 3 characters required.')

        if not type or type not in Product.VALID_PRODUCT_TYPES:
            raise tornado.web.HTTPError(400, 'Invalid type. Must be one of health_care, banking or others.')

        if not owners_email or not is_valid_email(owners_email):
            raise tornado.web.HTTPError(400, 'Invalid Owner\'s email.')

        with self.session_scope() as session:
            if session.query(Product).filter(and_(Product.name == name, Product.is_deleted == False)).one_or_none():
                raise tornado.web.HTTPError(400, 'Product with the name {} already exists'.format(name))

            product = Product(
                name=name,
                type=type,
                owner_email=owners_email
            )
            session.add(product)
            session.flush()

            response = product.to_json()

            self.write(response)


class ProductHandler(BaseHandler):
    @authenticated
    def get(self, product_uid):
        """

        :param product_uid: uid of the product
        :return: json of the product.
        """
        product_uid = convert_uuid_or_400(product_uid)

        with self.session_scope() as session:
            product = session.query(Product).filter(
                and_(
                    Product.uid == product_uid,
                    Product.is_deleted == False
                )
            ).one_or_none()

            if product:
                response = Product.convert_to_dict(product)
                self.write(response)

            else:
                raise tornado.web.HTTPError(409, 'No product found for {}'.format(product_uid))

    @authenticated
    def put(self, product_uid):
        """

        :param product_uid: uid of the product to edit
        :return: uid, timestamp of the edited product

        """
        product_uid = convert_uuid_or_400(product_uid)

        data = self.convert_argument_to_json()

        name = data.get('name', None)
        type = data.get('type', None)
        owners_email = data.get('email', None)

        if not name or len(name) < 3:
            raise tornado.web.HTTPError(400, 'Invalid name. Min 3 characters required.')

        if not type or type not in Product.VALID_PRODUCT_TYPES:
            raise tornado.web.HTTPError(400, 'Invalid type. Must be one of health_care, banking or others.')

        if not owners_email or not is_valid_email(owners_email):
            raise tornado.web.HTTPError(400, 'Invalid Owner\'s email.')

        with self.session_scope() as session:
            product = session.query(Product).filter(
                and_(
                    Product.uid == product_uid,
                    Product.is_deleted == False
                )
            ).one_or_none()

            if product:
                product.name = name
                product.type = type
                product.owner_email = owners_email

                session.flush()

                response = product.to_json()

                self.write(response)

            else:
                raise tornado.web.HTTPError(409, 'No product found for {}'.format(product_uid))

    @authenticated
    def delete(self, product_uid):
        """
        :param product_uid: uid of the product to delete.
        :return: uid, created_at and deleted_at timestamp of product.
        """
        product_uid = convert_uuid_or_400(product_uid)

        with self.session_scope() as session:
            product = session.query(Product).filter(
                and_(
                    Product.uid == product_uid,
                    Product.is_deleted == False
                )
            ).one_or_none()

            if product:
                product.mark_deleted()

                response = product.to_json()
                response['deleted_at'] = product.deleted_at.isoformat()
                self.write(response)

            else:
                raise tornado.web.HTTPError(409, 'No product found for {}'.format(product_uid))
