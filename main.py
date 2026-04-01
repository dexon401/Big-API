import os
import sys
import requests
import arcade

STATIC_MAPS_API_KEY = "f3a0fe3a-b07e-4840-a1da-06f18b2ddf13"
STATIC_MAPS_URL = "https://static-maps.yandex.ru/v1"

GEOCODER_API_KEY = "8013b162-6b42-4997-9691-77b7074026e0"
GEOCODER_URL = "https://geocode-maps.yandex.ru/v1"

SEARCH_MAPS_API_KEY = "dda3ddba-c9ea-4ead-9010-f43fbc15c6e3"
SEARCH_MAPS_URL = "https://search-maps.yandex.ru/v1"

WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720
WINDOW_TITLE = "MAP"
MAP_FILE = "map.png"


class GameView(arcade.Window):
    def setup(self):
        self.get_image()

    def on_draw(self):
        self.clear()

        arcade.draw_texture_rect(
            self.background,
            arcade.LBWH(
                (self.width - self.background.width) // 2,
                (self.height - self.background.height) // 2,
                self.background.width,
                self.background.height,
            ),
        )

    def get_image(self):
        lat, lon = 55.75105603488043, 37.61748581976496
        spn_lat, spn_lon = 0.3, 0.3
        
        params = {
            "apikey": STATIC_MAPS_API_KEY,
            "ll": f"{lon},{lat}",
            "spn": f"{spn_lon},{spn_lat}"
        }
        response = requests.get(STATIC_MAPS_URL, params=params)

        if not response:
            print("Http статус:", response.status_code, "(", response.reason, ")")
            sys.exit(1)

        with open(MAP_FILE, "wb") as file:
            file.write(response.content)

        self.background = arcade.load_texture(MAP_FILE)


def main():
    gameview = GameView(WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_TITLE)
    gameview.setup()
    arcade.run()
    os.remove(MAP_FILE)


if __name__ == "__main__":
    main()
