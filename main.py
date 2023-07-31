from fastapi import FastAPI,Depends,HTTPException,status
from src.database.db import get_db
from sqlalchemy.orm import Session
from sqlalchemy import text,or_,func
from src.database.model import Contact
from src.schemas import ContactModel,ContactResponse
from typing import List
from datetime import datetime, timedelta

app= FastAPI()

@app.get("/api/healthchecker")
def healthchecker(db: Session = Depends(get_db)):
    try:
        result = db.execute(text("SELECT 1")).fetchone()
        if result is None:
            raise HTTPException(status_code=500, detail="Database is not configured correctly")
        return {"message": "Welcome to FastAPI!"}
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Error connecting to the database")


@app.post("/contact", response_model = ContactResponse)
async def add_contact(body :ContactModel, db: Session = Depends(get_db)):
    contact_email=db.query(Contact).filter_by(email=body.email).first()
    if contact_email:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email is exsisting",
        )
    contact_phone=db.query(Contact).filter_by(phone=body.phone).first()
    if contact_phone:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Phone is exsisting",
        )
    contact=Contact(name=body.name, email=body.email,surname=body.surname,
                    phone=body.phone,birthday=body.birthday,notes=body.notes)
    db.add(contact)
    db.commit()

    return contact


@app.get("/contacts", response_model = List[ContactResponse])
async def all_contacts(db: Session = Depends(get_db)):
    contacts=db.query(Contact).all()
    return contacts


@app.put("/contact/{contact_id}", response_model = ContactResponse)
async def update(contact_id : int,body:ContactModel,db: Session = Depends(get_db)):
    contact=db.query(Contact).filter_by(id=contact_id).first()
    if contact is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="NOT FOUND",
        )
    contact.name=body.name
    contact.email=body.email
    contact.surname=body.surname
    contact.phone=body.phone
    contact.birthday=body.birthday
    contact.notes=body.notes
    db.commit()
    return contact


@app.get("/contact/{elem}", response_model = List[ContactResponse])
async def search(elem : str,db: Session = Depends(get_db)):
    contact = db.query(Contact).filter(
            or_(
                Contact.name.ilike(f"%{elem}%"),
                Contact.surname.ilike(f"%{elem}%"),
                Contact.email.ilike(f"%{elem}%"),
            )
        ).all()
    if contact is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="NOT FOUND",
        )
    return contact


@app.delete("/contact/{contact_id}")
async def Delete(contact_id : int,db: Session = Depends(get_db)):
    contact=db.query(Contact).filter_by(id=contact_id).first()
    if contact is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="NOT FOUND",
        )
    db.delete(contact)
    db.commit()
    return contact



@app.get("/contacts/HB", response_model = List[ContactResponse])
async def HpB(db: Session = Depends(get_db)):
    current_date = datetime.now().date()
    end_date = current_date + timedelta(days=7)


    contacts = db.query(Contact).filter(or_(
            func.extract('month', Contact.birthday) >= current_date.month,
            func.extract('day', Contact.birthday) >= current_date.day,
            func.extract('day', Contact.birthday) <= end_date.day
        )
    ).all()

    return contacts
