from registration import AuthUser
import aiohttp
import aiohttp_jinja2
import jinja2
from aiohttp import web
import os
import aiohttp_session
from aiohttp_session import new_session, SimpleCookieStorage
from SocketInitiate import Web_Sockets


routes = web.RouteTableDef()

def get_app(argv=None):
    app = web.Application()
    app.add_routes(routes)
    aiohttp_jinja2.setup(app, loader=jinja2.FileSystemLoader(os.path.join(os.getcwd(), "templates")))
    aiohttp_session.setup(app, aiohttp_session.SimpleCookieStorage(cookie_name="RTC"))
    return app

app = get_app()
staticdir_ = os.path.join(os.getcwd(), "static")
app.add_routes([web.static('/static/', staticdir_)])

# Urls for the User Authentication
Authentication = AuthUser()
app.add_routes([web.get('/', Authentication.Signup),
                web.post('/', Authentication.Signup_)])

# Urls for the User Authentication
socket = Web_Sockets()
app.add_routes([web.get('/{phoneNumber}/ws/', socket.websocket)])



if __name__ == '__main__':
    web.run_app(app,host="192.168.1.18",port=8000)