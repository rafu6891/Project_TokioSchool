"""This module sets up and establishes a connection to the SQlite database using SQLAlchemy.
It also prepares the sessions for database interactions and sets up the base class for ORM models."""


from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

#Setting up the SQLAlchemy engine to connect to 'usuarios.db' in SQLite.
engine = create_engine('sqlite:///database/usuarios.db', connect_args={'check_same_thread': False})

#Creating a session factory bound to the database engine.
Session = sessionmaker(bind=engine)

#Creating a session instance that can be used to interact with the database.
session = Session(bind=engine)

#Setting up the base class for declarative ORM.
Base = declarative_base()

