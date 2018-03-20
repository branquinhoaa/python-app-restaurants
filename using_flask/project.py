from flask import Flask
app = Flask(__name__)

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

# Here I will take care of the db:
engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

##########################################################

# Here I take care of my routes:

@app.route('/')
@app.route('/hello')
def HelloWorld():
  restaurants = session.query(Restaurant).all()
  output = ''
  for r in restaurants:
    output += '<h1>%s</h1>'%r.name
    items = session.query(MenuItem).filter_by(restaurant_id = r.id)
    for i in items:
      output += '<li>%s</li>'%i.name
      output += '</br>'

  return output

def populate_restaurants_db():
  list_of_restaurants = ['The Silver Rooftop', 'The Summer Oriental', 'The Minty Tulip', 'The Wild Pond']
  menu_items = ['chicken pasta primavera', 'barcelona bbq', 'ceasar salad', 'ojo de bife']
  menu_description = ['delicious chicken with pasta primavera and alfredo sauce', 'wonderful bbq from chief barcelona', 'salad with sauce ceasar, cheese and croutons', 'delicious ojo de bife from argentina']
  menu_price = ['6.5', '7.8', '10.1', '50.3']
  for i in list_of_restaurants:
    rest = Restaurant(name=i)
    session.add(rest)
    session.commit()
    for item, desc, price in zip(menu_items, menu_description, menu_price):
      item_r = MenuItem(name=item, restaurant_id=rest.id, description=desc, price=price)
      session.add(item_r)
      session.commit()



if __name__ == '__main__':
  # populate the db:
  populate_restaurants_db()

  app.debug = True
  app.run(host='0.0.0.0', port=5000)
