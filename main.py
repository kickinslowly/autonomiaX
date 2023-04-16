import random
# list of all creatures in simulation, all dead creatures are removed at the end of eah cycle
creatures = []
# number of cycles of simulation that has been run, every cycle adds +1 to this variable
cycles = 0


class Creature():
    def __init__(self):
        self.location = [random.randint(-50, 50), random.randint(-50, 50)]
        self.alive = True
        # lifespan determines how many cycles the creature will live before dying
        self.lifespan = 5
        self.lifetime = 0
        self.health = 100
        self.reproduce = True
        self.speed = 1
        self.attack = 1
        self.defense = 1
        self.move = 1
        self.name = random.randint(1, 100000000)
        self.oxygen = 100
        self.carbon = 100
        self.nitrogen = 100

    def move(self):
        self.location[0] += 1
        self.location[1] += 1

    def eat(self, prey):
        self.oxygen += prey.oxygen
        self.carbon += prey.carbon
        self.nitrogen += prey.nitrogen

    def die(self):
        self.alive = False
        self.oxygen = 0
        self.nitrogen = 0
        self.carbon = 0
        print(f'{self.name} has died. {self.name} lived for {self.lifetime} cycles.')

    def reproduce(self):
        b = Creature()

    # main creature function called in cycle, other class functions will be embedded in this eventually, such as hunt, reproduce, eat
    def live(self):
        self.lifespan -= 1
        self.lifetime += 1
        print(f'{self.name} has {self.lifespan} cycle lives remaining.')
        if self.lifespan <= 0:
            print(f'{self.name} has died of old age.')
            self.die()



for i in range(0, 100):
    a = Creature()
    creatures.append(a)
    print(a.name)

while True:
    print(f'This is cycle {cycles}. There are {len(creatures)} creatures alive.')
    print(creatures)
    # adds +1 every time the simulation cycle runs
    cycles += 1
    # this loops through list of all creatures and calls their live() function
    for creature in creatures:
        creature.live()
    # this loops through list of all creatures and checks if they are alive, if not alive, get removed from creature list
    i = 0
    length = len(creatures)
    while i < length:
        if not creatures[i].alive:
            creatures.remove(creatures[i])
            length -= 1
            i -= 1
        i += 1
    # this checks if the creatures list is 0 and then breaks the loop if so. currently all creatures die after 5 cycles.
    if len(creatures) == 0:
        print('There are 0 creatures remaining.')
        break


