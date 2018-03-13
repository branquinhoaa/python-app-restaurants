from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from database_setup import Restaurant, Base
from sqlalchemy import create_engine
engine = create_engine('sqlite:///restaurants_for_list.db')
from sqlalchemy.orm import sessionmaker
DBSession = sessionmaker()
DBSession.bind = engine
session = DBSession()

Base.metadata.bind = engine
import cgi

class WebServerHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        if self.path.endswith("/restaurants"):
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            restaurants = session.query(Restaurant).all()
            message = ""
            message += "<html><body>All The restaurants!<a href = '/new_restaurant'>Create a new one</a>"
            for i in restaurants:
                url_edit = "/%s/edit" %str(i.id)
                url_delete = "/%s/delete" %str(i.id)
                message += "<li>%s <a href =%s>Edit</a> <a href = %s>Delete</a></li>" %(str(i.name), url_edit, url_delete)           
            message += "</body></html>"
            self.wfile.write(message)
            print message
            return

        if self.path.endswith("/edit"):
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            rest_id = self.path.split('/')[-2]
            url = "/restaurant/%s/edit"%rest_id
            message = ""
            message += "<html><body>Edit your restaurant!<a href = %s>Back to restaurants page</a>"%url
            message += '''<form method='POST' enctype='multipart/form-data' action=%s><h2>Change here the restaurant name</h2><input name="rest_name" type="text" ><input type="submit" value="Submit"> </form>'''%url
            message += "</body></html>"
            self.wfile.write(message)
      
        if self.path.endswith("/new_restaurant"):
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            message = ""
            message += "<html><body>Make a  new restaurant!<a href = '/restaurants/new'>Back to restaurants page</a>"
            message += '''<form method='POST' enctype='multipart/form-data' action='/restaurants/new'><h2>Put here the restaurant name</h2><input name="new_restaurant" type="text" ><input type="submit" value="Submit"> </form>'''
            message += "</body></html>"
            self.wfile.write(message)
            print message
            return
    
        if self.path.endswith('/delete'):
            rest_id = self.path.split('/')[-2]
            restaurant = session.query(Restaurant).filter_by(id=rest_id)
            session.delete(restaurant)
            session.commit()
            output = ""
            output += "<html><body>"
            output += " <h2> Your restaurant was deleted successfully! </h2>"
            output += "</body></html>"
            self.wfile.write(output)
            print output

        else:
            self.send_error(404, 'File Not Found: %s' % self.path)


    def do_POST(self):
        try:
            if self.path.endswith('/restaurants/new'):
                ctype, pdict = cgi.parse_header(
                    self.headers.getheader('content-type'))
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    messagecontent = fields.get('new_restaurant')
                new_restaurant = Restaurant(name=messagecontent[0])
                session.add(new_restaurant)
                session.commit()
                
                self.send_response(301)
                self.send_header('Content-type', 'text/html')
                self.send_header('Location', '/restaurants')
                self.end_headers()
                

            if self.path.endswith('/edit'):
                ctype, pdict = cgi.parse_header(
                    self.headers.getheader('content-type'))
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    messagecontent = fields.get('rest_name')
                    rest_id = self.path.split('/')[-2]
                    restaurant = session.query(Restaurant).filter_by(id=rest_id).one()
                    if restaurant:
                        restaurant.name = messagecontent[0]
                        session.add(restaurant)
                        session.commit()
                        self.send_response(301)
                        self.send_header('Content-type', 'text/html')
                        self.send_header('Location', '/restaurants,')
                        self.end_headers()
        except:
            pass


def main():
    try:
        port = 8080
        server = HTTPServer(('', port), WebServerHandler)
        print "Web Server running on port %s" % port
        server.serve_forever()
    except KeyboardInterrupt:
        print " ^C entered, stopping web server...."
        server.socket.close()

if __name__ == '__main__':
    main()