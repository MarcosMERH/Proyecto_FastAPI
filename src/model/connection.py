from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm.exc import NoResultFound

class Connection:
    
    def __init__(self):
        try:
            DB_NAME = "universidad" 
            DB_ROOT = "root"
            DB_HOST = "127.0.0.1"
            DB_PORT = "3306"
            CONN_DB = f"mysql+pymysql://{DB_ROOT}:@{DB_HOST}:{DB_PORT}/{DB_NAME}"
            self.engine = create_engine(CONN_DB)
            print('Conexión exitosa')
        except NoResultFound as Err:
            print(Err)
            print('Conexión fallida')