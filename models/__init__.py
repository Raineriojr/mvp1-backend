from sqlalchemy_utils import database_exists, create_database
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

import os

from models.base import Base
from models.contacts import Contact

db_path = "database/"
db_url = "sqlite:///%s/db.sqlite3" % db_path

if not os.path.exists(db_path):
    os.makedirs(db_path)

engine = create_engine(db_url, echo=False)

Session = sessionmaker(bind=engine)

if not database_exists(db_url):
    create_database(db_url)

Base.metadata.create_all(engine)
