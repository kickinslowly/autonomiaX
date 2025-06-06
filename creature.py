import random
import time
import turtle
import math

creatures = ['Bacteria', 'Animalia', 'Protista', 'Plantista', 'Fungi']
colors = ['green', 'blue', 'red', 'yellow', 'black']

class Creature:
    def __init__(self, location=None):
        if location is None:
            location = [random.randint(-400, 400), random.randint(-400, 400)]
        self.id = random.randint(1, 1000000000)
        self.type = 'creature'
        self.location = location
        self.carbon = 1
        self.nitrogen = 1
        self.oxygen = 1
        self.CO2 = 1
        self.health = .1
        self.attack = 0
        self.defense = 0
        self.speed = 50
        self.eats = []
        self.lifespan = time.time() + random.randint(0, 40)
        self.size = self.health
        self.baby = False
        self.alive = True
        self.turtle = turtle.Turtle()
        self.turtle.penup()
        self.turtle.shape('circle')

        self.turtle.goto(self.location[0], self.location[1])
        self.turtle.turtlesize(self.health)
        self.prey = None

    def move(self):
        self.turtle.goto(self.location[0], self.location[1])

    def check_proximity(self, all_creatures):
        for creature in all_creatures:
            if creature.id != self.id:  # to ensure it doesn't check distance to itself
                rough_distance_threshold = 50
                if abs(self.location[0] - creature.location[0]) < rough_distance_threshold and abs(self.location[1] - creature.location[1]) < rough_distance_threshold:
                    distance = math.sqrt((self.location[0] - creature.location[0]) ** 2 + (self.location[1] - creature.location[1]) ** 2)
                    if distance <= 25 and creature.type in self.eats:
                        self.prey = creature
                        break  # Exit the loop after finding the first close creature

    def hunt(self, all_creatures):
        if self.health > 10:
            pass
        else:
            self.check_proximity(all_creatures)
            if self.prey:
                self.location = self.prey.location
                self.move()
                self.eat(creature=self.prey)

    def eat(self, creature):
        creature.die()
        self.health += creature.health
        self.oxygen += creature.oxygen
        self.nitrogen += creature.nitrogen
        self.carbon += creature.carbon
        self.turtle.turtlesize(self.health)
        self.lifespan += 10


    def rest(self):
        pass

    def reproduce(self):
        self.baby = True

    def live(self, all_creatures):
        if self.type == 'Plantae' or self.type == 'Bacteria':
            self.health += self.health/4
        else:
            self.health -= self.health/4
        if self.health <= 0:
            self.die()
        else:
            self.reproduce()
            self.hunt(all_creatures)
        self.turtle.turtlesize(self.health)

        time.sleep(.2)

    def die(self):
        self.alive = False
        self.turtle.hideturtle()

    def evade(self):
        pass


class Bacteria(Creature):
    def __init__(self, location=None):
        if location is None:
            location = [random.randint(-400, 400), random.randint(-400, 400)]
        super().__init__(location)

        self.type = 'Bacteria'
        self.carbon = 1
        self.nitrogen = 1
        self.oxygen = 1
        self.health = .2
        self.attack = 1
        self.defense = 0
        self.speed = 0
        self.eats = []
        self.turtle.color('purple')
        self.turtle.turtlesize(self.health)

    def eat(self, creature):
        pass


class Protista(Creature):
    def __init__(self, location=None):
        if location is None:
            location = [random.randint(-400, 400), random.randint(-400, 400)]
        super().__init__(location)
        self.type = 'Protista'
        self.carbon = 5
        self.nitrogen = 5
        self.oxygen = 5
        self.health = .5
        self.attack = 1
        self.defense = 0
        self.speed = 1
        self.eats = ['Bacteria', 'Plantae']
        self.turtle.color('blue')
        self.turtle.turtlesize(self.health)

class Plantae(Creature):
    def __init__(self, location=None):
        if location is None:
            location = [random.randint(-400, 400), random.randint(-400, 400)]
        super().__init__(location)
        self.type = 'Plantae'
        self.carbon = 5
        self.nitrogen = 5
        self.oxygen = 5
        self.health = .5
        self.attack = 0
        self.defense = 1
        self.speed = 0
        self.turtle.color('green')
        self.turtle.turtlesize(self.health)

    def eat(self, creature):
        pass


class Fungi(Creature):
    def __init__(self, location=None):
        if location is None:
            location = [random.randint(-400, 400), random.randint(-400, 400)]
        super().__init__(location)
        self.type = 'Fungi'
        self.carbon = 5
        self.nitrogen = 5
        self.oxygen = 5
        self.health = .5
        self.attack = 1
        self.defense = 1
        self.speed = 0
        self.eats = ['Bacteria', 'Plantae', 'Fungi']
        self.turtle.color('yellow')
        self.turtle.turtlesize(self.health)


class Animalia(Creature):
    def __init__(self, location=None):
        if location is None:
            location = [random.randint(-400, 400), random.randint(-400, 400)]
        super().__init__(location)
        self.type = 'Animalia'
        self.lifespan = time.time() + random.randint(0, 35)
        self.carbon = 5
        self.nitrogen = 5
        self.oxygen = 5
        self.health = 1
        self.attack = 10
        self.defense = 1
        self.speed = 1
        self.eats = ['Bacteria', 'Protista', 'Plantae', 'Fungi', 'Animalia']
        self.turtle.color('red')
        self.turtle.turtlesize(self.health)



