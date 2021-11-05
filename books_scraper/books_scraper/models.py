from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.engine.base import Engine
from sqlalchemy.engine.url import URL
from sqlalchemy.ext.declarative import declarative_base
from books_scraper import settings

DeclarativeBase = declarative_base()

def db_connect():
	return create_engine(URL(**settings.DATABASE))

def create_items_table(engine: Engine):
	DeclarativeBase.metadata.create_all(engine)

class Items(DeclarativeBase):
	__tablename__ = "items"
	name = Column("name", String, primary_key=True)
	price = Column("price", Integer)
	