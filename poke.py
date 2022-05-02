import random
import pickle
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


def start():
    print("----------------- POKEMON -----------------")
    print("--------- A rip-off by ReubenIB13 ---------")
    print("\nYou awake in a town, dazzled, a bright sun beating down above your head.")
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
    pokemon = []
    pokemon = first_pokemon(area, pokemon)

    inventory = {"pokeballs": 0, "treats": 0}
    keys_found = {"FOREST": False, "MOUNTAIN": False,
                  "OCEAN": False, "DESERT": False}
    boss_beat = {"FOREST": False, "MOUNTAIN": False,
                 "OCEAN": False, "DESERT": False}
    final_boss = False

    return area, pokemon, inventory, keys_found, boss_beat, final_boss


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
            if pokemon[pokemon_choice].health <= 0:
                pokemon[pokemon_choice].health = 10
                print(
                    f"Pokemon {pokemon[pokemon_choice].nickname} is now on 10 health")
            else:
                print(
                    f"{pokemon[pokemon_choice].nickname} still has health so cannot be revived")
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

    if keys_found["DESERT"] == False and random.randint(0, 5) == 0:
        contents.append("Desert key")
        keys_found["DESERT"] = True

    if keys_found["MOUNTAIN"] == False and random.randint(0, 5) == 0:
        contents.append("Mountain key")
        keys_found["MOUNTAIN"] = True

    if keys_found["FOREST"] == False and random.randint(0, 5) == 0:
        contents.append("Forest key")
        keys_found["FOREST"] = True

    if keys_found["OCEAN"] == False and random.randint(0, 5) == 0:
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

    return pokemon


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
        damage = random.randint(8, (10 + increment) +
                                2 * pokemon[pokemon_choice].level)
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
                action = validate_string_input(
                    "Would you like to release a pokemon (Y / N): ", ['y', 'n'], "Enter(Y / N) only!")
                if action == 'y':
                    print("\nPokemon:")
                    for i, v in enumerate(pokemon):
                        print(f"{i + 1}: {v.nickname}")
                    accepted = []
                    for i in range(len(pokemon)):
                        accepted.append(i+1)
                    pokemon_choice = validate_int_input(
                        "Enter the number of the pokemon you wish to release: ", accepted, f"Enter only the number of one of your pokemon") - 1
                    pokemon.pop(pokemon_choice)
            elif random.randint(0, 1) == 0:
                print("Success")
                inventory["pokeballs"] -= 1
                pokemon = find_pokemon(
                    encounter.name, encounter.type, 50, encounter.level, 0, pokemon)
            else:
                print(f"{encounter.name} escaped\nTry again next time")

    return pokemon, inventory


def boss(area, pokemon, boss_beat):
    boss_beat[area] = True
    print(f"You have encountered the {area} Boss!")
    for i in range(4):
        total = 0
        for j in pokemon:
            total += j.health
        if total < 1:
            print("All pokemon have fainted go to Poke-Hosipital")
            boss_beat[area] = False
            break

        else:
            encounter = Pokemon(
                POKEMON[area][i], POKEMON[area][i], AREA_TO_TYPE[area], 50, i + 2, 0)
            print(f"\nThe {area} Boss used they're {encounter.name}")
            print("\nPokemon:")
            for i, v in enumerate(pokemon):
                print(f"{i + 1}: {v.nickname}")
            accepted = []
            for i in range(len(pokemon)):
                accepted.append(i+1)
            pokemon_choice = validate_int_input(
                "Enter the number of the pokemon you wish to fight: ", accepted, "Enter only the number of one of your pokemon") - 1
            while pokemon[pokemon_choice].health < 1:
                print("That pokemon has fainted choose another")
                pokemon_choice = validate_int_input(
                    "Enter the number of the pokemon you wish to fight: ", accepted, "Enter only the number of one of your pokemon") - 1
            pokemon, _ = fight(pokemon_choice, encounter, pokemon, None, False)

    if boss_beat[area] and encounter.health <= 0:
        print(
            f"Congratulations you beat the boss\nYou can now enter the DEEP {area}")
    return pokemon, boss_beat


def end_boss(pokemon):
    won = True
    for i in range(5):
        print("\nYou have encountered the final boss!\n")

        total = 0
        for j in pokemon:
            total += j.health
        if total < 1:
            print("All pokemon have fainted go to Poke-Hosipital")
            won = False
            break

        area = random.choice(["MOUNTAIN", "DESERT", "OCEAN", "FOREST"])
        name = random.choice(POKEMON[area])
        encounter = Pokemon(name, name, AREA_TO_TYPE[area], 50, i + 5, 0)

        print(
            f"The {area} Boss used they're level {encounter.level} {encounter.name}")

        print("\nPokemon:")
        for i, v in enumerate(pokemon):
            print(f"{i + 1}: {v.nickname}")

        accepted = []
        for i in range(len(pokemon)):
            accepted.append(i+1)

        pokemon_choice = validate_int_input(
            "Enter the number of the pokemon you wish to fight: ", accepted, f"Enter only the number of one of your pokemon") - 1
        while pokemon[pokemon_choice].health < 1:
            print("That pokemon has fainted choose another")
            pokemon_choice = validate_int_input(
                "Enter the number of the pokemon you wish to fight: ", accepted, f"Enter only the number of one of your pokemon") - 1
        pokemon, _ = fight(pokemon_choice, encounter, pokemon, None, False)

    return pokemon, won


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


def explore(area, pokemon, inventory, keys_found, final_boss):
    won = False
    if area == "TOWN":
        if not final_boss:
            while True:
                print("There is the Poke-Hospital")
                print("\nYou can:")
                print("Enter Poke-Hospital - (E)")
                print("Quit exploring - (Q)")
                action = validate_string_input(
                    "Enter action: ", ['e', 'q'], "Enter (E / Q) only!")
                if action == 'e':
                    pokemon = poke_hospital(pokemon)
                elif action == 'q':
                    break
        if final_boss:
            while True:
                print("There is the Poke-Hospital")
                print("A mysterious cave appeared")
                print("\nYou can:")
                print("Enter Poke-Hospital - (E)")
                print("Enter mysterious cave - (C)")
                print("Quit exploring - (Q)")
                action = validate_string_input(
                    "Enter action: ", ['e', 'c', 'q'], "Enter (E / C / Q) only!")
                if action == 'e':
                    pokemon = poke_hospital(pokemon)
                elif action == 'c':
                    pokemon, won = end_boss(pokemon)
                elif action == 'q' or won:
                    break

    else:
        level_increment = 0
        chest_increment = 0
        if area[:4] == "DEEP":
            level_increment = 2
            chest_increment = 3

        found = random.choice(["chest", "encounter"])
        if found == "chest":
            inventory, keys_found = chest(
                inventory, keys_found, chest_increment)

        elif found == "encounter":
            name = random.choice(POKEMON[area])
            encounter = Pokemon(name, name, AREA_TO_TYPE[area], random.randint(
                15, 30), random.choice([1, 1, 1, 1, 1, 2, 2, 3]) + level_increment, 0)
            print(
                f"You encountered a level {encounter.level} {encounter.name}")
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

    return pokemon, inventory, keys_found, won


def travel(area, keys_found, boss_beat, pokemon, inventory):

    if area[:4] == "DEEP":
        print("You can travel to: ")
        print(f"{area[5:]} - (T)")
        print("Stay here - (H)")
        direction_choice = validate_string_input(
            "\nEnter direction: ", ['t', 'h'], "Enter (T / H) only!")
        if direction_choice == 't':
            area = area[5:]

    elif area == "TOWN":
        print("You can travel to:")
        print("North - A forest (N)")
        print("East - A mountain (E)")
        print("South - A ocean (S)")
        print("West - An desert (W)")
        print("Stay here - (H)")
        direction_choice = validate_string_input(
            "\nEnter direction: ", ['n', 'e', 's', 'w', 'h'], "Enter (N / E / S / W / H) only!")
        area = {'n': "FOREST", 'e': "MOUNTAIN",
                's': "OCEAN", 'w': "DESERT", 'h': "TOWN"}[direction_choice]

    else:
        print("You can travel to:")
        print("Back to town - (T)")
        print(f"Into the deep {area} - (D)")
        print("Stay here - (H)")
        direction_choice = validate_string_input(
            "\nEnter direction: ", ['t', 'd', 'h'], "Enter (T / D / H) only!")
        if direction_choice == 't':
            area = "TOWN"
        elif direction_choice == 'd':
            if keys_found[area]:
                if not boss_beat[area]:
                    pokemon, boss_beat = boss(area, pokemon, boss_beat)
                if boss_beat[area]:
                    area = "DEEP " + area
            else:
                print(f"You haven't found the {area} key\nTry again later")

    return area, pokemon, inventory, boss_beat


def save(area, pokemon, inventory, keys_found, boss_beat):
    account = input("Enter account you'd like to save under: ")
    with open(f"{account}area.txt", 'w') as f:
        f.write(area)

    with open(f"{account}pokemon.txt", 'wb') as f:
        pickle.dump(pokemon, f)

    with open(f"{account}inventory.txt", 'wb') as f:
        pickle.dump(inventory, f)

    with open(f"{account}keys_found.txt", 'wb') as f:
        pickle.dump(keys_found, f)

    with open(f"{account}boss_beat.txt", 'wb') as f:
        pickle.dump(boss_beat, f)


def main():
    while True:
        action = validate_string_input("\nWould like to load save (L) or Start new game (N): ", [
            'l', 'n'], "Enter (L / N) only!")
        if action == 'l':
            account = input("Enter account name you'd like to load: ")
            try:
                with open(f"{account}area.txt", "r") as f:
                    area = f.read()

                with open(f"{account}pokemon.txt", "rb") as f:
                    pokemon = pickle.loads(f.read())

                with open(f"{account}inventory.txt", "rb") as f:
                    inventory = pickle.loads(f.read())

                with open(f"{account}keys_found.txt", "rb") as f:
                    keys_found = pickle.loads(f.read())

                with open(f"{account}boss_beat.txt", "rb") as f:
                    boss_beat = pickle.loads(f.read())
                break

            except FileNotFoundError:
                print("Account not found")
        elif action == 'n':
            area, pokemon, inventory, keys_found, boss_beat, final_boss = start()
            break

    won = False
    while True:
        final_boss = True
        for i in boss_beat:
            if not boss_beat[i]:
                final_boss = False

        if won:
            print("\n\nTHANKS FOR PLAYING")
            print("Congratulations you have beaten Pokemon")
            break
        else:
            print(f"\nYou are at the {area}")
            print("You can: ")
            print("View Pokemon - (V)")
            print("Explore the area - (E)")
            print("Travel - (T)")
            print("Save Game - (S)")
            print("Quit Game - (Q)")
            action_choice = validate_string_input(
                "\nEnter action: ", ['v', 'e', 't', 's', 'q'], "Enter (V / E / T / S / Q) only!")
            if action_choice == 'v':
                pokemon, inventory = view_pokemon(pokemon, inventory)
            elif action_choice == 'e':
                pokemon, inventory, keys_found, won = explore(
                    area, pokemon, inventory, keys_found, final_boss)
            elif action_choice == 't':
                area, pokemon, inventory, boss_beat = travel(
                    area, keys_found, boss_beat, pokemon, inventory)
            elif action_choice == 's':
                save(area, pokemon, inventory, keys_found, boss_beat)
            elif action_choice == 'q':
                break


if __name__ == "__main__":
    main()
