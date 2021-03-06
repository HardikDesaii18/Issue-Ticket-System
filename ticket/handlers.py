import tornado.web
from sqlalchemy import and_

from base_handler import BaseHandler, authenticated
from ticket.models import Ticket
from utils.app_util import convert_uuid_or_400
from auth.models import AuthToken, Auth
from product.models import Product


class CreteTicketHandler(BaseHandler):
    @authenticated
    def get(self):
        """
        Handler to get all the tickets if the user has permission to view tickets.
        Route - /api/ticket
        Method- GET

        :return: list of tickets
        """
        with self.session_scope() as session:
            token = self.access_token_from_authorization_header()

            token = convert_uuid_or_400(token)

            auth_token = session.query(AuthToken).filter(AuthToken.uid == token).one_or_none()

            permissions = auth_token.auth.permissions

            if int(permissions[2]) != 1:
                raise tornado.web.HTTPError(409, 'Current user don\'t have permission to view tickets.')

            tickets = session.query(Ticket).filter(
                    Ticket.is_deleted == False
            ).all()

            response = Ticket.convert_to_dict(tickets)

            self.write(dict(tickets=response))

    @authenticated
    def post(self):
        """
        Handler to create new Ticket.

        Route - /api/ticket
        Method- POST
        :param:
            status - either of select_dev, in_progress or done.
            type- either of Bug, Enhancement or Feature.
            product_uid - Foreign key for model Product

            description - JSON field storing the description of ticket.
        :return: uid, timestamp of the ticket created.
        """
        data = self.convert_argument_to_json()

        status = data.get('status', None)
        type = data.get('type', None)
        desc = data.get('desc', None)
        product_uid = convert_uuid_or_400(data.get('product_uid', None))

        if not type or type not in Ticket.VALID_TICKET_TYPES:
            raise tornado.web.HTTPError(400, 'Invalid type for ticket. Must be one of bug, enhancement or feature')

        if not status or status not in Ticket.VALID_TICKET_STATUS:
            raise tornado.web.HTTPError(400,
                                        'Invalid status for ticket. Must be one of select_dev, in_progress or done')

        if not desc:
            raise tornado.web.HTTPError(400, 'Please provide description for the ticket.')

        if not product_uid:
            raise tornado.web.HTTPError(400, "Please provide product uid for which ticket to be created.")

        with self.session_scope() as session:

            product = session.query(Product).filter(
                and_(
                    Product.uid == product_uid,
                    Product.is_deleted == False
                )
            ).one_or_none()

            if not product:
                raise tornado.web.HTTPError(409, 'No product found for {}'.format(product_uid))

            token = self.access_token_from_authorization_header()

            token = convert_uuid_or_400(token)

            auth_token = session.query(AuthToken).filter(AuthToken.uid == token).one_or_none()

            permissions = auth_token.auth.permissions

            if int(permissions[0]) != 1:
                raise tornado.web.HTTPError(409, 'Current user don\'t have permission to create ticket.')

            ticket = Ticket(
                status=status,
                type=type,
                auth=auth_token.auth,
                description=dict(description=desc),
                product_uid=product_uid
            )

            session.add(ticket)
            session.flush()

            response = ticket.to_json()

            self.write(response)


class TicketHandler(BaseHandler):

    @authenticated
    def get(self, ticket_uid):
        """
        Handler to get details of a ticket.

        Route - /api/ticket/<ticket-uid>
        Method - GET
        :param ticket_uid: id of the ticket to be returned
        :return: ticket details

        """
        with self.session_scope() as session:
            token = self.access_token_from_authorization_header()

            token = convert_uuid_or_400(token)

            auth_token = session.query(AuthToken).filter(AuthToken.uid == token).one_or_none()

            permissions = auth_token.auth.permissions

            if int(permissions[2]) != 1:
                raise tornado.web.HTTPError(409, 'Current user don\'t have permission to view tickets.')

            ticket = session.query(Ticket).filter(
                and_(
                    Ticket.uid == ticket_uid,
                    Ticket.is_deleted == False
                )
            ).one_or_none()

            if ticket:

                response = dict(
                    status=ticket.status,
                    type=ticket.type,
                    product_uid=str(ticket.product_uid),
                    description=ticket.description,
                    auth_uid=str(ticket.auth.uid),
                    uid=str(ticket.uid),
                    created_at=ticket.created_at.isoformat()

                )

                self.write(response)

            else:
                raise tornado.web.HTTPError(409, 'No Ticket found for {}'.format(ticket_uid))


    @authenticated
    def put(self, ticket_uid):
        """
        Handler to update the status and description  of a ticket.

        Route - /api/ticket/<ticket-uid>
        Method - PUT
        :param ticket_uid: id of the ticket to be returned
        :return: uid , timestamp of ticket

        """

        data = self.convert_argument_to_json()

        status = data.get('status', None)
        desc = data.get('desc', None)

        if not status or status not in Ticket.VALID_TICKET_STATUS:
            raise tornado.web.HTTPError(400,
                                        'Invalid status for ticket. Must be one of select_dev, in_progress or done')

        if not desc:
            raise tornado.web.HTTPError(400, 'Please provide description for the ticket.')

        with self.session_scope() as session:
            token = self.access_token_from_authorization_header()

            token = convert_uuid_or_400(token)

            auth_token = session.query(AuthToken).filter(AuthToken.uid == token).one_or_none()

            permissions = auth_token.auth.permissions

            if int(permissions[1]) != 1:
                raise tornado.web.HTTPError(409, 'Current user don\'t have permission to edit tickets.')

            ticket = session.query(Ticket).filter(
                and_(
                    Ticket.uid == ticket_uid,
                    Ticket.is_deleted == False
                )
            ).one_or_none()

            if ticket:
                description = dict(description=desc)

                ticket.status = status
                ticket.description=description

                session.flush()

                response = ticket.to_json()

                self.write(response)

            else:
                raise tornado.web.HTTPError(409, 'No Ticket found for {}'.format(ticket_uid))


    @authenticated
    def delete(self, ticket_uid):
        """
        Handler to delete a ticket for given ticket uid.

        Route - /api/ticket/<ticket-uid>
        Method - PUT
        :param ticket_uid: uid of the ticket to be deleted
        :return: uid, creted_at and deleted_at timestamp
        """

        with self.session_scope() as session:
            token = self.access_token_from_authorization_header()

            token = convert_uuid_or_400(token)

            auth_token = session.query(AuthToken).filter(AuthToken.uid == token).one_or_none()

            permissions = auth_token.auth.permissions

            if int(permissions[3]) != 1:
                raise tornado.web.HTTPError(409, 'Current user don\'t have permission to delete tickets.')

            ticket = session.query(Ticket).filter(
                and_(
                    Ticket.uid == ticket_uid,
                    Ticket.is_deleted == False
                )
            ).one_or_none()

            if ticket:
                ticket.mark_deleted()

                session.flush()

                response = ticket.to_json()
                response['deleted_at'] = ticket.deleted_at.isoformat()

                self.write(response)

            else:
                raise tornado.web.HTTPError(409, 'No Ticket found for {}'.format(ticket_uid))

