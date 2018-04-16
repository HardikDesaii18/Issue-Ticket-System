### Issue Ticket System

 This POC is created using the following
 
   1. Python framework Tornado.
   2. PostgreSQL databse hosted on AWS RDS.
   3. ORM SqlAlchemy


## Data Models

### Auth   

- User Authentication models, Having the following fields:
        
        uid - uuid primary key field
        created_at - timestamp
        email - email of the user
        password - 128 bit hashed password
        permissions - 4 BIT permission for ticket access


### AuthToken

- Auth token for the user that is provided on successfull login or signup.
- It's is needed to access the Product and Ticket modules of the application.

         uid - uuid primary key
         auth - relationship with model Auth
         auth_uid - Foreign key for Auth      
         created_at - timestamp
         token_type - type of the token, for now type is authentication
         is_deleted - bool field to know if token deleted or not
         deleted_at - delete timestamp


### Product

- Product can be any software system for which tickets can be created.

        uid - uuid primary field
        created_at - timestamp
        name - name of the product
        type - can be one of health_care, banking or others.
        owner_email - email of the product owner.
        is_deleted - bool field to know if product deleted or not
        deleted_at - delete timestamp


### Ticket

- Tickets can be created for the model Product

        uid - uuid primary field
        created_at - timestamp
        status - either of select_dev, in_progress or done.
        type- either of Bug, Enhancement or Feature.
        product_uid - Foreign key for model Product 
        auth_uid - Foreign key for model Auth
        description - JSON field storing the description of ticket.
        is_deleted - bool field to know if product deleted or not
        deleted_at - delete timestamp
        

## Routes

 ```
    Route - https://issue-ticket.herokuapp.com/api/sign-up
    Method - POST
    Params -
            email - Unique email for which user's account to be created.
            password - Any passphrase having min 6 characters.

    :returns: token, uid, timestamp of the newly created user.
    

```
```
    Route - https://issue-ticket.herokuapp.com/api/sign-in
    Method - POST
    Params:
        email : User's email for which account was created.
        password : User's password provided during signup.
    
    :returns: token, uid and timestamp of the logged in user.

```

- All the following route requires `Authorization` header and value `Bearer <Auth-token>`

```
   Handler to change the permission of the user. Pass the user access token in the Authorization Header.
   
   Route - https://issue-ticket.herokuapp.com/api/edit-user
   Method - PUT
   Params -
       Authorization - Bearer User Access Token received during login or signup
       permissions -  Int array of length 4, must only contain 0 or 1. 
               
   :returns: - uid, timestamp of the user
```

```
    Handler to list all the products.
    
    Route - https://issue-ticket.herokuapp.com/api/product
    Method - GET
    :return: list of non-deleted products

```

```
    Handler to create new product.
    
    Route - https://issue-ticket.herokuapp.com/api/product
    Method - POST
           
    :param:
            name - Name of the product
            type - Type of the product, Must be health_care, banking, others
            email - Owners email of the Product.


    :return: uid, timestamp of the product created.
```

```
    Handler to get the product details for th given product uid.
      
    Route - https://issue-ticket.herokuapp.com/api/product/<product-uid>
    Method - GET
    :param product_uid: uid of the product
    :return: json of the product.

```

```
    Handler to edit the product.
        
    Route - https://issue-ticket.herokuapp.com/api/product/<product-uid>
    Method - PUT
    :param product_uid: uid of the product to edit
    :return: uid, timestamp of the edited product

```

```
    Handler to delete the product.
    
    Route - https://issue-ticket.herokuapp.com/api/product/<product-uid>
    Method - DELETE
    :param product_uid: uid of the product to delete.
    :return: uid, created_at and deleted_at timestamp of product.
```

```
    Handler to get all the tickets if the user has permission to view tickets.
    Route - https://issue-ticket.herokuapp.com/api/ticket
    Method- GET
        
    :return: list of tickets
```                

```
    Handler to create new Ticket.
        
    Route - https://issue-ticket.herokuapp.com/api/ticket
    Method- POST

    :param:
        status - either of select_dev, in_progress or done.
        type- either of Bug, Enhancement or Feature.
        product_uid - Foreign key for model Product 
        description - JSON field storing the description of ticket.

        :return: uid, timestamp of the ticket created.

```

```
    Handler to get details of a ticket.
         
    Route - https://issue-ticket.herokuapp.com/api/ticket/<ticket-uid>
    Method - GET
    :param ticket_uid: id of the ticket to be returned
    :return: ticket details

```

```
    Handler to update the status and description  of a ticket.
         
    Route - https://issue-ticket.herokuapp.com/api/ticket/<ticket-uid>
    Method - PUT
    :param ticket_uid: id of the ticket to be returned
    :return: uid , timestamp of ticket 
```

```
    Handler to delete a ticket for given ticket uid.
         
    Route - https://issue-ticket.herokuapp.com/api/ticket/<ticket-uid>
    Method - PUT
    :param ticket_uid: uid of the ticket to be deleted
    :return: uid, creted_at and deleted_at timestamp
```         