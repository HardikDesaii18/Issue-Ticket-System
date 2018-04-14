settings = dict(
    db=dict(
        username='hardikdesai',
        password='Pulsar@2729',
        host='postgresinstance.cxjyukbuyrhv.us-east-1.rds.amazonaws.com',
        database='issue_ticket',
        port='5432'
    ),
    tornado=dict(
        debug=True,
    ),
    # todo CHECK WHAT DO IS changes
    tornado_server_settings = {
        "xheaders" : False
    },
)
