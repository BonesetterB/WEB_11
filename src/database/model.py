from sqlalchemy import Column, Integer, String, Date
from .db import Base,engine

class Contact(Base):
    __tablename__ = 'contacts'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    surname = Column(String(100), nullable=False)
    email = Column(String(150),unique=True, nullable=False)
    phone = Column(String(20),unique=True,nullable=False)
    birthday = Column(Date,nullable=False)
    notes = Column(String(500),nullable=True)

Base.metadata.create_all(bind=engine)


