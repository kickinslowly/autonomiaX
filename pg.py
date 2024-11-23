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
    'Bacteria': (128, 0, 128),
    'Dead': (100, 100, 100)  # Color for dead creatures
}

# Define diets for each type of creature
diets = {
    'Bacteria': ['Plantista', 'Dead'],  # Bacteria can benefit from dead creatures
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

# Maximum size factors for different types of creatures
max_sizes = {
    'Bacteria': 5,
    'Protista': 8,
    'Plantista': 12,
    'Animalia': 15,
    'Fungi': 10
}

# Maximum number of creatures to prevent overpopulation
MAX_CREATURES = 150


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
        self.size = min(self.health * 10 * self.size_factor, max_sizes[creature_type])
        self.alive = True
        self.prey = None
        self.reproduction_count = 0
        self.last_reproduction_time = time.time()
        self.last_hunt_time = 0  # Track the time of the last successful hunt
        self.dead_mode = False  # Track if the creature is in "dead mode"
        self.death_time = None  # Time when the creature died
        self.buffed_creatures = set()  # Track dead creatures that have buffed this bacteria

    def move(self):
        if self.dead_mode:  # Dead creatures cannot move
            return
        if self.type == 'Plantista':
            return
        self.location[0] += random.randint(-self.speed, self.speed)
        self.location[1] += random.randint(-self.speed, self.speed)
        self.location[0] = max(1, min(self.location[0], WINDOW_WIDTH - 1))
        self.location[1] = max(1, min(self.location[1], WINDOW_HEIGHT - 1))

    def draw(self, screen):
        if self.dead_mode:
            color = colors['Dead']  # Use the dead color
            size = int(self.size)  # Use current size (which shrinks during fade-out)
        else:
            color = colors[self.type]
            size = int(self.size)
        pygame.draw.circle(screen, color, (int(self.location[0]), int(self.location[1])), size)

    def check_proximity(self, all_creatures):
        if self.dead_mode:  # Dead creatures cannot check proximity
            return False
        search_radius = 2000 if self.type != 'Bacteria' else 300
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
        if self.dead_mode:  # Dead creatures cannot hunt
            return
        # Enforce a 5-second cooldown after the last successful hunt
        current_time = time.time()
        if current_time - self.last_hunt_time < 5:
            return  # Skip hunting if cooldown is active

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
                self.size = min(self.health * 10 * self.size_factor, max_sizes[self.type])
                self.lifespan += 10
                self.prey = None
                self.last_hunt_time = current_time  # Update last hunt time

    def reproduce(self, all_creatures):
        if self.dead_mode:  # Dead creatures cannot reproduce
            return
        current_time = time.time()

        # Default reproduction thresholds
        reproduction_threshold = 1.5
        cooldown_period = 5
        energy_requirement = 3

        # Plantista and Bacteria reproduction overrides
        if self.type == 'Plantista' or self.type == 'Bacteria':
            reproduction_threshold = 0.3  # Lower health requirement
            cooldown_period = 1  # Faster reproduction
            energy_requirement = 0  # Minimal energy required

        # Enforce maximum creatures limit
        if len(all_creatures) >= MAX_CREATURES:
            return  # Stop reproduction if the limit is reached

        # Reproduction logic
        if self.health > reproduction_threshold and self.energy > energy_requirement:
            if self.type != 'Plantista' and self.reproduction_count >= 3:
                return  # Limit reproduction for non-Plants to 3 times

            if current_time - self.last_reproduction_time > cooldown_period:
                # Only reduce health and energy for non-Plantista types
                if self.type != 'Plantista':
                    self.health -= 0.2  # Reduce health
                    self.energy -= 0.5  # Reduce energy

                self.size = min(self.health * 10 * self.size_factor, max_sizes[self.type])

                # Generate independent random offsets for x and y
                offset_x = random.randint(-30, 30)
                offset_y = random.randint(-30, 30)
                new_location = [
                    max(0, min(self.location[0] + offset_x, WINDOW_WIDTH)),
                    max(0, min(self.location[1] + offset_y, WINDOW_HEIGHT))
                ]

                new_creature = Creature(location=new_location, creature_type=self.type, parent_id=self.id)
                new_creature.health = 0.8
                all_creatures.append(new_creature)

                # Increment reproduction count for non-Plantista types
                if self.type != 'Plantista':
                    self.reproduction_count += 1

                self.last_reproduction_time = current_time

    def check_lifespan(self):
        if self.dead_mode:  # Dead creatures are already "dead"
            return
        if self.energy <= 0 or time.time() > self.lifespan:
            self.die()

    def die(self):
        if self.dead_mode:
            return  # Already in dead mode
        self.alive = False
        self.dead_mode = True
        self.death_time = time.time()

    def handle_dead_mode(self, all_creatures):
        """Handle the dead mode effects."""
        elapsed_time = time.time() - self.death_time

        # Apply fade-out effect: progressively reduce size
        if elapsed_time <= 5:
            fade_factor = 1 - (elapsed_time / 5)  # Linear fade-out over 5 seconds
            self.size = max(1, self.size * fade_factor)  # Ensure size doesn't go below 1
        else:
            # Mark for removal after fade-out
            self.dead_mode = False
            self.alive = False


class World:
    def __init__(self):
        self.creatures = []
        self.populate()

    def populate(self):
        self.creatures.clear()  # Clear existing creatures before repopulating
        for _ in range(10):
            self.creatures.append(Creature(creature_type='Bacteria'))
        for _ in range(5):
            self.creatures.append(Creature(creature_type='Animalia'))
        for _ in range(5):
            self.creatures.append(Creature(creature_type='Protista'))
        for _ in range(10):  # Increase the number of initial plants
            self.creatures.append(Creature(creature_type='Plantista'))
        for _ in range(5):
            self.creatures.append(Creature(creature_type='Fungi'))

    def run(self):
        running = True
        while running:
            screen.fill(BACKGROUND_COLOR)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            # Remove creatures that are fully faded out
            self.creatures = [
                creature for creature in self.creatures
                if not creature.dead_mode or time.time() - creature.death_time <= 5
            ]

            # Check if only one creature is remaining
            if len([creature for creature in self.creatures if creature.alive]) <= 1:
                self.populate()

            for creature in self.creatures:
                if creature.alive:
                    creature.check_lifespan()
                    creature.hunt(self.creatures)
                    creature.move()
                    creature.reproduce(self.creatures)
                elif creature.dead_mode:
                    creature.handle_dead_mode(self.creatures)
                creature.draw(screen)

            pygame.display.flip()
            clock.tick(30)

        pygame.quit()


if __name__ == "__main__":
    world = World()
    world.run()
