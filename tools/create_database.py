#!/usr/bin/env python
import os.path
import sys

from settings import settings
from utils.db import Db

sys.path.append(os.getcwd())


def main():
    db_settings = settings['db']

    db = Db(**db_settings)

    print("Creating DB tables...")
    from models import Base

    db.drop_tables(Base.metadata)
    db.create_tables(Base.metadata)

    print('Done!')

if __name__ == "__main__":
    main()
