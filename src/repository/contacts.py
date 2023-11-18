from typing import List, Optional

from sqlalchemy.orm import Session
from sqlalchemy import and_, or_

from src.database.models import Contact
from src.schemas import ContactModel, ContactUpdate

from datetime import datetime, timedelta


async def get_contacts(skip: int, limit: int, db: Session) -> List[Contact]:
    return db.query(Contact).offset(skip).limit(limit).all()


async def search_contacts(
    db: Session,
    search_key: Optional[str] = None,
    name: Optional[str] = None,
    lastname: Optional[str] = None,
    email: Optional[str] = None
) -> List[Contact]:
    filters = {
        "name": name,
        "lastname": lastname,
        "email": email,
    }
    filters = {k: v for k, v in filters.items() if v is not None}

    contacts = db.query(Contact).filter(
        or_(
            Contact.name == search_key,
            Contact.lastname == search_key,
            Contact.email == search_key,
            **filters
        )).all()

    if email:
        contacts += db.query(Contact).filter(Contact.email == email).all()
    return contacts


async def get_contact(contact_id: int, db: Session) -> Contact:
    return db.query(Contact).filter(and_(Contact.id == contact_id)).first()


async def create_contact(body: ContactModel,  db: Session) -> Contact:
    contact = Contact(name=body.name, 
                      lastname=body.lastname, 
                      email=body.email, 
                      phone=body.phone, birthday=body.birthday)
    db.add(contact)
    db.commit()
    db.refresh(contact)
    return contact

async def remove_contact(contact_id: int, db: Session) -> Contact | None:
    contact = db.query(Contact).filter(and_(Contact.id == contact_id)).first()
    if contact:
        db.delete(contact)
        db.commit()
    return contact

async def update_contact(contact_id: int, body: ContactUpdate, db: Session) -> Contact | None:
    contact = db.query(Contact).filter(and_(Contact.id == contact_id)).first()
    
    if contact:
        # update only transmitted values
        for field, value in body.dict(exclude_unset=True).items():
            setattr(contact, field, value)
        
        db.commit()
    
    return contact


async def get_week_birthdays(db: Session) -> List[Contact]:
    contacts = db.query(Contact).all()

    matching_contacts = []
    for contact in contacts:    
        bd = datetime(year=datetime.now().year, 
                      month=contact.birthday.month, 
                      day=contact.birthday.day)

        delta = bd - datetime.now()
        week_delta = timedelta(days=7)

        if timedelta(days=0) <= delta <= week_delta:
            matching_contacts.append(contact)

    return matching_contacts