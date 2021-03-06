from aiohttp import web
import  aiohttp
from database import activeUsers,Users

websockets = set()
userSockets = {}



class Web_Sockets:
    def __init__(self):
        pass
    
    async def websocket(self,request):
        phoneNumber = request.match_info.get('phoneNumber', "Anonymous")
        print(phoneNumber)
        if Users.find_one({"phoneNumber":phoneNumber}) is not None:
            ws = web.WebSocketResponse()
            await ws.prepare(request)
            if activeUsers.find_one({"phoneNumber":phoneNumber}) is not None:
                activeUsers.insert({"phoneNumber":phoneNumber})
        else:
            ws = None
            print("Please Register your PhoneNumber")

        websockets.add(ws)
        userSockets[phoneNumber] = ws

        try:
            async for msg in ws:
                if msg.type == aiohttp.WSMsgType.TEXT:
                    print(msg.data)
                elif msg.type == aiohttp.WSMsgType.ERROR:
                    print('ws connection closed with exception %s' %
                        ws.exception())
        finally:
            websockets.remove(ws)
            activeUsers.delete_one({"phoneNumber":phoneNumber})
        return ws