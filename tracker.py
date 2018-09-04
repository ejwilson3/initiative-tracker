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
def spill(fighter):
    fmt = "{id:d}\t{init:d}\t{name:s}\t\t{HP:d}\t{AC:d}"
    print(fmt.format(id=fighter.idx, init=fighter.initiative, name=fighter.name,
                     HP=fighter.HP, AC = fighter.AC))
    return

# Create a new Combatant. Different from the _Combatant.init() because they
# don't need to enter information if it's being loaded from a file.
def new_fighter():
    newFighter = _Combatant()
    NPC = ""
    while (NPC != "NPC" and NPC != "PC"):
        NPC = input("NPC or PC? ")
    newFighter.PC = (NPC ==  "PC")
    newFighter.name = input("Name: ")
    newFighter.modifier = int(input("Modifier: "))
    #newFighter.modifier = modifer
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
            spill(fighter)

    print("q = quit, n = new, r = reroll, e = edit, l = load, s = Save, "
          "d = damage")
    command = input("? ")

    # Replace all of this with a switch?
    # Damage a combatant
    if command == "d":
        editee = _Combatant()
        idx = int(input("idx "))
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
                # This seems inefficient. Only an insane GM would have enough
                # people in a single combat for it to matter, but is there a
                # better way?
                for fighter in combatants:
                    if fighter.idx > idx:
                        fighter.idx -= 1

    # Edit the information for a combatant. This is important because I don't
    # want to add so much for everyone, when it's an initiative tracker.
    elif command == "e":
        editee = _Combatant()
        idx = int(input("idx "))
        for fighter in combatants:
            if fighter.idx == idx:
                editee = fighter
                break
        editee.HP = int(input("New HP "))
        editee.AC = int(input("New AC "))
        initiative = input("New Initiative? ")
        if initiative:
            editee.initiative = int(initiative)

    # Load a file previously saved.
    elif command == "l":
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

    # Add a new combatant.
    elif command == "n":
        newFighter = new_fighter()
        newFighter.idx = len(combatants)
        combatants.append(newFighter)
        combatants.sort(key=lambda x: x.initiative, reverse=True)

    # Quit the program.
    elif command == "q":
        running = False

    # Reroll the initiatives. Always rerolls all of the NPCs, but you have the
    # option to reroll PCs too.
    elif command == "r":
        PCs = input("PCs? ") in ["y", "yes"]
        for fighter in combatants:
            if PCs or not fighter.PC:
                fighter.initiative = random.randrange(1, 21) + fighter.modifier

    # Save the current initiatives. Does not save IDs.
    elif command == "s":
        data = ''
        for fighter in combatants:
            data = data + fighter.name + "," + str(fighter.initiative) + "," + \
                        str(fighter.modifier) + "," + str(fighter.HP) + "," + \
                        str(fighter.AC) + "," + str(fighter.PC) + "\n"
        data = data[:-1]
        filename = input("filename ")
        f = open(filename + ".txt", "w")
        f.write(data)
        f.close()


    print("")
