import random
import creature
import time
import turtle
import multiprocessing
import cProfile

screen = turtle.Screen()
screen.title("Autonomia-X")
screen.tracer(1, 10)
creature_classes = {'Bacteria': creature.Bacteria,
                    'Protista': creature.Protista,
                    'Plantae': creature.Plantae,
                    'Fungi': creature.Fungi,
                    'Animalia': creature.Animalia}


# main class for autonomia2 world
class World:
    def __init__(self):
        self.status = True
        self.start_time = time.time()
        self.carbon = 100
        self.nitrogen = 100
        self.oxygen = 100
        self.CO2 = 100
        self.resources = {'Carbon': self.carbon,
                          'Nitrogen': self.nitrogen,
                          'Oxygen': self.oxygen}
        self.bacteria = []
        self.protista = []
        self.plantae = []
        self.fungi = []
        self.animalia = []
        self.creatures = [self.bacteria, self.protista, self.plantae, self.fungi, self.animalia]
        self.total_creatures = 0
        self.total_creatures_text = f'Total Creatures: {self.total_creatures}'
        self.total_creatures_text_turtle = turtle.Turtle()
        # Set the turtle to display creature count
        self.total_creatures_text_turtle.penup()
        self.total_creatures_text_turtle.goto(-350, 350)
        self.total_creatures_text_turtle.write(self.total_creatures_text, align="center", font=("Arial", 16, "bold"))
        self.total_creatures_text_turtle.hideturtle()

    # checks if any  creatures are past their intended lifespan and removes them if so
    def checkalive(self, each, to_remove, now):
        if now >= each.lifespan:
            each.die()
            to_remove.append(each)
            return False
        elif each.alive == False:
            each.die()
            to_remove.append(each)
            return False

    # initial population of world, should only run once
    def populate(self):
        total = 10
        screen.tracer(0)
        for i in range(0, total):
            new_creature = creature.Bacteria()
            self.bacteria.append(new_creature)
        for i in range(0, total):
            new_creature = creature.Plantae()
            self.plantae.append(new_creature)
        for i in range(0, total):
            new_creature = creature.Protista()
            self.protista.append(new_creature)
        for i in range(0, total):
            new_creature = creature.Fungi()
            self.fungi.append(new_creature)
        for i in range(0, total):
            new_creature = creature.Animalia()
            self.animalia.append(new_creature)
        screen.tracer(1, 10)

    # refreshes current creatures in world
    def update(self):
        self.total_creatures = len(self.bacteria) + len(self.protista) + len(self.plantae) + len(self.fungi) + len(self.animalia)

    def print_update(self):
        while True:
            self.update()
            print(self.total_creatures)

    def reproduction(self, each):
        if each.baby:
            screen.tracer(0)
            creature_class = creature_classes[each.type]
            i = creature_class(location=[each.location[0], each.location[1]])
            if i.type == 'Bacteria':
                j = creature_class(location=[each.location[0] + 10, each.location[1] + 10])
                self.bacteria.append(i)
                self.bacteria.append(j)
            elif i.type == 'Fungi':
                self.fungi.append(i)
            elif i.type == 'Plantae':
                j = creature_class(location=[each.location[0] + 10, each.location[1] + 10])
                self.plantae.append(i)
                self.plantae.append(j)
            elif i.type == 'Protista':
                self.protista.append(i)
            elif i.type == 'Animalia':
                self.animalia.append(i)
            screen.tracer(1, 10)

    def shuffle(self, life_cycle):
        for kingdom in self.creatures:
            for each_creature in kingdom:
                life_cycle.append(each_creature)
        random.shuffle(life_cycle)

    def total_creatures_text_print(self):
        self.update()
        self.total_creatures_text = f'Total Creatures: {self.total_creatures}'
        self.total_creatures_text_turtle.clear()
        self.total_creatures_text_turtle.write(self.total_creatures_text, align="center", font=("Arial", 16, "bold"))
        print(f'total creatures: {self.total_creatures}')

    # main function that loops constantly
    def run(self):
        self.populate()
        while True:
            life_cycle = []
            to_remove = []
            self.shuffle(life_cycle)
            for i in range(0, len(life_cycle)):
                each = life_cycle[i]
                now = time.time()
                if self.checkalive(each, to_remove, now) == False:
                    pass
                elif each:
                    self.reproduction(each)
                    each.live(all_creatures=life_cycle)

            to_remove_set = set(to_remove)
            for kingdom in self.creatures:
                # Process creatures that need to die
                for each in filter(to_remove_set.__contains__, kingdom):
                    each.die()
                # Remove creatures efficiently
                kingdom[:] = [each for each in kingdom if each not in to_remove_set]
            self.total_creatures_text_print()


a = World()
a.run()


