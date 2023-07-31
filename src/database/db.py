from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
import configparser

config = configparser.ConfigParser()
config.read('config.ini')

user = config.get('DB', 'USER')
passWOrd = config.get('DB', 'PASSWORD')
host = config.get('DB', 'HOST')
port = config.get('DB', 'PORT')
name=config.get('DB', 'NAME')


class Base(DeclarativeBase):
    pass

engine = create_engine(f'postgresql://{user}:{passWOrd}@{host}:{port}/{name}')

Session = sessionmaker(bind=engine)

def get_db():
    db=Session()
    try:
        yield db
    finally:
        db.close()


