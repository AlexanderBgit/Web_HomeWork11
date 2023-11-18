from typing import List, Optional

from fastapi import APIRouter, HTTPException, Depends, status, Path
from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse

from src.database.conn_db import get_db
from src.schemas import ContactModel, ContactUpdate, ContactResponse
from src.repository import contacts as repository_contacts



router = APIRouter(prefix='/contacts')

# за замовчуванням
# @router.get("/", response_model=List[ContactResponse], name='return contacts1')
# async def get_contacts(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
#     contacts = await repository_contacts.get_contacts(skip, limit, db)
#     return contacts

@router.get("/", response_model=List[ContactResponse], name='return contacts2')
async def read_contacts(contact_id: int | None = None, db: Session = Depends(get_db)):
    if contact_id is not None:
        contact = await repository_contacts.get_contact(contact_id, db)
        if contact is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not Found")
        return [contact]
    else:
        contacts = await repository_contacts.get_contacts(0, 100, db)
        return contacts

# +
# @router.get("/{contact_id}", response_model=ContactResponse)
# async def read_contact(contact_id: int, db: Session = Depends(get_db)):
#     contact = await repository_contacts.get_contact(contact_id, db)
#     if contact is None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not Found")
#     return contact

@router.get("/{contact_id}", response_model=List[ContactResponse], name='get id')
async def read_contacts(contact_id: int | None = None, db: Session = Depends(get_db)):
    if contact_id is not None:
        contact = await repository_contacts.get_contact(contact_id, db)
        if contact is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not Found")
        return [contact]
    else:
        contacts = await repository_contacts.get_contacts(0, 100, db)
        return contacts

# +
@router.put("/{contact_id}", response_model=ContactResponse, name='update contacts')
async def update_contact(body: ContactUpdate, contact_id: int, db: Session = Depends(get_db)):
    contact = await repository_contacts.update_contact(contact_id, body, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not Found")
    return contact

# +
@router.post("/", response_model=ContactResponse, status_code=status.HTTP_201_CREATED)
async def create_contact(body: ContactModel, db: Session = Depends(get_db)):
    return await repository_contacts.create_contact(body, db)

# +
@router.delete("/{contact_id}", response_model=ContactResponse)
async def remove_contact(contact_id: int = Path(ge=1), db: Session = Depends(get_db)):
    contact = await repository_contacts.remove_contact(contact_id, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found")
    return contact

# +
@router.get("/search/", response_model=List[ContactResponse], name='search by params')
async def search_contacts(
    search_key: Optional[str] = None,
    name: Optional[str] = None,
    lastname: Optional[str] = None,
    email: Optional[str] = None,
    db: Session = Depends(get_db)
):
    contacts = await repository_contacts.search_contacts(
        search_key=search_key,
        name=name,
        lastname=lastname,
        email=email,
        db=db
    )
    return contacts

# +
@router.get("/week_birthdays/", response_model=List[ContactResponse], name='birthdays')
async def get_week_birthdays(db: Session = Depends(get_db)):
    contacts = await repository_contacts.get_week_birthdays(db)
    return contacts