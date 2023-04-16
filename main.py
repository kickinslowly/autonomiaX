import random

creatures = []
cycles = 0


class Creature():
    def __init__(self):
        self.location = [random.randint(-50, 50), random.randint(-50, 50)]
        self.alive = True
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
    # if creatures == 0:
    #     break
    cycles += 1
    # this loops through list of all creatures and reduces their lifespan by 1 for every cycle run
    ## moved this loop inside live function in creature class and changed it accordingly
    for creature in creatures:
        creature.live()
    i = 0
    length = len(creatures)
    while i < length:
        if not creatures[i].alive:
            creatures.remove(creatures[i])
            length -= 1
            i -= 1
        i += 1
    if len(creatures) == 0:
        print('There are 0 creatures remaining.')
        break


