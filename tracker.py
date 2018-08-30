import random
class _Combatant():
    def __init__(self):
        self.initiative = 0
        self.PC = False
        self.name = ""

def spill(fighter):
    print(fighter.name, fighter.initiative)
    return

def new_fighter():
    newFighter = _Combatant()
    NPC = ""
    while (NPC != "NPC" and NPC != "PC"):
        NPC = input("NPC or PC? ")
    newFighter.PC = (NPC ==  "PC")
    newFighter.name = input("Name: ")
    modifier = input("Modifier: ")
    #modifier = modifer
    newFighter.initiative = random.randrange(1, 21) + int(modifier)
    return newFighter

combatants = []
running = True

while running:
    
    if combatants != []:
        for fighter in combatants:
            spill(fighter)
    print("q = quit, n = new, r = reroll, e = edit, l = load, s = Save")
    command = input("? ")

    if command == "q":
        running = False

    if command == "n":
        newFighter = new_fighter()
        combatants.append(newFighter)
        combatants.sort(key=lambda x: x.initiative, reverse=True)

    print("")
