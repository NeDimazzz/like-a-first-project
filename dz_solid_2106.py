from abc import ABC, abstractmethod


class Weapon(ABC):
    @abstractmethod
    def attack(self):
        pass


class Sword(Weapon):
    def attack(self):
        print("наносит удар мечом")


class Bow(Weapon):
    def attack(self):
        print ("стреляет из лука")



class Fighter:
    def __init__(self, weapon: Weapon):
        self.weapon = weapon

    def change_weapon(self, weapon: Weapon):
        self.weapon = weapon


    def fight (self):
        print(self.weapon.attack())



class Monster:
    pass

sword1 = Sword()
bow1 = Bow()

fighter1 = Fighter(sword1)
monster1 = Monster()

fighter1.fight()

fighter1.change_weapon(bow1)
fighter1.fight()

