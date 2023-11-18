from sqlalchemy import (
    Boolean, 
    Column, 
    ForeignKey, 
    Integer, 
    String, 
    DateTime, 
    func, 
    event, 
    Date
    )
from sqlalchemy.orm import relationship, declarative_base


Base = declarative_base()


class Contact(Base):
    # mandatory data
    __tablename__ = "contacts"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    lastname = Column(String)
    email = Column(String, unique=True, index=True)
    phone = Column(String, default="None", nullable=False)
    birthday = Column(Date, default=None, nullable=True)
    
    # optional data
    age = Column(Integer)
    additional = Column(String, default="None", nullable=False)
    description = Column(String, default="None", index=True)
    created_at = Column(DateTime, default=func.now())  
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

