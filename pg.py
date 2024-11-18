import pygame
import random
import time
import math

# Initialize Pygame
pygame.init()

# Set up full-screen mode
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
pygame.display.set_caption("Creature Simulation")
clock = pygame.time.Clock()

# Get the screen dimensions dynamically
WINDOW_WIDTH, WINDOW_HEIGHT = screen.get_size()
BACKGROUND_COLOR = (30, 30, 30)

# Define colors for different types of creatures
colors = {
    'Fungi': (255, 255, 0),
    'Animalia': (255, 0, 0),
    'Protista': (0, 0, 255),
    'Plantista': (0, 255, 0),
    'Bacteria': (128, 0, 128)
}

# Define diets for each type of creature
diets = {
    'Bacteria': [],
    'Animalia': ['Protista', 'Plantista', 'Animalia'],
    'Protista': ['Bacteria', 'Protista'],
    'Plantista': [],
    'Fungi': ['Bacteria', 'Plantista', 'Fungi']
}

# Define size factors for different types of creatures
size_factors = {
    'Bacteria': 0.5,
    'Protista': 0.75,
    'Plantista': 1.0,
    'Animalia': 1.0,
    'Fungi': 1.0
}

# Maximum number of creatures to prevent overpopulation
MAX_CREATURES = 1000


class Creature:
    def __init__(self, location=None, creature_type='Bacteria', parent_id=None):
        if location is None:
            location = [random.randint(0, WINDOW_WIDTH), random.randint(0, WINDOW_HEIGHT)]
        self.id = random.randint(1, 1000000000)
        self.type = creature_type
        self.parent_id = parent_id
        self.location = location
        self.health = 1.0
        self.energy = 5.0
        self.speed = 1 if creature_type == 'Fungi' else 2
        self.eats = diets[creature_type]
        self.lifespan = time.time() + random.randint(20, 60)
        self.size_factor = size_factors[creature_type]
        self.size = self.health * 10 * self.size_factor
        self.alive = True
        self.prey = None
        self.reproduction_count = 0
        self.last_reproduction_time = time.time()

    def move(self):
        if self.type == 'Plantista':
            return
        self.location[0] += random.randint(-self.speed, self.speed)
        self.location[1] += random.randint(-self.speed, self.speed)
        self.location[0] = max(0, min(self.location[0], WINDOW_WIDTH))
        self.location[1] = max(0, min(self.location[1], WINDOW_HEIGHT))

    def draw(self, screen):
        pygame.draw.circle(screen, colors[self.type], (int(self.location[0]), int(self.location[1])), int(self.size))

    def check_proximity(self, all_creatures):
        search_radius = 2000 if self.type != 'Bacteria' else 500
        closest_distance = search_radius
        closest_prey = None

        for creature in all_creatures:
            if creature.id != self.id and creature.alive and creature.type in self.eats:
                if creature.id == self.parent_id or creature.parent_id == self.id:
                    continue
                distance = math.sqrt((self.location[0] - creature.location[0]) ** 2 +
                                     (self.location[1] - creature.location[1]) ** 2)
                if distance < closest_distance:
                    closest_distance = distance
                    closest_prey = creature

        if closest_prey:
            self.prey = closest_prey
            return True
        else:
            self.prey = None
            return False

    def hunt(self, all_creatures):
        if self.check_proximity(all_creatures) and self.prey:
            prey_x, prey_y = self.prey.location
            direction_x = prey_x - self.location[0]
            direction_y = prey_y - self.location[1]
            distance = math.sqrt(direction_x ** 2 + direction_y ** 2)

            if distance > 5:
                self.location[0] += (direction_x / distance) * self.speed
                self.location[1] += (direction_y / distance) * self.speed
            else:
                self.prey.die()
                self.health += 0.5
                self.energy += 2
                self.size = self.health * 10 * self.size_factor
                self.lifespan += 10
                self.prey = None

    def reproduce(self, all_creatures):
        current_time = time.time()
        reproduction_threshold = 1.5 if self.type != 'Bacteria' else 1.0
        cooldown_period = 5 if self.type != 'Bacteria' else 3

        if self.health > reproduction_threshold and self.reproduction_count < 2 and self.energy > 3:
            if current_time - self.last_reproduction_time > cooldown_period:
                if len(all_creatures) < MAX_CREATURES:
                    self.health -= 0.5
                    self.energy -= 2
                    self.size = self.health * 10 * self.size_factor
                    offset = random.randint(-20, 20)
                    new_location = [self.location[0] + offset, self.location[1] + offset]

                    new_creature = Creature(location=new_location, creature_type=self.type, parent_id=self.id)
                    new_creature.health = 0.8
                    all_creatures.append(new_creature)

                    self.reproduction_count += 1
                    self.last_reproduction_time = current_time

                    if self.reproduction_count >= 2:
                        self.die()

    def check_lifespan(self):
        if time.time() > self.lifespan or self.energy <= 0:
            self.die()

    def die(self):
        self.alive = False


class World:
    def __init__(self):
        self.creatures = []
        self.populate()

    def populate(self):
        for _ in range(10):
            self.creatures.append(Creature(creature_type='Bacteria'))
        for _ in range(5):
            self.creatures.append(Creature(creature_type='Animalia'))
        for _ in range(5):
            self.creatures.append(Creature(creature_type='Protista'))
        for _ in range(5):
            self.creatures.append(Creature(creature_type='Plantista'))
        for _ in range(5):
            self.creatures.append(Creature(creature_type='Fungi'))

    def reset_simulation(self):
        """Restart the simulation by clearing and repopulating creatures."""
        self.creatures.clear()
        self.populate()

    def run(self):
        running = True
        while running:
            screen.fill(BACKGROUND_COLOR)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            # Check if only one creature is remaining
            if len([creature for creature in self.creatures if creature.alive]) <= 1:
                self.reset_simulation()

            for creature in self.creatures:
                if creature.alive:
                    creature.check_lifespan()
                    creature.hunt(self.creatures)
                    creature.move()
                    creature.reproduce(self.creatures)
                    creature.draw(screen)

            pygame.display.flip()
            clock.tick(30)

        pygame.quit()


if __name__ == "__main__":
    world = World()
    world.run()
