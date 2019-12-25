from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

url = 'postgresql://'

engine = create_engine(url)
Session = sessionmaker(bind=engine)
Base = declarative_base()