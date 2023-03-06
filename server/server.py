from __future__ import print_function

import sys
from time import sleep, localtime
from weakref import WeakKeyDictionary

from PodSixNet.Server import Server
from PodSixNet.Channel import Channel
from accessible_output2.outputs.auto import Auto
output = Auto()

class PlayerChannel(Channel):
    nickname: str
    """
    This is the server representation of a single connected client.
    """
    def __init__(self, *args, **kwargs):
        self.nickname = None
        Channel.__init__(self, *args, **kwargs)

    def Close(self):
        self._server.DelPlayer(self)

    ##################################
    ##################################
    def SendToEveryoneElse(self, data):
        for player in self._server.players:
            if player != self:
                player.Send(data)

    def Network_i_just_moved(self, data):
       self.SendToEveryoneElse({"action": "someone_just_moved", "x": data["x"], "y": data["y"]})

    def Network_give_nickname(self, data):
        self.nickname = data["name"]
        self.SendToEveryoneElse({"action": "new_guy", "name": self.nickname})

    def Network_ListEveryone(self, data):
        names = [p.nickname for p in self._server.players]
        self.Send({"action": "ListEveryone", "names": names})

    def Network_chat(self, data):
        self.SendToEveryoneElse({"action": "chat", "name": self.nickname, "message": data["message"]})


class ChatServer(Server):
    channelClass = PlayerChannel
    
    def __init__(self, *args, **kwargs):
        Server.__init__(self, *args, **kwargs)
        self.players = []
        print('SERVER LAUNCHED')
    
    def Connected(self, channel, addr):
        print("get connected for free", addr)
        self.players.append(channel)
        self.SendToAll({"action": "players", "players": [p.nickname for p in self.players]})
        # player nickname will be shown immediately after



    def DelPlayer(self, player):
        self.players.remove(player)
    
    def SendToAll(self, data):
        [p.Send(data) for p in self.players]
    
    def Launch(self):
        while True:
            self.Pump()
            sleep(0.0001)

host = "0.0.0.0"
port = 80
s = ChatServer(localaddr=(host, int(port)))
s.Launch()

