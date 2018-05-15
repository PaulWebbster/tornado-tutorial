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
            (r"/login", LoginHandler),
        ]
        settings = dict(
            cookie_secret="huisa7623eb,fdsbu73rjanfjbasdufy8sd",
            template_path=os.path.join(os.path.dirname(__file__), "templates")
        )
        super(MyApplication, self).__init__(handlers, **settings)


class BaseHandler(tornado.web.RequestHandler):
    def get_current_user(self):
        return self.get_secure_cookie("user")


class MainHandler(BaseHandler):
    def get(self):
        if not self.current_user:
            self.redirect("login")
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


def main():
    application = tornado.httpserver.HTTPServer(MyApplication())
    application.listen(8888)
    tornado.ioloop.IOLoop.current().start()


if __name__ == '__main__':
    main()
