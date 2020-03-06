import unittest

import aiohttp

host = "http://localhost:8080/"


class TestWebService(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self) -> None:
        self.client_session = aiohttp.ClientSession()

    async def asyncTearDown(self) -> None:
        await self.client_session.close()

    async def test_ping(self):
        async with self.client_session.get(host + "api/ping") as resp:
            text = await resp.text()
            print(text)
            self.assertEqual(text, "pong")

    async def test_get_room(self):
        async with self.client_session.get(host + "api/rooms") as resp:
            json = await resp.json()
            print(json)
            self.assertEqual(json['status'], 0)

    async def test_websocket(self):
        async with self.client_session.ws_connect(host + "api/ws?nickname=233") as ws:
            await ws.send_json({
                'command': 'ping'
            })
            pong = await ws.receive_json()
            print(pong)
            self.assertEqual(pong['status'], 0)

    async def test_create_room(self):
        async with self.client_session.ws_connect(host + "api/ws?nickname=233") as ws:
            await ws.send_json({
                'command': 'create_room'
            })

            response = await ws.receive_json()
            async with self.client_session.get(host + "api/rooms") as resp:
                json = await resp.json()
                print(json)
                self.assertTrue(response['data'] in json['data'])


if __name__ == '__main__':
    unittest.main()
