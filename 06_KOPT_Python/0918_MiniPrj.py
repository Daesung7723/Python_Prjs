import random as rd

class character:
    def __init__(self, name, hp, power):
        self.name = name
        self.hp = hp
        self.power = power

    def status(self):
        print(f"Name: {self.name}, HP: {self.hp}, Power: {self.power}")

    def attack(self):
        damage = rd.randint(1, self.power)
        print(f"{self.name} attacks and deals {damage} damage!")
        return damage

    def injured(self, damage):
        self.hp -= damage
        if self.hp <= 0:
            print(f"{self.name} has been defeated!")
        else:
            print(f"{self.name} has {self.hp} HP remaining.")
            print("-----")

class Player(character):
    def heal(self):
        heal_amount = rd.randint(10, 30)
        self.hp += heal_amount
        print(f"{self.name} heals for {heal_amount} HP! Current HP: {self.hp}")

class Monster(character):
    def roar(self):
        print(f"{self.name} lets out a terrifying roar!")

# Create instances
player = Player("Hero", 100, 20)
monster = Monster("Goblin", 80, 15)
# Display status
player.status()
monster.status()

# Simulate an attack
damage = player.attack()
monster.injured(damage)
damage = monster.attack()
player.injured(damage)

while player.hp > 0 and monster.hp > 0:
    print("                                         ")
    action = input("Choose action: 1. Attack 2. Heal\n")
    if action == '1':
        damage = player.attack()
        monster.injured(damage)
        if monster.hp <= 0:
            break
        damage = monster.attack()
        player.injured(damage)
    elif action == '2':
        player.heal()
        damage = monster.attack()
        player.injured(damage)
    else:
        print("Invalid action. Please choose again.")