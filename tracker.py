import random
class _Combatant():
    def __init__(self):
        self.AC = 0
        self.HP = 0

def spill(fighter):
    fmt = "{id:d}\t{init:d}\t{name:s}\t\t{HP:d}\t{AC:d}"
    print(fmt.format(id=fighter.idx, init=fighter.initiative, name=fighter.name,
                     HP=fighter.HP, AC = fighter.AC))
    return

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

combatants = []
running = True

while running:
    
    if combatants != []:
        stats = "id\tinit\tname\t\tHP\tAC"
        print(stats)
        for fighter in combatants:
            spill(fighter)
    print("q = quit, n = new, r = reroll, e = edit, l = load, s = Save")
    command = input("? ")

    if command == "q":
        running = False

    if command == "n":
        newFighter = new_fighter()
        newFighter.idx = len(combatants)
        combatants.append(newFighter)
        combatants.sort(key=lambda x: x.initiative, reverse=True)

    if command == "r":
        PCs = input("PCs? ") in ["y", "yes"]
        for fighter in combatants:
            if PCs or not fighter.PC:
                fighter.initiative = random.randrange(1, 21) + fighter.modifier

    print("")
