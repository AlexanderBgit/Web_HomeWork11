from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException, status


# PostgreSQL database info: maybe into config.ini config.get('DB', 'user')
db_username = 'postgres'
db_password = 'gfhjkm'
db_name = 'rest_api' #hw11 перейменувати після запуску докер імейдж
domain = 'localhost' 


ALCHEMY_DB_URL = f"postgresql+psycopg2://{db_username}:{db_password}@localhost:5432/{db_name}"
# f'postgresql://{username}:{password}@{domain}:{port}/{db_name}'


# engine = create_engine(ALCHEMY_DB_URL, echo=True)
engine = create_engine(ALCHEMY_DB_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine) #загальне по документації


def get_db():
    db = SessionLocal()
    try:
        yield db
    except SQLAlchemyError as err:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(err))
    finally:
        db.close()



# альтернативний спосіб підключення з викоистанням config.ini
# import configparser
# import pathlib

# file_config = pathlib.Path(__file__).parent.joinpath('config.ini')
# config = configparser.ConfigParser()
# config.read(file_config)
# SQLALCHEMY_DATABASE_URL = config.get('DB', 'url')
