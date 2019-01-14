from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from database_setup import Base, Restaurant, MenuItem

app = Flask(__name__)

engine = create_engine('sqlite:///restaurantmenu.db',
    connect_args={'check_same_thread': False},
    poolclass=StaticPool, echo=True)
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


#Show Restaurants
@app.route('/restaurants/')
def showRestaurants():
    restaurants = session.query(Restaurant)
    return render_template('showrestaurants.html', restaurants=restaurants)


#New Restaurant
@app.route('/restaurant/new', methods=['GET', 'POST'])
def newRestaurant():
    if request.method == 'POST':
        newRest = Restaurant(name=request.form['name'])
        session.add(newRest)
        session.commit()
        flash("new restaurant created!")
        return redirect(url_for('showRestaurants'))
    else:
        return render_template('newrestaurant.html')


#Edit Restaurant
@app.route('/restaurant/1/edit', methods=['GET', 'POST'])
def editRestaurant():
    return render_template('editrestaurant.html', restaurant=restaurant)


#Delete Restaurant
@app.route('/restaurant/1/delete', methods=['GET', 'POST'])
def deleteRestaurant():
     return render_template('deleterestaurant.html', restaurant=restaurant)


#Show Menu (for chosen restaurant)
@app.route('/restaurants/<int:restaurant_id>/menu')
def showMenu(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).all()
    items = session.query(MenuItem).filter_by(restaurant_id=restaurant_id)
    return render_template(
        'showmenu.html', restaurant=restaurant, items=items, restaurant_id=restaurant_id)


#New Menu Item
@app.route('/restaurants/<int:restaurant_id>/new', methods=['GET', 'POST'])
def newMenuItem(restaurant_id):
    if request.method == 'POST':
        newItem = MenuItem(name=request.form['name'], description='tastey delights sprinkled with flavor crystals!', 
            price='$100.00', course='ten course', restaurant_id=restaurant_id)
        session.add(newItem)
        session.commit()
        flash("new menu item created!")
        return redirect(url_for('showMenu', restaurant_id=restaurant_id))
    else:
        return render_template('newmenuitem.html', restaurant_id=restaurant_id)


#Edit Menu Item
@app.route('/restaurants/<int:restaurant_id>/<int:menu_id>/edit', methods=['GET', 'POST'])
def editMenuItem(restaurant_id, menu_id):
    editedItem = session.query(MenuItem).filter_by(id=menu_id).one()
    if request.method == 'POST':
        if request.form['name']:
            editedItem.name = request.form['name']
        session.add(editedItem)
        session.commit()
        flash("menu item edited!")
        return redirect(url_for('showMenu', restaurant_id=restaurant_id))
    else:
        return render_template(
            'editmenuitem.html', restaurant_id=restaurant_id, menu_id=menu_id, item=editedItem)


#Delete Menu Item
@app.route('/restaurants/1/1/delete', methods=['GET', 'POST'])
def deleteMenuItem():
    return render_template('deletemenuitem.html', restaurant=restaurant, item=item)


#JSON all menu items
@app.route('/restaurants/<int:restaurant_id>/menu/JSON')
def restaurantMenuJSON(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).all()
    items = session.query(MenuItem).filter_by(restaurant_id=restaurant_id)
    return jsonify(MenuItems=[i.serialize for i in items])


#JSON for specific menu item(s)
@app.route('/restaurants/<int:restaurant_id>/menu/<int:menu_id>/JSON')
def menuItemJSON(restaurant_id, menu_id):
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).all()
    item = session.query(MenuItem).filter_by(id=menu_id).one()
    return jsonify(item.serialize)


if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)