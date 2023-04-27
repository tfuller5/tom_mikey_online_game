from __future__ import print_function
from time import sleep

from accessible_output2.outputs.auto import Auto
output = Auto()

from PodSixNet.Connection import connection, ConnectionListener

from _thread import *
from game_bit import mainloop, youmove


class Client(ConnectionListener):
    def __init__(self, host, port):
        self.Connect((host, port))
        name= "%"
        while not name.isalnum():
            output.speak("Enter your nickname: ")
            name = input("> ")
        name = name.replace(" ", "_")
        connection.Send({"action": "give_nickname", "name": name})
        t = start_new_thread(lambda *args: mainloop(self), ())
        self.Loop()

    def Save(self, encrypted_data):
        connection.Send({"action": "save_player_data", "data": encrypted_data})

    def ListEveryone(self):
        connection.Send({"action": "ListEveryone"})

    def Network_ListEveryone(self, data):
        ps = data["names"]
        output.speak("There are " + str(len(ps)) + " players in the server")
        for p in ps:
            output.speak(f"{p}, what a great guy")

    def i_just_moved(self, x, y):
        connection.Send({"action": "i_just_moved", "x": x, "y": y})

    def Network_someone_just_moved(self, data):
        youmove(data["x"], data["y"])

    def Chat(self, message):
        output.speak("You said: "+ message)
        connection.Send({"action": "chat", "message": message})


    def Network_chat(self, data):
        output.speak(data["name"] + " said " + data["message"])

    def Network_confirmation(self, data):
        output.speak(f"CONFIRMATION. <{data['response']}>")
        print(f"CONFIRMATION. <{data['response']}>")

    def Network_new_guy(self, data):
        output.speak(data["name"] + " has connected to the server")

    def Network_someone_else_disconnected(self, data):
        output.speak(str(data["name"]) + " has disconnected from the server")

    def Loop(self):
        connection.Pump()
        self.Pump()


host = "81.106.228.102"
host = "44.200.50.168"
host = "34.205.4.43"
port = 8080
c = Client(host, int(port))
while True:
    c.Loop()
    sleep(0.001)
