from accessible_output2.outputs.auto import Auto
output = Auto()

from PodSixNet.Connection import connection, ConnectionListener

from game_bit import mainloop, youmove, youchat

class Client(ConnectionListener):
    def __init__(self):
        self.name = load_nickname()
        self.connected = False
        self.connect_callback = None

        host = "81.106.228.102"
        host = "44.200.50.168"
        host = "34.205.4.43"
        host = "34.237.139.36"
        host = "44.193.199.42"
        #host = "localhost"
        port = 8080

        self.host = host
        self.port = port

    def start_game(self):
        mainloop(self)

    def disconnect(self):
        # this is not working currently
        self.connected = False
        connection.Close()

    def connect(self, callback):
        self.Connect((self.host, self.port))
        print("hello?")

        connection.Send({"action": "give_nickname", "name": self.name})
        self.connect_callback = callback

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

    def Network_I_connected(self, data):
        print("I connected, confirmation")
        self.connected = True
        self.connect_callback()

    def Network_chat(self, data):
        say_this= data["name"] + " said " + data["message"]
        output.speak(say_this)
        youchat(say_this)

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


def load_nickname():
    nickname_file = "game_files/nick_is_the_name.txt"

    try:
        file = open(nickname_file, "r")
        nick = file.read()
        file.close()
        return nick
    except FileNotFoundError:
        open(nickname_file, "w").close()
        return None

c = Client()

c.start_game()

