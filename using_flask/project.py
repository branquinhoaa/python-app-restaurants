from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
db = SQLAlchemy(app)

# here I create my models


class Restaurant(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(80), nullable=False)


class MenuItem(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(80), nullable=False)
  course = db.Column(db.String(250))
  description = db.Column(db.String(250))
  price = db.Column(db.String(8))
  restaurant_id = db.Column(db.Integer, db.ForeignKey('restaurant.id'))
  restaurant = db.relationship(Restaurant)

###########################################################################

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
#from database_setup import Base, Restaurant, MenuItem


# Here I will take care of the db:

##########################################################

# Here I take care of my routes:

@app.route('/')
def HelloWorld():
  restaurants = db.session.query(Restaurant).all()
  print(len(restaurants))
  output = ''
  for r in restaurants:
    output += '<h1>%s</h1>'%r.name
    items = db.session.query(MenuItem).filter_by(restaurant_id = r.id)
    for i in items:
      output += '<li>%s - %s : $ %s</li>'%(i.name, i.description, i.price)
      output += '</br>'

  return output

def populate_restaurants_db():
  list_of_restaurants = ['The Silver Rooftop', 'The Summer Oriental', 'The Minty Tulip', 'The Wild Pond']
  menu_items = ['chicken pasta primavera', 'barcelona bbq', 'ceasar salad', 'ojo de bife']
  menu_description = ['delicious chicken with pasta primavera and alfredo sauce', 'wonderful bbq from chief barcelona', 'salad with sauce ceasar, cheese and croutons', 'delicious ojo de bife from argentina']
  menu_price = ['6.5', '7.8', '10.1', '50.3']
  for i in list_of_restaurants:
    try:
      rest = db.session.query(Restaurant).filter_by(name=i)
    except:    
      print(i)
      rest = Restaurant(name=i)
      db.session.add(rest)
      db.session.commit()
      for item, desc, price in zip(menu_items, menu_description, menu_price):
        item_r = MenuItem(name=item, restaurant_id=rest.id, description=desc, price=price)
        db.session.add(item_r)
        db.session.commit()



if __name__ == '__main__':
  # create and populate the db:
  # db.create_all()
  populate_restaurants_db()

  app.debug = True
  app.run(host='0.0.0.0', port=5000)
