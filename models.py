"""
User Model Module.

Defines the User ORM model for a gaming system, with methods for password 
verification and custom database querying. Relies on SQLAlchemy for database 
operations and werkzeug for password security.
"""


from datetime import datetime
from sqlalchemy.orm import Query
from sqlalchemy import Column, Integer, String, Date, Boolean
import db
from werkzeug.security import check_password_hash

class User(db.Base):
    """
    Represents a user within the system, containing fields for storing information
    related to the user, their games and administrative privileges.
    """
    __tablename__ = 'usuarios'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    password = Column(String, nullable=False)
    email = Column(String(100), nullable=False)
    antiquity = Column(Date, default=datetime.today, nullable=False)
    ranking = Column(Integer, default=0, nullable=False)
    tetris_count = Column(Integer, default=0)
    cod_count = Column(Integer, default=0)
    is_admin = Column(Boolean, default=False)


    def __init__(self, name, password, email,games="Tetris,COD",  is_admin=False):
        """
        Initializes a new user instance.
        """
        self.name = name
        self.password = password
        self.email = email
        self.games = games
        self.is_admin = is_admin

    def check_password(self, password):
        """
        Checks if the provided password matches the stored hashed password.
        """
        return check_password_hash(self.password, password)

    @classmethod
    def custom_query(cls) -> Query:
        """
        Returns a custom query object for the User class.
        """
        return db.session.query(cls)

