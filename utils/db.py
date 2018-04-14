import logging
from contextlib import contextmanager

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import sqlalchemy_utils

Session = sessionmaker()

class Db:
    def __init__(self, **kwargs):
        all_settings = dict()

        if kwargs:
            all_settings.update(kwargs)

        urlstr = "postgresql://{username}:{password}@{host}:{port}/{database}"

        self.database_url = urlstr.format(**all_settings)

        self.settings = all_settings

        self.engine = create_engine(
            self.database_url,
            echo = all_settings.get('echo', False)
        )
        Session.configure(bind=self.engine)

    def create_database(self):
        conn = self.engine.connect()
        conn.execute('commit')
        conn.execute("create database {database}".format(**self.settings))
        conn.close()

    def drop_database(self):
        sqlalchemy_utils.functions.drop_database(self.database_url)

    def create_tables(self, metadata):
        metadata.create_all(self.engine)

    def drop_tables(self, metadata):
        metadata.drop_all(self.engine)

    def create_all(self, metadata):
        metadata.create_all(self.engine)

    def drop_all(self, metadata):
        metadata.drop_all(self.engine)

    def session(self):
        return Session()

    @contextmanager
    def session_scope(self):
        """Provide a database scope for operations."""
        session = Session()

        try:
            yield session
            session.commit()

        except Exception as e:

            session.rollback()
            raise

        finally:
            session.close()
