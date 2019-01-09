from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import cgi
import time

# import CRUD Operations from Lesson 1
from database_setup import Base, Restaurant, MenuItem
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Create session and connect to DB
engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()


class webServerHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        try:
            if self.path.endswith("/restaurants"):
                restaurants = session.query(Restaurant).all()
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                output = ""
                output += "<html><body>"
                output += " <h1>My Restaurants</h1>"
                output += "<h3><a href='restaurants/new'>+Add New Restaurant</a></h3>"
                output += "</br>"
                for restaurant in restaurants:
                    output += restaurant.name
                    output += "<div><a href='/restaurants/%s/edit'>Edit</a></div>" % restaurant.id
                    output += "<div><a href='/restaurants/%s/delete'>Delete</a></div>" % restaurant.id
                    output += "</br></br></br>"

                output += "</body></html>"
                self.wfile.write(output)
                return
        
            if self.path.endswith("/restaurants/new"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                output = ""
                output += "<html><body>"
                output += " <h2>Add New Restaurant</h2>"
                output += '''<form method='POST' enctype='multipart/form-data' action='/restaurants/new'><input name="new-rest" type="text" ><input type="submit" value="Create"></form>'''

                output += "</body></html>"
                self.wfile.write(output)
                return

            if self.path.endswith("/edit"):
                restaurantIDPath = self.path.split("/")[2]
                myRestaurantQuery = session.query(Restaurant).filter_by(id = restaurantIDPath).one()
                if myRestaurantQuery:
                    self.send_response(200)
                    self.send_header('Content-type', 'text/html')
                    self.end_headers()
                    output = ""
                    output += "<html><body>"
                    output += "<div><a href='/restaurants'>Home</a></div>"
                    output += "</br></br></br>"
                    output += "<h2>Rename Restaurant</h2>"
                    output += '''<form method='POST' enctype='multipart/form-data' action='/restaurants/%s/edit'><input name="rename" type="text" ><input type="submit" value="Rename"></form>''' % myRestaurantQuery.id

                    output += "</body></html>"
                    self.wfile.write(output)
                    return

            if self.path.endswith("/delete"):
                restaurantIDPath = self.path.split("/")[2]
                myRestaurantQuery = session.query(Restaurant).filter_by(id = restaurantIDPath).one()
                if myRestaurantQuery:
                    self.send_response(200)
                    self.send_header('Content-type', 'text/html')
                    self.end_headers()
                    output = ""
                    output += "<html><body>"
                    output += "<div><a href='/restaurants'>Home</a></div>"
                    output += "</br></br></br>"
                    output += "<h2>Delete Restaurant</h2>"
                    output += "<h4>Are you sure you would like to permanently delete %s?</h4>" % myRestaurantQuery.name
                    output += '''<form method='POST' enctype='multipart/form-data' action='/restaurants/%s/delete'><input name="delete" type="submit" value="Delete"></form>''' % myRestaurantQuery.id

                    output += "</body></html>"
                    self.wfile.write(output)
                    return

        except IOError:
            self.send_error(404, 'File Not Found: %s' % self.path)
    
    def do_POST(self):
        try:
            if self.path.endswith("/edit"):
                ctype, pdict = cgi.parse_header(
                    self.headers.getheader('content-type'))
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    messagecontent = fields.get('rename')
                    restaurantIDPath = self.path.split("/")[2]
                    
                    myRestaurantQuery = session.query(Restaurant).filter_by(id = restaurantIDPath).one()
                    if myRestaurantQuery != []:
                        myRestaurantQuery.name = messagecontent[0]
                        session.add(myRestaurantQuery)
                        session.commit()
                        
                        self.send_response(301)
                        self.send_header('Content-type', 'text/html')
                        self.send_header('Location', '/restaurants')
                        self.end_headers()

                        return
            
            if self.path.endswith("/delete"):
                restaurantIDPath = self.path.split("/")[2]
                
                myRestaurantQuery = session.query(Restaurant).filter_by(id = restaurantIDPath).one()
                if myRestaurantQuery:
                    session.delete(myRestaurantQuery)
                    session.commit()

                    self.send_response(301)
                    self.send_header('Content-type', 'text/html')
                    self.send_header('Location', '/restaurants')
                    self.end_headers()

                    return

            if self.path.endswith("/restaurants/new"):
                ctype, pdict = cgi.parse_header(
                    self.headers.getheader('content-type'))
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    messagecontent = fields.get('new-rest')

                newRestaurant = Restaurant(name = messagecontent[0])
                session.add(newRestaurant)
                session.commit()
                
                self.send_response(301)
                self.send_header('Content-type', 'text/html')
                self.send_header('Location', '/restaurants')
                self.end_headers()

                return

        except:
            pass

def main():
    try:
        server = HTTPServer(('', 8080), webServerHandler)
        print 'Web server running...open localhost:8080/restaurants in your browser'
        server.serve_forever()
    except KeyboardInterrupt:
        print '^C received, shutting down server'
        server.socket.close()

if __name__ == '__main__':
    main()