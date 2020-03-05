from aiohttp import web

from src.PioneerUno.WebService import app

if __name__ == '__main__':
    web.run_app(app)
