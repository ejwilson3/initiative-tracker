#!/usr/bin/env python
import random

################################################################################
# DEFINE CLASSES, FUNCTIONS, AND SUBROUTINES
################################################################################

# Class to contain the information for each combatant
class _Combatant():
    def __init__(self):
        self.AC = 0
        self.HP = 1

    # Display relevant information for the combatant in question
    def spill(self):
        fmt = "{id:d}\t{init:d}\t{name:s}\t\t{HP:d}\t{AC:d}"
        if len(fighter.name) > 7:
            fmt = "{id:d}\t{init:d}\t{name:s}\t{HP:d}\t{AC:d}"
        print(fmt.format(id=fighter.idx, init=fighter.initiative,
                         name=fighter.name, HP=fighter.HP, AC = fighter.AC))
        return

# Create a new Combatant. Different from the _Combatant.init() because they
# don't need to enter information if it's being loaded from a file.
def new_fighter():
    newFighter = _Combatant()
    NPC = ""
    while (NPC != "NPC" and NPC != "PC"):
        NPC = input("NPC or PC? ")
    newFighter.PC = (NPC ==  "PC")
    newFighter.name = input("Name: ")[:15]
    modifier = input("Modifier: ")
    if (modifier[0] == "+"):
        modifier = modifier[1:]
    try:
        newFighter.modifier = int(modifier)
    except ValueError:
        # TODO Find a better way to do this; modifier can't be changed later.
        print("What are you doing? Setting it to 0.")
        newFighter.modifier = 0
    newFighter.initiative = random.randrange(1, 21) + newFighter.modifier
    return newFighter

################################################################################
# END OF DEFINITIONS
################################################################################

combatants = []
running = True

while running:
 
    if combatants != []:
        stats = "id\tinit\tname\t\tHP\tAC"
        print(stats)

        # We're just using a simple terminal display, so we have to print out
        # the entire initiative list every time.
        for fighter in combatants:
            fighter.spill()

    command = input("? ")

    # Replace all of this with a switch?
    # Turns out they don't have real switches in Python...
    # Damage a combatant
    if command == "d" or command == "damage":
        try:
            editee = _Combatant()
            idx = int(input("idx "))
            # TODO Find a way to break if fighter not found, instead of making
            # user go through the rest of "d".
            for fighter in combatants:
                if fighter.idx == idx:
                    editee = fighter
                    break
            damage = int(input("damage "))
            editee.HP -= damage
            if editee.HP <= 0:
                editee.HP = 0 
                if input("kill? ") in ["y", "yes"]:
                    combatants.remove(editee)
                    # This seems inefficient. Only an insane GM would have
                    # enough people in a single combat for it to matter, but is
                    # there a better way?
                    for fighter in combatants:
                        if fighter.idx > idx:
                            fighter.idx -= 1
        except ValueError:
            print("What are you doing?")        

    # Edit the information for a combatant. This is important because I don't
    # want to add so much for everyone, when it's an initiative tracker.
    elif command == "e" or command == "edit":
        try:
            editee = _Combatant()
            idx = int(input("idx "))
            for fighter in combatants:
                if fighter.idx == idx:
                    editee = fighter
                    break
            editee.HP = int(input("New HP "))
            editee.AC = int(input("New AC "))
            initiative = input("New Initiative? ")
            try:
                if initiative:
                    editee.initiative = int(initiative)
            except ValueError:
                pass
        except ValueError:
            print("What are you doing?")

    # Spit out list of commands
    elif command == "h" or command == "help":
        print("d = damage, e = edit, h = help, l = load, n = new, q = quit, "
              "r = reroll, s = save")

    # Load a file previously saved. Only accepts .txt files, and adds extension
    # automatically. Change this?
    elif command == "l" or command == "load":
        try:
            filename = input("filename ")
            f = open(filename + ".txt", "r")
            contents = f.read()
            contents = contents.split("\n")
            for fighter in contents:
                newFighter = _Combatant()
                fighter = fighter.split(",")
                newFighter.name = fighter[0]
                newFighter.initiative = int(fighter[1])
                newFighter.modifier = int(fighter[2])
                newFighter.HP = int(fighter[3])
                newFighter.AC = int(fighter[4])
                newFighter.PC = bool(fighter[5])
                newFighter.idx = len(combatants)
                combatants.append(newFighter)
            f.close()
        except FileNotFoundError:
            print("File not found")
        except:
            print("This file is not properly formatted.")

    # Add a new combatant.
    elif command == "n" or command == "new":
        newFighter = new_fighter()
        newFighter.idx = len(combatants)
        combatants.append(newFighter)
        combatants.sort(key=lambda x: x.initiative, reverse=True)

    # Quit the program.
    elif command == "q" or command == "quit":
        running = False

    # Reroll the initiatives. Always rerolls all of the NPCs, but you have the
    # option to reroll PCs too.
    elif command == "r" or command == "reroll":
        PCs = input("PCs? ") in ["y", "yes"]
        for fighter in combatants:
            if PCs or not fighter.PC:
                fighter.initiative = random.randrange(1, 21) + fighter.modifier
        combatants.sort(key=lambda x: x.initiative, reverse=True)

    # Save the current initiatives. Does not save IDs.
    elif command == "s" or command == "save":
        data = ''
        for fighter in combatants:
            data = data + fighter.name + "," + str(fighter.initiative) + "," + \
                        str(fighter.modifier) + "," + str(fighter.HP) + "," + \
                        str(fighter.AC) + "," + str(fighter.PC) + "\n"
        data = data[:-1]
        filename = input("filename ")
        try:
            f = open(filename + ".txt", "w")
            f.write(data)
            f.close()
        except FileNotFoundError:
            print("Something went wrong. Please try a different filename.")


    print("")
