from sqlalchemy import Column, String, Integer, DateTime
from datetime import datetime
# from sqlalchemy_serializer import SerializerMixin

from models import Base


class Contact(Base):
    __tablename__ = "contacts"

    id = Column("contact_id", Integer, primary_key=True, autoincrement=True)
    firstname = Column(String(50))
    lastname = Column(String(50), nullable=True)
    phone = Column(String(20), unique=True)
    phone_type = Column(String(30), default="celular".lower())
    email = Column(String(100), nullable=True, unique=True)
    created_at = Column(DateTime, default=datetime.now())
    updated_at = Column(DateTime, nullable=True)

    def __init__(
        self,
        firstname: str,
        lastname: str,
        phone: str,
        phone_type: str,
        email: str,
    ):
        self.firstname = firstname
        self.lastname = lastname
        self.phone = phone
        self.phone_type = phone_type
        self.email = email
