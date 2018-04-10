from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
db = SQLAlchemy(app)

############################################################################

# here I create my models

class Restaurant(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(80), nullable=False)
  address = db.Column(db.String(80))
  stars = db.Column(db.Integer)



class MenuItem(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(80), nullable=False)
  course = db.Column(db.String(250))
  description = db.Column(db.String(250))
  price = db.Column(db.String(8))
  restaurant_id = db.Column(db.Integer, db.ForeignKey('restaurant.id'))
  restaurant = db.relationship(Restaurant)

############################################################################
               # HERE STARTS THE ROUTES FOR RESTAURANTS #
############################################################################


@app.route('/')
def allRestaurants():
  restaurant = db.session.query(Restaurant).filter_by(id=1).one()
  items = db.session.query(MenuItem).filter_by(restaurant_id=restaurant.id)
  return render_template('main_page.html', restaurant=restaurant, items=items)


@app.route('/restaurants/<int:restaurant_id>/')
def restaurant(restaurant_id):
  restaurant = db.session.query(Restaurant).filter_by(id=restaurant_id).one()
  items = db.session.query(MenuItem).filter_by(restaurant_id=restaurant_id)
  return render_template('restaurant_menu.html')


@app.route('/restaurants/new', methods=['GET', 'POST'])
def newRestaurant():
  if request.method == 'POST':
    newRestaurant = Restaurant(name=request.form['name'], address=request.form['address'], stars=request.form['stars'])
    db.session.add(newRestaurant)
    db.session.commit()
    flash("this restaurant was successfully created!")
    return redirect(url_for('allRestaurants'))
  else:
    return render_template('new_restaurant.html')


@app.route('/restaurants/edit/<int:restaurant_id>/', methods=['GET', 'POST'])
def editRestaurant(restaurant_id):
  restaurant = db.session.query(Restaurant).filter_by(id=restaurant_id).one()
  items = db.session.query(MenuItem).filter_by(restaurant_id=restaurant_id)
  if request.method == 'POST':
    pass
  else:
    pass


@app.route('/restaurants/delete/<int:restaurant_id>/', methods=['GET', 'POST'])
def restaurant_delete(restaurant_id):
  restaurant = db.session.query(Restaurant).filter_by(id=restaurant_id).one()
  if request.method == 'POST':
    db.session.delete(restaurant)
    db.session.commit()
    return "Restaurant deleted!"
  else:
    pass
 

############################################################################
                # HERE STARTS THE ROUTES FOR MENU ITEMS #
############################################################################


@app.route('/restaurants/<int:restaurant_id>/new', methods=['GET', 'POST'])
def newMenuItem(restaurant_id):
  if request.method == 'POST':
    newItem = MenuItem(name=request.form['name'], course=request.form['course'], price=request.form['price'], description=request.form['description'], restaurant_id=restaurant_id)
    db.session.add(newItem)
    db.session.commit()
    flash("this item was successfully created!")
    return redirect(url_for('restaurant', restaurant_id=restaurant_id))
  else:
    return render_template('new_menu_item.html', restaurant_id=restaurant_id)



@app.route('/restaurants/<int:restaurant_id>/edit_item/<int:item_id>', methods=['GET', 'POST'])
def editMenuItem(restaurant_id, item_id):
  item = db.session.query(MenuItem).filter_by(restaurant_id=restaurant_id).filter_by(id=item_id)
  if request.method == 'POST':
    if request.form['name']:
      item.name = request.form['name']
    if request.form['course']:
      item.course = request.form['course']
    if request.form['price']:
      item.price=request.form['price']
    if request.form['description']:
      item.description=request.form['description']
    db.session.commit()
    flash("this item was successfully edited!")
    return redirect(url_for('restaurant', restaurant_id=restaurant_id))
  else:
    return render_template('edit_menu_item.html', restaurant_id=restaurant_id, item_id=item_id, item=item)


@app.route('/restaurants/<int:restaurant_id>/delete/<int:item_id>')
def deleteMenuItem(restaurant_id, item_id):
  if request.method == 'POST':
    item = db.session.query(MenuItem).filter_by(restaurant_id=restaurant_id).filter_by(item_id=item_id)
    db.session.delete(item)
    db.session.commit()
    flash("this item was successfully deleted!")
    return redirect(url_for('restaurant', restaurant_id=restaurant_id))
  else:
    return render_template('delete_menu_item.html', restaurant_id=restaurant_id, item_id=item_id, item=item)



# THIS FUNCTION ABOVE IS JUST TO POPULATE MY DB - USED ONCE

def populate_restaurants_db():
  list_of_restaurants = ['The Silver Rooftop', 'The Summer Oriental', 'The Minty Tulip', 'The Wild Pond']
  menu_items = ['chicken pasta primavera', 'barcelona bbq', 'ceasar salad', 'ojo de bife']
  menu_description = ['delicious chicken with pasta primavera and alfredo sauce', 'wonderful bbq from chief barcelona', 'salad with sauce ceasar, cheese and croutons', 'delicious ojo de bife from argentina']
  menu_price = ['6.5', '7.8', '10.1', '50.3']
  for i in list_of_restaurants:
    try:
      rest = db.session.query(Restaurant).filter_by(name=i)
    except:    
      rest = Restaurant(name=i)
      db.session.add(rest)
      for item, desc, price in zip(menu_items, menu_description, menu_price):
        item_r = MenuItem(name=item, restaurant_id=rest.id, description=desc, price=price)
        db.session.add(item_r)
        db.session.commit()



if __name__ == '__main__':
  # create and populate the db:
  db.create_all()
  populate_restaurants_db()

  #include a key for our sessions:
  app.secret_key = "super_secret_key"

  app.debug = True
  app.run(host='0.0.0.0', port=5000)
