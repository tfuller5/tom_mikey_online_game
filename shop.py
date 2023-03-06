from accessible_output2.outputs.auto import Auto
output = Auto()
import simple_menu
import lucia
if not lucia.running: lucia.initialize()
class item:
    def __init__(self, ID, name, price, description):
        self.id = ID
        self.name = name
        self.price = price
        self.description = description
    def buy(self, player):
        if player.gold > self.price:
            output.speak(f"{self.name} purchased")
            player.add_item(self)
        else:
            output.speak("You don't have enough gold to buy this.")

stock=[
    item(1, "M164 Master Sniper", 250, "This weapon deals a lot of damage and only contains 3 bullets. ."),
    item(2, "Burst machinegun", 200, "This weapon contains a lot of ammo and fires fast.."),
    item(3, "M16Shotgun", 150, "A powerful weapon that can kill enemies."),
]


def inventory(items):
    if items == {}:
        output.speak("Your inventory is empty")
        return

    s = simple_menu.simple_menu(clicksound="menuclick.ogg", edgesound="menuedge.ogg", entersound="menuenter.ogg",
                                wrapsound="menuwrap.ogg", leftright=False, updown=True, wrapping=True, homeend=True)

    for each_item in items.values():
        s.add_item(str(each_item[1]) + " "+each_item[0].name)
    s.run(f"Inventory, press down arrow to navigate through your items.", True)


def shop(player):
    s = simple_menu.simple_menu(clicksound = "menuclick.ogg", edgesound = "menuedge.ogg", entersound = "menuenter.ogg", wrapsound="menuwrap.ogg", leftright = False, updown = True, wrapping = True, homeend = True)

    for pos, each_item in enumerate(stock):
        s.add_item(each_item.name+" costs "+ str(each_item.price) + " gold. "+each_item.description, internal_name = str(pos))
    choice = s.run(f"The shop, press down arrow to navigate through the available items.",True)
    stock[int(s.get_item_name(choice))].buy(player)

def load(ids, player):
    item_by_id = {item.id: item for item in stock}
    for id, amount in ids:
        for _ in range(amount):
            player.add_item(item_by_id[id])

if __name__ == "__main__": shop()