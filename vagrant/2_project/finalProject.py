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

#Show Restaurants
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


#Show Menu (for chosen restaurant)
@app.route('/restaurants/1/menu')
def showMenu():
    return render_template('showmenu.html', restaurant=restaurant, items=items)


#New Menu Item
@app.route('/restaurants/1/new', methods=['GET', 'POST'])
def newMenuItem():
    return render_template('newmenuitem.html', restaurant=restaurant, items=items)


#Edit Menu Item
@app.route('/restaurants/1/1/edit', methods=['GET', 'POST'])
def editMenuItem():
    return render_template('editmenuitem.html', restaurant=restaurant, item=item)


#Delete Menu Item
@app.route('/restaurants/1/1/delete', methods=['GET', 'POST'])
def deleteMenuItem():
    return render_template('deletemenuitem.html', restaurant=restaurant, item=item)


# #JSON all menu items
# @app.route('/restaurants/<int:restaurant_id>/menu/JSON')
# def restaurantMenuJSON(restaurant_id):
#     return "Return the JSON for all menu items"


# #JSON for specific menu item(s)
# @app.route('/restaurants/<int:restaurant_id>/menu/<int:menu_id>/JSON')
# def menuItemJSON(restaurant_id, menu_id):
#     return "Return the JSON for a specific menu item(s)"


if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)