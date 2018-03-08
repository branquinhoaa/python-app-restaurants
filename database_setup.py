import sys

from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import create_engine

Base = declarative_base()
###########################

class Restaurant(Base):
  __tablename__='restaurant'
  name = Column(String(80), nullable = False)
  id = Column(Integer, primary_key = True)




class MenuItem(Base):
  __tablename__='menu_item'
  name = Column(String(80), nullable = False)
  id = Column(Integer, primary_key = True)
  course = Column(String(250))
  description = Column(String(250))
  price = Column(String(8))
  restaurant_id = Column(Integer, ForeignKey('restaurant.id'))
  restaurant = relationship(Restaurant)



###########################

engine = create_engine('sqlite:///restaurants_for_list.db')
Base.metadata.create_all(engine)


#DBSession = sessionmaker(bind=engine)

#session = DBSession()

#for i in range(10):
#    restaurant = Restaurant(name="Restaurante%i"%i)
#    session.add(restaurant)
#    session.commit()