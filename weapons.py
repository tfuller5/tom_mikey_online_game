from accessible_output2.outputs.auto import Auto
output = Auto()

class weapon:
    def __init__(self, name, damage, range, ammo):
        self.name = name
        self.damage = damage
        self.range = range
        self.ammo = ammo
        self.firing = False
        self.heldat = 0

    def triggerhold(self, frames):
        if self.firing == True:
            framediff = frames - self.heldat
            if framediff%10 == 0:
                output.speak("zit")

        else:
            self.firing = True
            self.heldat = frames

    def triggerrelease(self):
        self.firing = False

class weapons:
    default = [
        weapon("Bonk 3000", 1000000000, 1000000000, 1),
        weapon("bloop15", 1000000000, 1000000000, 10),
        weapon("crip900", 1000000000, 1000000000, 15),
    ]

    @staticmethod
    def select_weapon(player):
        chosen = weapons.default[0]
        output.speak(f"Equipped {chosen.name}")
        player.equipped = chosen