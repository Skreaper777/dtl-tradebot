from sqlalchemy import Column, String, Integer, create_engine
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Person(Base):
    __tablename__ = 'person'
    id = Column(Integer, primary_key = True)
    name = Column(String(250), nullable=False)
    job = Column(String(250), nullable=False)

engine = create_engine('sqlite:///persons.sqlite')
session = sessionmaker()
session.configure(bind=engine)
Base.metadata.create_all(engine)

dct = {'John':'doctor', 'Alice':'typist'}

for el in dct:
    np = Person(name=el, job=dct[el])
    s = session()
    s.add(np)
    s.commit()