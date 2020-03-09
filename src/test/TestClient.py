import aiohttp

host = "http://localhost:8080/"

session = aiohttp.ClientSession()


def print_help():
    print(
        """
        """
    )


command = {

}


async def main():
    player_name = input("your player name:")
    connection = session.ws_connect(host + f"api/ws?nickname={player_name}")
    while True:
        pass
