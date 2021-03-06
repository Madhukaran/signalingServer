import aiohttp
import aiohttp_jinja2
import jinja2
from aiohttp import web
from database import Users


class AuthUser:
    def __init__(self):
        pass

    async def Signup(self,request):
        context = {}
        response = aiohttp_jinja2.render_template("signup.html", request,context=context)
        return response
    
    async def Signup_(self,request):
        try:
            data = await request.post()
            phoneNumber = data.get("phoneNumber")
            if phoneNumber is not None:
                if Users.find_one({"phoneNumber":phoneNumber}) is None:
                    Users.insert({"phoneNumber":phoneNumber})
                    return web.Response(text="User created Sucessfully!")
                else:
                    return web.Response(text="User Already exist!!")
        except :
            pass

