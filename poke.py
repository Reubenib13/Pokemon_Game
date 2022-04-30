import random
from time import sleep


class Pokemon:
    def __init__(self, nickname, name, type, health, level, exp):
        self.nickname = nickname
        self.name = name
        self.type = type
        self.health = health
        self.level = level
        self.exp = exp
  

TYPES = {"EARTH": "WATER", "WATER": "FIRE", "FIRE": "GRASS", "GRASS": "EARTH"}
AREA_TO_TYPE = {"MOUNTAIN": "EARTH", "OCEAN": "WATER",
                "DESERT": "FIRE", "FOREST": "GRASS"}
TYPE_TO_ATTACK = {"FIRE": "Fire-Breath", "EARTH": "Rock-Smash",
                  "WATER": "Water-Squirt", "GRASS": "Leaf-Slice"}
POKEMON = {"MOUNTAIN": ["Geodude", "Sandshrew", "Sandslash", "Diglet"],
           "OCEAN": ["Squirtle", "Wartortle", "Blastoise", "Sobble"],
           "DESERT": ["Vulpix", "Charmander", "Scorbunny", "Cinderace"],
           "FOREST": ["Leafeon", "Bulbasaur", "Ivysaur", "Venusaur"]}


def validate_string_input(string, accepted, fail_message):
    valid = False
    while not valid:
        input_ = input(string).lower()
        if input_ in accepted or accepted == []:
            valid = True
        else:
            print(fail_message)
    return input_


def validate_int_input(string, accepted, fail_message):
    valid = False
    while not valid:
        try:
            input_ = int(input(string).lower())
        except ValueError:
            print(fail_message)
            continue
        if input_ in accepted or accepted == []:
            valid = True
        else:
            print(fail_message)
    return input_


def heal(pokemon, pokemon_choice):
    if pokemon[pokemon_choice].health == 50:
        print("Pokemon already fully healed")
    elif pokemon[pokemon_choice].health == 0:
        print("Pokemon has fainted go to the Poke-Hospital to revive")
    else:
        pokemon[pokemon_choice].health += random.randint(10, 20)
        if pokemon[pokemon_choice].health > 50:
            pokemon[pokemon_choice].health = 50

    return pokemon


def find_pokemon(name, type, health, level, exp, pokemon):
    print(f"\nCongratulations you found a {name}")
    nickname = input("What would you like to nickname it: ")
    nicknames = []
    for i in pokemon:
        nicknames.append(i.nickname)
    while nickname in nicknames:
        print("Nickname taken")
        nickname = input("What would you like to nickname your {name}: ")

    pokemon.append(Pokemon(
        nickname=nickname,
        name=name,
        type=type,
        health=health,
        level=level,
        exp=exp
    ))

    return pokemon


def first_pokemon(area, pokemon):
    if area == "MOUNTAIN":
        find_pokemon("Geodude", "EARTH", 50, 1, 0, pokemon)
    elif area == "OCEAN":
        find_pokemon("Squirtle", "WATER", 50, 1, 0, pokemon)
    elif area == "DESERT":
        find_pokemon("Vulpix", "FIRE", 50, 1, 0, pokemon)
    elif area == "FOREST":
        find_pokemon("Leafeon", "GRASS", 50, 1, 0, pokemon)

    return pokemon


def poke_hospital(pokemon):
    while True:
        print("\nYou are at the Poke-Hospital")
        print("Revive a pokemon - (R)")
        print("Quit Poke-Hospital - (Q)")
        action = validate_string_input(
            "Enter action: ", ['r', 'q'], "Enter (R / Q) only!")
        if action == 'r':
            print("\nPokemon:")
            for i, v in enumerate(pokemon):
                print(f"{i + 1}: {v.nickname}")
            accepted = []
            for i in range(len(pokemon)):
                accepted.append(i+1)
            pokemon_choice = validate_int_input(
                "\nEnter the number of the pokemon you wish to revive: ", accepted, f"Enter only the number of one of your pokemon") - 1
            if pokemon(pokemon_choice).health <= 0:
                pokemon(pokemon_choice).health == 10
                print(
                    f"Pokemon {pokemon(pokemon_choice).nickname} is now on 10 health")
            else:
                print(
                    f"{pokemon(pokemon_choice).nickname} still has health so cannot be revived")
        elif action == 'q':
            break
    return pokemon


def chest(inventory, keys_found, chest_increment):
    contents = []
    for _ in range(random.randint(0, 4 + chest_increment)):
        contents.append("Treat")
        inventory["treats"] += 1

    for _ in range(random.randint(0, 4 + chest_increment)):
        contents.append("Poke-Ball")
        inventory["pokeballs"] += 1

    if keys_found["DESERT"] == False and random.randint(0, 20) == 0:
        contents.append("Desert key")
        keys_found["DESERT"] = True

    if keys_found["MOUNTAIN"] == False and random.randint(0, 20) == 0:
        contents.append("Mountain key")
        keys_found["MOUNTAIN"] = True

    if keys_found["FOREST"] == False and random.randint(0, 20) == 0:
        contents.append("Forest key")
        keys_found["FOREST"] = True

    if keys_found["OCEAN"] == False and random.randint(0, 20) == 0:
        contents.append("Ocean key")
        keys_found["OCEAN"] = True

    print("The chest contained")
    for i in contents:
        print(f"A {i}")

    return inventory, keys_found


def check_evolve(pokemon_choice, pokemon):
    if pokemon[pokemon_choice].exp < 50:
        return pokemon
    pokemon[pokemon_choice].health = 50
    pokemon[pokemon_choice].level += 1
    pokemon[pokemon_choice].exp = 0
    print(
        f"\n{pokemon[pokemon_choice].nickname} has evolved to level {pokemon[pokemon_choice].level}")
    print("Xp has been reset and health restored to full")


def fight(pokemon_choice, encounter, pokemon, inventory, catch):
    print(f"\n{pokemon[pokemon_choice].nickname} vs {encounter.name}")
    while True:
        sleep(1.5)
        print(f"\n{encounter.name} used {TYPE_TO_ATTACK[encounter.type]}")
        increment = 0
        if pokemon[pokemon_choice].type == TYPES[encounter.type]:
            increment = 3
            print("Attack was very effective")
        damage = random.randint(8, (9 + increment) + 2 * encounter.level)
        print(f"Attack dealt {damage} damage")
        pokemon[pokemon_choice].health -= damage
        if pokemon[pokemon_choice].health < 1:
            pokemon[pokemon_choice].health = 0
            print(f"{pokemon[pokemon_choice].nickname} has fainted")
            print("\nYou Lost!")
            won = False
            break
        print(
            f"{pokemon[pokemon_choice].nickname} is on {pokemon[pokemon_choice].health} health")

        sleep(1.5)
        print(
            f"\n{pokemon[pokemon_choice].nickname} used {TYPE_TO_ATTACK[pokemon[pokemon_choice].type]}")
        if encounter.type == TYPES[pokemon[pokemon_choice].type]:
            increment = 3
            print("Attack was very effective")
        damage = random.randint(8, (10 + increment) + 2 * encounter.level)
        print(f"Attack dealt {damage} damage")
        encounter.health -= damage
        if encounter.health < 1:
            print(f"{encounter.name} has fainted")
            print("\nYou Won!")
            print(f"{pokemon[pokemon_choice].nickname} gained 10xp")
            pokemon[pokemon_choice].exp += 10
            pokemon = check_evolve(pokemon_choice, pokemon)
            won = True
            break
        print(f"{encounter.name} is on {encounter.health} health")

    if won and catch and inventory["pokeballs"] > 0:
        pokeballs_remaing = inventory["pokeballs"]
        print(f"\nYou have {pokeballs_remaing} pokeballs remaining")
        action = validate_string_input(
            f"Would you like to throw a pokeball to catch {encounter.name} (Y / N): ", ['y', 'n'], "Enter (Y / N) only!")
        if action == 'y':
            if len(pokemon) > 4:
                print("Cannot catch as you have a full team")
                print(
                    "Remove a pokemon from the view pokemon menu to try and catch next time")
            elif random.randint(0, 1) == 0:
                print("Success")
                pokemon = find_pokemon(
                    encounter.name, encounter.type, 50, encounter.level, 0, pokemon)
            else:
                print(f"{encounter.name} escaped\nTry again next time")

    return pokemon, inventory


def view_pokemon(pokemon, inventory):
    while True:
        print("\nPokemon:")
        for i, v in enumerate(pokemon):
            print(f"{i + 1}: {v.nickname}")
        print("\nYou can:")
        print("View details about a pokemon - (V)")
        print("Quit view pokemon - (Q)")
        action_choice = validate_string_input(
            "\nEnter action: ", ['v', 'q'], "Enter (V / Q) only!")
        if action_choice == 'v':
            accepted = []
            for i in range(len(pokemon)):
                accepted.append(i+1)
            pokemon_choice = validate_int_input(
                "Enter the number of the pokemon you wish to view: ", accepted, f"Enter only the number of one of your pokemon") - 1
            while True:
                print(
                    f"\n{pokemon[pokemon_choice].nickname} the {pokemon[pokemon_choice].name}")
                print(f"Type - {pokemon[pokemon_choice].type}")
                print(f"Health - {pokemon[pokemon_choice].health}")
                print(f"Level - {pokemon[pokemon_choice].level}")
                print(f"xp - {pokemon[pokemon_choice].exp}")
                print("\nYou can:")
                treats_left = inventory["treats"]
                print(
                    f"Feed a treat (You have {treats_left} treats left) - (F)")
                print(
                    f"Release '{pokemon[pokemon_choice].nickname}' into the wild - (R)")
                print("Go back- (B)")
                action = validate_string_input(
                    "Enter action: ", ['f', 'r', 'b'], "Enter (F/ R / B) only!")
                if action == 'f':
                    if treats_left == 0:
                        print("No treats avalible")
                    elif pokemon[pokemon_choice].health < 1:
                        print("Cannot feed a fainted pokemon go to the Poke-Hospital")
                    else:
                        inventory["treats"] -= 1
                        pokemon = heal(pokemon, pokemon_choice)
                        print(
                            f"{pokemon[pokemon_choice].nickname} healed to {pokemon[pokemon_choice].health}")

                elif action == 'r':
                    if len(pokemon) == 1:
                        print("You cannot release your only pokemon")
                    else:
                        pokemon.pop(pokemon_choice)
                        print(
                            f"Your pokemon has been released into the wild")

                elif action == 'b':
                    break

        elif action_choice == 'q':
            break
    return pokemon, inventory


def explore(area, pokemon, inventory, keys_found):
    if area == "TOWN":
        while True:
            print("There is the Poke-Hospital")
            print("\nYou can")
            print("Enter Poke-Hospital - (E)")
            print("Quit exploring - (Q)")
            action = validate_string_input(
                "Enter action: ", ['e', 'q'], "Enter (E / Q) only!")
            if action == 'e':
                pokemon = poke_hospital(pokemon)
            elif action == 'q':
                break

    else:
        level_increment = 0
        chest_increment = 0
        if area[:4] == "DEEP":
            level_increment = 2
            chest_increment = 3

        found = random.choice(["chest", "encounter"])
        if found == "chest":
            inventory, keys_found = chest(inventory, keys_found, chest_increment)

        elif found == "encounter":
            name = random.choice(POKEMON[area])
            encounter = Pokemon(name, name, AREA_TO_TYPE[area], random.randint(
                15, 30), random.choice([1, 1, 1, 1, 1, 2, 2, 3]) + level_increment, 0)
            print(f"You encountered a level {encounter.level} {encounter.name}")
            print("\nPokemon:")
            for i, v in enumerate(pokemon):
                print(f"{i + 1}: {v.nickname}")
            accepted = []
            for i in range(len(pokemon)):
                accepted.append(i+1)
            pokemon_choice = validate_int_input(
                "\nEnter the number of the pokemon you wish to fight: ", accepted, f"Enter only the number of one of your pokemon") - 1

            if pokemon[pokemon_choice].health < 1:
                print("That pokemon has fainted go to the Poke-Hospital")
            else:
                pokemon, inventory = fight(
                    pokemon_choice, encounter, pokemon, inventory, True)

    return pokemon, inventory, keys_found


def travel(area, keys_found, boss_beat):
    pass


pokemon = []
inventory = {"pokeballs": 0, "treats": 0}
keys_found = {"FOREST": False, "MOUNTAIN": False,
              "OCEAN": False, "DESERT": False}
boss_beat = {"FOREST": False, "MOUNTAIN": False,
             "OCEAN": False, "DESERT": False}

print("----------------- POKEMON -----------------")
print("--------- A rip-off by ReubenIB13 ---------")
print("\nYou awake in a town, dazzeled, a bright sun beating down above your head.")
print("Getting your bearings you see around you, a forest, a mountain, an ocean and a desert.")
print("Choose a dirction to go")
print("North - A forest (N)")
print("East - A mountain (E)")
print("South - A ocean (S)")
print("West - An desert (W)")
direction_choice = validate_string_input(
    "\nEnter direction: ", ['n', 'e', 's', 'w'], "Enter (N / E / S / W) only!")
area = {'n': "FOREST", 'e': "MOUNTAIN",
        's': "OCEAN", 'w': "DESERT"}[direction_choice]
pokemon = first_pokemon(area, pokemon)

while True:
    print(f"\nYou are at the {area}")
    print("You can: ")
    print("View pokemon - (V)")
    print("Explore the area - (E)")
    print("Travel - (T)")
    action_choice = validate_string_input(
        "\nEnter action: ", ['v', 'e', 't'], "Enter (V / E / T) only!")
    if action_choice == 'v':
        pokemon, inventory = view_pokemon(pokemon, inventory)
    elif action_choice == 'e':
        pokemon, inventory, keys_found = explore(
            area, pokemon, inventory, keys_found)
    elif action_choice == 't':
        area = travel(area, keys_found, boss_beat)
