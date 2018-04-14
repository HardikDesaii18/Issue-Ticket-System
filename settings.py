import os

settings = dict(
    db=dict(
        username=os.environ.get('username'),
        password=os.environ.get('password'),
        host=os.environ.get('host'),
        database='issue_ticket',
        port='5432'
    ),
    tornado=dict(
        debug=True,
    ),

    tornado_server_settings = {
        "xheaders" : False
    },
)
