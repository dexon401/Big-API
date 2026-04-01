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

MAX_SPN = 10
MIN_SPN = 0.002
MAX_LAT = 58
MIN_LAT = 53
MAX_LON = 40
MIN_LON = 35


class GameView(arcade.Window):
    def setup(self):
        self.lat, self.lon = 55.75105603488043, 37.61748581976496
        self.spn = [0.3, 0.3]

        self.update_image()

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

    def update_image(self):
        params = {
            "apikey": STATIC_MAPS_API_KEY,
            "ll": f"{self.lon},{self.lat}",
            "spn": ",".join(map(str, self.spn)),
        }
        response = requests.get(STATIC_MAPS_URL, params=params)

        if not response:
            print(params)
            print("Http статус:", response.status_code, "(", response.reason, ")")
            sys.exit(1)

        with open(MAP_FILE, "wb") as file:
            file.write(response.content)

        self.background = arcade.load_texture(MAP_FILE)

        self.on_draw()

    def on_key_press(self, symbol, modifiers):
        changed = False
        if symbol == arcade.key.PAGEUP:
            new_spn = [min(MAX_SPN, x * 2) for x in self.spn]
            if new_spn != self.spn:
                self.spn = new_spn
                changed = True
        elif symbol == arcade.key.PAGEDOWN:
            new_spn = [max(MIN_SPN, x * 0.5) for x in self.spn]
            if new_spn != self.spn:
                self.spn = new_spn
                changed = True

        if symbol == arcade.key.UP:
            new_lat = min(self.lat + self.spn[0] * 0.45, MAX_LAT)
            if new_lat != self.lat:
                self.lat = new_lat
                changed = True
        if symbol == arcade.key.DOWN:
            new_lat = max(self.lat - self.spn[0] * 0.45, MIN_LAT)
            if new_lat != self.lat:
                self.lat = new_lat
                changed = True
        if symbol == arcade.key.RIGHT:
            new_lon = min(self.lon + self.spn[1] * 0.45, MAX_LON)
            if new_lon != self.lon:
                self.lon = new_lon
                changed = True
        if symbol == arcade.key.LEFT:
            new_lon = max(self.lon - self.spn[1] * 0.45, MIN_LON)
            if new_lon != self.lon:
                self.lon = new_lon
                changed = True

        if changed:
            print("Changing...")
            self.update_image()

        return super().on_key_press(symbol, modifiers)


def main():
    gameview = GameView(WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_TITLE)
    gameview.setup()
    arcade.run()
    os.remove(MAP_FILE)


if __name__ == "__main__":
    main()
