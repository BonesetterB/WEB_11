from datetime import datetime, timedelta
from db import Session
from model import Contact
from sqlalchemy import cast, Date

current_date = datetime.now().date()

# Отримуємо дату через 7 днів
end_date = current_date + timedelta(days=7)
print(current_date)

print(end_date)
if datetime.strptime("2023-08-05", "%Y-%m-%d").date()>current_date:
    # Depends(get_db)
    Session=Session()
    contacts = Session.query(Contact).filter(cast(Contact.birthday, Date) >= current_date, cast(Contact.birthday, Date) <= end_date).all()

    for i in contacts:
        print(i.name)
        print(i.birthday)
        print(i.phone)
        print(i.email)
        print(i.surname)
        print(i.notes)
        print(i.id)
    Session.close()
# contacts = db.query(Contact).filter(Contact.birthday >= current_date, Contact.birthday <= end_date).all()
