import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

sqliteName = "movies.sqlite"
base_dir = os.path.dirname(os.path.abspath(__file__))
dataBaseURL = f"sqlite:///{os.path.join(base_dir, sqliteName)}"

engine = create_engine(dataBaseURL, connect_args={"check_same_thread": False})

Session = sessionmaker(bind=engine)

Base = declarative_base()