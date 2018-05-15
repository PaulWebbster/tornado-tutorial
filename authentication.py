import os
import tornado.web
import tornado.escape
import tornado.ioloop
import tornado.httpserver

from database import check_login


class MyApplication(tornado.web.Application):

    def __init__(self):
        handlers = [
            (r"/", MainHandler),
            (r"/auth/login", LoginHandler),
            (r"/auth/logout", LogoutHandler)
        ]
        settings = dict(
            cookie_secret="huisa7623eb,fdsbu73rjanfjbasdufy8sd",
            template_path=os.path.join(os.path.dirname(__file__), "templates"),
            login_url="/auth/login"
        )
        super(MyApplication, self).__init__(handlers, **settings)


class BaseHandler(tornado.web.RequestHandler):
    def get_current_user(self):
        return self.get_secure_cookie("user")


class MainHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        name = tornado.escape.xhtml_escape(self.current_user)
        self.write("Hello, " + name)


class LoginHandler(BaseHandler):
    def get(self):
        self.render("login.html", error=None)

    def post(self):
        username = self.get_argument("name")
        password = self.get_argument("password")
        if check_login(username, password):
            self.set_secure_cookie("user", username)
            self.redirect("/")
        else:
            self.render('login.html', error="Error: incorrect password or username")


class LogoutHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        name = tornado.escape.xhtml_escape(self.current_user)
        self.clear_cookie("user")
        self.write("{} you log out".format(name))

def main():
    application = tornado.httpserver.HTTPServer(MyApplication())
    application.listen(8888)
    tornado.ioloop.IOLoop.current().start()


if __name__ == '__main__':
    main()
