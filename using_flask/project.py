from flask import Flask, render_template, request, redirect, url_for
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


class MenuItem(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(80), nullable=False)
  course = db.Column(db.String(250))
  description = db.Column(db.String(250))
  price = db.Column(db.String(8))
  restaurant_id = db.Column(db.Integer, db.ForeignKey('restaurant.id'))
  restaurant = db.relationship(Restaurant)

############################################################################

# THE FUNCTIONS HERE ARE THE MAIN OPERATIONS THAT CAN BE DONE WITH MY RESTAURANTS

@app.route('/')
def allRestaurants():
  restaurant = db.session.query(Restaurant).filter_by(id=1).one()
  items = db.session.query(MenuItem).filter_by(restaurant_id=restaurant.id)

  return render_template('main_page.html', restaurant=restaurant, items=items)

@app.route('/restaurants/<int:restaurant_id>/')
def restaurant(restaurant_id):
  restaurant = db.session.query(Restaurant).filter_by(id=restaurant_id).one()
  items = db.session.query(MenuItem).filter_by(restaurant_id=restaurant_id)
  edit = '/restaurants/edit/%i'%restaurant_id
  delete = '/restaurants/delete/%i'%restaurant_id
  output = '<h1>%s</h1>'%restaurant.name
  output += '<a href = %s>Edit</a> </br>'%edit
  output += '<a href = %s>Delete</a></br>'%delete

  for i in items:
    output += '<li>%s - %s : $ %s</li>'%(i.name, i.description, i.price)
    output += '</br>'
  return output


@app.route('/restaurants/edit/<int:restaurant_id>/')
def restaurant_edit(restaurant_id):
  restaurant = db.session.query(Restaurant).filter_by(id=restaurant_id).one()
  items = db.session.query(MenuItem).filter_by(restaurant_id=restaurant_id)
  url = '/restaurants/update/<int:restaurant_id>/'
  message = ""
  message += "<h1>Edit your restaurant!</h1>"
  message += '''<form method='POST' enctype='multipart/form-data' action=%s>
  <h2>Change here the restaurant name</h2><input name="rest_name" type="text" > </br>
  <input type="submit" value="Submit"> </form>'''%url
  return message


@app.route('/restaurants/update/<int:restaurant_id>/')
def restaurant_update(restaurant_id):
  restaurant = db.session.query(Restaurant).filter_by(id=restaurant_id).one()
  restaurant.name = 'newname'
  db.session.commit()
 
  message += "<h1>Restaurant edited!</h1>"

  return message


@app.route('/restaurants/delete/<int:restaurant_id>/')
def restaurant_delete(restaurant_id):
  restaurant = db.session.query(Restaurant).filter_by(id=restaurant_id).one()
  db.session.delete(restaurant)
  db.session.commit()
  return "Restaurant deleted!"


### HERE STARTS THE ROUTES FOR MENU ITEMS ###

@app.route('/restaurants/<int:restaurant_id>/new', methods=['GET', 'POST'])
def newMenuItem(restaurant_id):
  if request.method == 'POST':
    newItem = MenuItem(name=request.form['name'], course=request.form['course'], price=request.form['price'], description=request.form['description'], restaurant_id=restaurant_id)
    db.session.add(newItem)
    db.session.commit()
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
    return redirect(url_for('restaurant', restaurant_id=restaurant_id))
  else:
    return render_template('edit_menu_item.html', restaurant_id=restaurant_id, item_id=item_id, item=item)


@app.route('/restaurants/<int:restaurant_id>/delete/<int:item_id>')
def deleteMenuItem(restaurant_id, item_id):
  if request.method == 'POST':
    item = db.session.query(MenuItem).filter_by(restaurant_id=restaurant_id).filter_by(item_id=item_id)
    db.session.delete(item)
    db.session.commit()
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

  app.debug = True
  app.run(host='0.0.0.0', port=5000)
