from player import player
from gamething import simple_menu
import lucia

if not lucia.running: lucia.initialize()
def info():
	s = simple_menu.simple_menu(clicksound ="menuclick.ogg", edgesound ="menuedge.ogg", entersound ="menuenter.ogg", wrapsound="menuwrap.ogg", leftright = False, updown = True, wrapping = True, homeend = True)
	s.add_item(f"You have {player.coins} coins.")
	s.add_item(f"You are level {player.level}.")
	s.add_item(f"You have {player.health} health.")
	s.add_item(f"You have {player.points} points.")
	s.add_item(f"Your current world is {player.world}")
	choice = s.run("Infomation, press down arrow to read",True)
if __name__ == "__main__": info()