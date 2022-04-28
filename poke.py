import random


class Pokemon:
    def __init__(self, nickname, name, primary_type, health, level):
        self.nickname = nickname
        self.name = name
        self.primary_type = primary_type
        self.health = health
        self.level = level


TYPES = ["EARTH", "WATER", "FIRE", "GRASS", "EARTH"]


def find_pokemon(name, primary_type, health, level):
    print("\n Congratulations you found a {name}")
    nickname = input("What would youlike to nickname it: ")
    nicknames = []
    for i in pokemon:
        nicknames.append(i.nickname)
    while nickname in nicknames:
        print("Nickname taken")
        nickname = input("What would you like to nickname your {name}: ")

    pokemon.append(Pokemon(
        nickname=nickname,
        name=name,
        primary_type=primary_type,
        health=health,
        level=level
    ))


def first_pokemon(area):
    if area == "MOUNTAIN":
        find_pokemon("Geodude", "EARTH", 50, 1)
    elif area == "SEA":
        find_pokemon("Squirtle", "WATER", 50, 1)
    elif area == "DESERT":
        find_pokemon("Vulpix", "FIRE", 50, 1)
    elif area == "FOREST":
        find_pokemon("Leafeon", "GRASS", 50, 1)


def validate_string_input(string, accepted, fail_message):
    valid = False
    while not valid:
        input_ = input(string).lower()
        if input_ in accepted:
            valid = True
        else:
            print(fail_message)
    return input_


def view_pokemon(pokemon):
    print("Pokemon:")
    for i, v in enumerate(pokemon):
        print(f"{i + 1}: {v.name}")
    print("You can:") # You are here


pokemon = []

print("----------------- POKEMON -----------------")
print("---------- A rip-off by ReubenIB13 ---------")
print("\nYou awake a bright sun beating down above your head.")
print("Getting your bearings you see around you, a forest, a rocky outcrop, an ocean and a desert.")
print("Choose a dirction to go")
print("North - A forest (N)")
print("East - A mountain (E)")
print("South - A ocean (S)")
print("West - An desert (W)")
direction_choice = validate_string_input(
    "\nEnter direction: ", ['n', 'e', 's', 'w'], "Enter (N / E / S / W) only")
area = {'n': "FOREST", 'e': "MOUNTAIN",
        's': "OCEAN", 'w': "DESERT"}[direction_choice]
first_pokemon(area)

while True:
    print(f"You are at the {area}")
    print("You can: ")
    print("View pokemon - (V)")
    print("Explore the area - (E)")
    print("Travel - (T)")
    action_choice = validate_string_input(
        "\nEnter action: ", ['v', 'e', 't'], "Enter (V / E / T) only")
    if action_choice == 'v':
        view_pokemon(pokemon)
    elif action_choice == 'e':
        pass
    elif action_choice == 't':
        pass
