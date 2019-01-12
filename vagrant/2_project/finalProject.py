from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from database_setup import Base, Restaurant, MenuItem

app = Flask(__name__)

restaurant = {'name': 'The CRUDdy Crab', 'id': '1'}

restaurants = [{'name': 'The CRUDdy Crab', 'id': '1'}, {'name':'Blue Burgers', 'id':'2'},{'name':'Taco Hut', 'id':'3'}]


#Fake Menu Items
items = [ {'name':'Cheese Pizza', 'description':'made with fresh cheese', 'price':'$5.99','course' :'Entree', 'id':'1'}, {'name':'Chocolate Cake','description':'made with Dutch Chocolate', 'price':'$3.99', 'course':'Dessert','id':'2'},{'name':'Caesar Salad', 'description':'with fresh organic vegetables','price':'$5.99', 'course':'Entree','id':'3'},{'name':'Iced Tea', 'description':'with lemon','price':'$.99', 'course':'Beverage','id':'4'},{'name':'Spinach Dip', 'description':'creamy dip with fresh spinach','price':'$1.99', 'course':'Appetizer','id':'5'} ]
item =  {'name':'Cheese Pizza','description':'made with fresh cheese','price':'$5.99','course' :'Entree'}

#All Restaurants
@app.route('/restaurants/')
def showRestaurants():
    return render_template(
        'showrestaurants.html', restaurants=restaurants)


#New Restaurant
@app.route('/restaurant/new')
def newRestaurant():
    return render_template('newrestaurant.html', restaurant=restaurant)


#Edit Restaurant
@app.route('/restaurant/1/edit', methods=['GET', 'POST'])
def editRestaurant():
    return render_template('editrestaurant.html', restaurant=restaurant)


#Delete Restaurant
@app.route('/restaurant/1/delete', methods=['GET', 'POST'])
def deleteRestaurant():
    return render_template('deleterestaurant.html', restaurant=restaurant)


#Restaurant Menu
@app.route('/restaurants/<int:restaurant_id>/menu')
def showMenu(restaurant_id):
  return "Return a specific restaurant's menu"


#Add Menu Item
@app.route('/restaurants/<int:restaurant_id>/new', methods=['GET', 'POST'])
def newMenuItem(restaurant_id):
    return "Return a form to POST a new menu item"


#Edit Menu Item
@app.route('/restaurants/<int:restaurant_id>/<int:menu_id>/edit', methods=['GET', 'POST'])
def editMenuItem(restaurant_id, menu_id):
    return "Return a form to POST an EDIT to a menu item"


#Delete Menu Item
@app.route('/restaurants/<int:restaurant_id>/<int:menu_id>/delete', methods=['GET', 'POST'])
def deleteMenuItem(restaurant_id, menu_id):
    return "Return a confirmation page to DELETE a menu item"


#JSON all menu items
@app.route('/restaurants/<int:restaurant_id>/menu/JSON')
def restaurantMenuJSON(restaurant_id):
    return "Return the JSON for all menu items"


#JSON for specific menu item(s)
@app.route('/restaurants/<int:restaurant_id>/menu/<int:menu_id>/JSON')
def menuItemJSON(restaurant_id, menu_id):
    return "Return the JSON for a specific menu item(s)"


if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)