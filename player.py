from accessible_output2.outputs.auto import Auto
output = Auto()
import os
import json
from shop import load
from encryption import new_key, encrypt_message, decrypt_message


class player:
    equipped = None
    key = "SWJiETZZVKXbhNQwv9LSJR26jONtOEl40NhnTGcL6t8="
    x = 0
    y = 0
    gold = 50
    level = 1
    health = 100
    points = 0
    items = {}
    world = "default"
    filename = "game_files/player_data.txt"

    @staticmethod
    def turn(facing):
        player.facing = facing
        output.speak(f"player is facing {facing}")

    @staticmethod
    def add_item(item):
        if player.items.get(item.id) is None:
            player.items[item.id] = [item, 1]
        else:
            player.items[item.id][1] += 1

    @staticmethod
    def status():
        output.speak("x " + str(player.x))
        output.speak("y " + str(player.y))
        output.speak("gold " + str(player.gold))
        output.speak("level " + str(player.level))
        output.speak("health " + str(player.health))
        output.speak("points " + str(player.points))
        output.speak("world " + player.world)

    @staticmethod
    def save(client):

        if not os.path.exists("game_files/key.txt"):
            new_key("game_files/key.txt")
        #file = open(player.filename, "wb")
        ids = [(k, player.items[k][1]) for k in player.items.keys()]
        print(ids)
        json_data = json.dumps({
            "x": player.x,
             "y": player.y,
             "points":player.points,
             "level": player.level,
             "gold": player.gold,
             "world": player.world,
             "health": player.health,
             "items": ids}).encode("utf-8")

        encrypted_json = encrypt_message(json_data, "game_files/key.txt")
        client.Save(encrypted_json)

    @staticmethod
    def load():
        if not os.path.exists(player.filename):
            return

        decrypt(player.filename, "game_files/key.txt")
        file = open(player.filename, "rb")
        data = json.loads(file.read().decode("utf-8"))
        file.close()
        player.x = data["x"]
        player.y = data["y"]
        ids = data["items"]
        print(ids)
        load(ids, player)
        player.gold = data["gold"]
        player.level = data["level"]
        player.health = data["health"]
        player.points = data["points"]
        player.world = data["world"]
        encrypt(player.filename, "game_files/key.txt") # make sure it stays encrypted


