from sqlalchemy import Column, Integer, String, Float
from db.database import Base

class Movie(Base):
    __tablename__ = "movies"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    title = Column(String, index=True)
    overview = Column(String)
    year = Column(Integer)
    rating = Column(Float)
    category = Column(String)