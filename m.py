from datetime import datetime, timedelta
from src.database.db import Session
from src.database.model import Contact
from sqlalchemy import  Date,extract,cast,func,or_
from datetime import datetime,date

current_date = datetime.now().date()
current_year=current_date.year
# Отримуємо дату через 7 днів
end_date = current_date + timedelta(days=7)

def birthday_this_year(birthday_date):
        return birthday_date.replace(year=current_year)

if datetime.strptime("2023-08-05", "%Y-%m-%d").date()>current_date:
    Session=Session()
    contacts = Session.query(Contact).filter(
        or_(
            func.extract('month', Contact.birthday) >= current_date.month,
            func.extract('day', Contact.birthday) >= current_date.day,
            func.extract('day', Contact.birthday) <= end_date.day
        )
    ).all()
    for i in contacts:
        print(i.name)
        print(i.birthday)
        print(i.id)
    Session.close()
# contacts = db.query(Contact).filter(Contact.birthday >= current_date, Contact.birthday <= end_date).all()