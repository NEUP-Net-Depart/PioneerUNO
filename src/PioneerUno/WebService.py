import aiohttp
from aiohttp import web

app = web.Application()
routes = web.RouteTableDef()


@routes.get("/ws")
async def websocket_handler(request):
    ws = web.WebSocketResponse()
    await ws.prepare(request)

    async for msg in ws:
        if msg.type == aiohttp.WSMsgType.TEXT:
            pass
        elif msg.type == aiohttp.WSMsgType.ERROR:
            print(ws.exception())


@routes.get("/rooms")
async def get_rooms():
    pass


app.add_routes(routes)
