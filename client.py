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
        output.speak("Enter your nickname: ")
        connection.Send({"action": "give_nickname", "name": input("> ")})
        t = start_new_thread(lambda *args: mainloop(self), ())

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

    def Loop(self):
        connection.Pump()
        self.Pump()

    ######################  #################
    ### Network event/message callbacks ###
    #######################################
    def Network_new_guy(self, data):
        output.speak(data["name"] + " has connected to the server")


host = "81.106.228.102"
port = 80
c = Client(host, int(port))
while True:
    c.Loop()
    sleep(0.001)
