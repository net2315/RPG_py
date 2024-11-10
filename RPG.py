import random


class Character:
    def __init__(self, name, hp, attack, defense):
        self.name = name
        self.hp = hp
        self.max_hp = hp
        self.attack = attack
        self.defense = defense
        self.level = 1
        self.xp = 0

    def take_damage(self, damage):
        actual_damage = max(0, damage - self.defense)
        self.hp = max(0, self.hp - actual_damage)  # Limite HP à zéro
        print(f"{self.name} prend {actual_damage} points de dégâts ! HP restant: {self.hp}")

    def is_alive(self):
        return self.hp > 0

    def heal(self, amount):
        self.hp = min(self.max_hp, self.hp + amount)
        print(f"{self.name} récupère {amount} points de vie !")


class Player(Character):
    def __init__(self, name):
        super().__init__(name, hp=100, attack=10, defense=5)
        self.inventory = [HealthPotion()]

    def level_up(self):
        self.level += 1
        self.max_hp += 10
        self.hp = self.max_hp
        self.attack += 2
        self.defense += 1
        print(f"{self.name} monte au niveau {self.level} ! Stats: HP={self.hp}, ATK={self.attack}, DEF={self.defense}")

    def gain_xp(self, amount):
        self.xp += amount
        print(f"{self.name} gagne {amount} points d'XP !")
        if self.xp >= self.level * 10:
            self.level_up()
            self.xp = 0

    def use_item(self, item):
        if item in self.inventory:
            item.apply_effect(self)
            self.inventory.remove(item)
        else:
            print("L'objet n'est pas dans l'inventaire !")


class Monster(Character):
    def __init__(self, name, level):
        hp = 50 + (level * 10)
        attack = 5 + (level * 2)
        defense = 3 + (level * 2)
        super().__init__(name, hp, attack, defense)
        self.level = level


class Item:
    def __init__(self, name):
        self.name = name

    def apply_effect(self, character):
        pass  # A surcharger pour chaque type d'objet


class HealthPotion(Item):
    def __init__(self):
        super().__init__("Potion de Santé")

    def apply_effect(self, character):
        character.heal(20)
        print(f"{character.name} utilise une {self.name} et récupère 20 HP !")


class Game:
    def __init__(self):
        self.player = None
        self.is_running = True
        self.map = {
            (0, 0): "point de départ",
            (1, 0): "une rivière",
            (0, 1): "un grand arbre",
            (1, 1): "un boss puissant"
        }
        self.boss_location = (1, 1)
        self.player_location = (0, 0)

    def start_game(self):
        print("Bienvenue dans le RPG rétro !")
        name = input("Entrez votre nom de joueur : ")
        self.player = Player(name)
        while self.is_running:
            self.main_menu()

    def main_menu(self):
        print("\n=== Menu Principal ===")
        print("1. Nouvelle Partie")
        print("2. Quitter")
        choice = input("Choisissez une option : ")
        if choice == '1':
            self.play_game()
        elif choice == '2':
            self.is_running = False
            print("Merci d'avoir joué !")
        else:
            print("Choix invalide.")

    def play_game(self):
        print(f"\nBienvenue, {self.player.name}. Vous commencez avec un couteau et {self.player.hp} HP.")
        while self.player.is_alive():
            self.describe_location()
            command = input("Entrez une commande (Nord, Sud, Est, Ouest) : ").lower()
            if command in ["nord", "sud", "est", "ouest"]:
                self.move_player(command)
            elif command == "quitter":
                print("Vous quittez le jeu.")
                break
            else:
                print("Commande invalide.")

    def describe_location(self):
        location = self.map.get(self.player_location, "une case vide.")
        print(f"\nVous êtes à {location}.")
        if self.player_location == self.boss_location:
            print("Le boss apparaît !")
            self.start_combat(Monster("Boss", 5))

    def move_player(self, direction):
        x, y = self.player_location
        if direction == "nord":
            self.player_location = (x, y + 1)
        elif direction == "sud":
            self.player_location = (x, y - 1)
        elif direction == "est":
            self.player_location = (x + 1, y)
        elif direction == "ouest":
            self.player_location = (x - 1, y)
        print(f"Vous vous déplacez vers le {direction}.")

        if self.player_location in self.map:
            if random.choice([True, False]):
                self.start_combat(Monster("Monstre", random.randint(1, self.player.level)))
            else:
                self.find_item()
        else:
            print("Vous êtes en dehors de la carte !")

    def find_item(self):
        item = HealthPotion()
        print(f"Vous trouvez un {item.name} et l'ajoutez à votre inventaire.")
        self.player.inventory.append(item)

    def start_combat(self, monster):
        print(f"\nCombat ! Vous affrontez un {monster.name} de niveau {monster.level} avec {monster.hp} HP.")
        while self.player.is_alive() and monster.is_alive():
            action = input("Choisissez une action (Attaquer, Objet, Fuir) : ").lower()
            if action == "attaquer":
                self.attack(monster)
            elif action == "objet":
                self.use_item()
            elif action == "fuir":
                print("Vous fuyez le combat !")
                return
            else:
                print("Action invalide.")
                continue

            if monster.is_alive():
                self.monster_attack(monster)
            else:
                print(f"Vous avez vaincu {monster.name} !")

        if self.player.is_alive():
            self.player.gain_xp(10)
        else:
            print("Vous êtes mort. Fin de la partie.")
            self.is_running = False

    def attack(self, monster):
        damage = max(0, self.player.attack - monster.defense)
        monster.take_damage(damage)
        print(f"Vous attaquez {monster.name} et lui infligez {damage} points de dégâts.")

    def monster_attack(self, monster):
        damage = max(0, monster.attack - self.player.defense)
        self.player.take_damage(damage)
        print(f"{monster.name} vous attaque et inflige {damage} points de dégâts.")

    def use_item(self):
        if not self.player.inventory:
            print("Votre inventaire est vide.")
            return
        print("Inventaire :")
        for i, item in enumerate(self.player.inventory, 1):
            print(f"{i}. {item.name}")
        choice = int(input("Choisissez un objet à utiliser : "))
        if 1 <= choice <= len(self.player.inventory):
            self.player.use_item(self.player.inventory[choice - 1])
        else:
            print("Choix invalide.")


if __name__ == "__main__":
    game = Game()
    game.start_game()

