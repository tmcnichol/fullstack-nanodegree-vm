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

#All Restaurants
@app.route('/restaurants/')
def restaurantList():
    return "This will return a list of all restaurants and link to menu"


#Restaurant Menu
@app.route('/restaurants/<int:restaurant_id>/menu')
def restaurantMenu(restaurant_id):
  return "This will return a specific restaurant's menu"


#Add Menu Item
@app.route('/restaurants/<int:restaurant_id>/new', methods=['GET', 'POST'])
def newMenuItem(restaurant_id):
    return "This will return a form to POST a new menu item"


#Edit Menu Item
@app.route('/restaurants/<int:restaurant_id>/<int:menu_id>/edit', methods=['GET', 'POST'])
def editMenuItem(restaurant_id, menu_id):
    return "This will return a form to POST an EDIT to a menu item"


#Delete Menu Item
@app.route('/restaurants/<int:restaurant_id>/<int:menu_id>/delete', methods=['GET', 'POST'])
def deleteMenuItem(restaurant_id, menu_id):
    return "This will return a confirmation page to DELETE a menu item"


#JSON all menu items
@app.route('/restaurants/<int:restaurant_id>/menu/JSON')
def restaurantMenuJSON(restaurant_id):
    return "This will return the JSON for all menu items"


#JSON for specific menu item(s)
@app.route('/restaurants/<int:restaurant_id>/menu/<int:menu_id>/JSON')
def menuItemJSON(restaurant_id, menu_id):
    return "This will return the JSON for a specific menu item(s)"


if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)