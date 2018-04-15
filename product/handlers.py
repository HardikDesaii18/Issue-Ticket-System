import tornado.web
from base_handler import BaseHandler, authenticated
from product.models import Product
from utils.app_util import is_valid_email


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
        pass

    @authenticated
    def put(self, product_uid):
        pass

    @authenticated
    def delete(self, product_uid):
        pass
