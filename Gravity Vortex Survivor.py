import pygame
import math
import random

# Initialize Pygame
pygame.init()
pygame.mixer.init()

# Game constants
WIDTH, HEIGHT = 1200, 800
FPS = 60
G = 0.2  # Further reduced gravitational constant
SHIP_ROTATION_SPEED = 5  # Faster rotation
SHIP_THRUST = 0.3  # Increased thrust
REVERSE_THRUST = 0.15  # Added reverse thrust
FUEL_CONSUMPTION = 0.2  # Reduced fuel consumption
MAX_FUEL = 1000
SAFE_SPAWN_RADIUS = 200
INERTIA_DAMPING = 0.98  # Slows down the ship over time
BOOST_MULTIPLIER = 2.0  # Boost speed multiplier
BOOST_FUEL_COST = 1.0  # Fuel cost for boosting

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

# Initialize screen and clock
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Gravity Vortex Survivor - Improved Controls")
clock = pygame.time.Clock()

# Load assets
ship_img = pygame.Surface((30, 40), pygame.SRCALPHA)
pygame.draw.polygon(ship_img, WHITE, [(15, 0), (0, 40), (30, 40)])
ship_mask = pygame.mask.from_surface(ship_img)

core_img = pygame.Surface((20, 20), pygame.SRCALPHA)
pygame.draw.circle(core_img, YELLOW, (10, 10), 8)
fuel_img = pygame.Surface((15, 15), pygame.SRCALPHA)
pygame.draw.circle(fuel_img, BLUE, (7, 7), 5)


class Ship(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = ship_img
        self.original_image = self.image
        self.rect = self.image.get_rect(center=(WIDTH / 2, HEIGHT / 2))
        self.mask = ship_mask
        self.pos = pygame.Vector2(self.rect.center)
        self.vel = pygame.Vector2(0, 0)
        self.angle = 0
        self.fuel = MAX_FUEL
        self.radius = 15
        self.boosting = False

    def update(self):
        # Apply inertia damping
        self.vel *= INERTIA_DAMPING
        self.pos += self.vel
        self.rect.center = self.pos

        # Screen wrapping
        if self.pos.x > WIDTH + self.radius:
            self.pos.x = -self.radius
        if self.pos.x < -self.radius:
            self.pos.x = WIDTH + self.radius
        if self.pos.y > HEIGHT + self.radius:
            self.pos.y = -self.radius
        if self.pos.y < -self.radius:
            self.pos.y = HEIGHT + self.radius

    def rotate(self, direction):
        self.angle += direction * SHIP_ROTATION_SPEED
        self.image = pygame.transform.rotate(self.original_image, self.angle)
        self.rect = self.image.get_rect(center=self.rect.center)
        self.mask = pygame.mask.from_surface(self.image)

    def thrust(self, reverse=False, boost=False):
        if self.fuel > 0:
            angle_rad = math.radians(self.angle)
            thrust_power = REVERSE_THRUST if reverse else SHIP_THRUST
            if boost:
                thrust_power *= BOOST_MULTIPLIER
                self.fuel -= BOOST_FUEL_COST
            self.vel.x += math.cos(angle_rad) * thrust_power * (1 if not reverse else -1)
            self.vel.y -= math.sin(angle_rad) * thrust_power * (1 if not reverse else -1)
            self.fuel -= FUEL_CONSUMPTION


class Planet(pygame.sprite.Sprite):
    def __init__(self, size):
        super().__init__()
        self.size = size
        self.image = pygame.Surface((size * 2, size * 2), pygame.SRCALPHA)
        pygame.draw.circle(self.image, RED, (size, size), size)
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.mass = size * 6  # Reduced mass
        self.radius = size


class EnergyCore(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.image = core_img
        self.rect = self.image.get_rect(center=pos)
        self.mask = pygame.mask.from_surface(self.image)


class FuelPod(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.image = fuel_img
        self.rect = self.image.get_rect(center=pos)
        self.mask = pygame.mask.from_surface(self.image)


def main():
    running = True
    score = 0
    game_time = 0
    font = pygame.font.Font(None, 36)

    # Create groups
    all_sprites = pygame.sprite.Group()
    planets = pygame.sprite.Group()
    cores = pygame.sprite.Group()
    fuel_pods = pygame.sprite.Group()

    # Create ship
    ship = Ship()
    all_sprites.add(ship)

    # Generate planets with safe spawn area
    ship_spawn = pygame.Rect(WIDTH / 2 - SAFE_SPAWN_RADIUS, HEIGHT / 2 - SAFE_SPAWN_RADIUS,
                             SAFE_SPAWN_RADIUS * 2, SAFE_SPAWN_RADIUS * 2)

    for _ in range(random.randint(4, 6)):
        size = random.randint(50, 80)
        planet = Planet(size)
        attempts = 0
        while True:
            planet.rect.center = (random.randint(0, WIDTH), random.randint(0, HEIGHT))
            if not ship_spawn.collidepoint(planet.rect.center) and \
                    not pygame.sprite.spritecollide(planet, planets, False,
                                                    lambda a, b: pygame.sprite.collide_circle(a, b)):
                break
            attempts += 1
            if attempts > 100:
                break
        planets.add(planet)
        all_sprites.add(planet)

    # Generate initial cores and fuel pods
    for _ in range(10):
        pos = (random.randint(0, WIDTH), random.randint(0, HEIGHT))
        while ship_spawn.collidepoint(pos):
            pos = (random.randint(0, WIDTH), random.randint(0, HEIGHT))
        core = EnergyCore(pos)
        cores.add(core)
        all_sprites.add(core)

    for _ in range(5):
        pos = (random.randint(0, WIDTH), random.randint(0, HEIGHT))
        while ship_spawn.collidepoint(pos):
            pos = (random.randint(0, WIDTH), random.randint(0, HEIGHT))
        fuel_pod = FuelPod(pos)
        fuel_pods.add(fuel_pod)
        all_sprites.add(fuel_pod)

    while running:
        clock.tick(FPS)
        game_time += 1 / FPS

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            ship.rotate(-1)
        if keys[pygame.K_RIGHT]:
            ship.rotate(1)
        if keys[pygame.K_UP]:
            ship.thrust(boost=keys[pygame.K_LSHIFT])
        if keys[pygame.K_DOWN]:
            ship.thrust(reverse=True)

        # Apply planetary gravity
        for planet in planets:
            dx = planet.rect.centerx - ship.pos.x
            dy = planet.rect.centery - ship.pos.y
            distance = math.hypot(dx, dy)
            if distance == 0:
                continue
            force = G * (planet.mass) / (distance ** 1.5)
            angle = math.atan2(dy, dx)
            ship.vel.x += math.cos(angle) * force
            ship.vel.y += math.sin(angle) * force

        all_sprites.update()

        # Check collisions
        if pygame.sprite.spritecollide(ship, planets, False, pygame.sprite.collide_mask):
            running = False

        core_collected = pygame.sprite.spritecollide(ship, cores, True, pygame.sprite.collide_mask)
        if core_collected:
            score += 100
            core = EnergyCore((random.randint(0, WIDTH), random.randint(0, HEIGHT)))
            cores.add(core)
            all_sprites.add(core)

        fuel_collected = pygame.sprite.spritecollide(ship, fuel_pods, True, pygame.sprite.collide_mask)
        if fuel_collected:
            ship.fuel = min(ship.fuel + 200, MAX_FUEL)
            fuel_pod = FuelPod((random.randint(0, WIDTH), random.randint(0, HEIGHT)))
            fuel_pods.add(fuel_pod)
            all_sprites.add(fuel_pod)

        # End game only when fuel completely depletes
        if ship.fuel <= 0:
            ship.fuel = 0
            if ship.vel.length() < 0.1:
                running = False

        # Render
        screen.fill(BLACK)
        all_sprites.draw(screen)

        # Draw HUD
        fuel_text = font.render(f"Fuel: {int(ship.fuel)}", True, WHITE)
        score_text = font.render(f"Score: {score}", True, WHITE)
        time_text = font.render(f"Time: {int(game_time)}s", True, WHITE)
        screen.blit(fuel_text, (10, 10))
        screen.blit(score_text, (10, 40))
        screen.blit(time_text, (10, 70))

        pygame.display.flip()

    # Game Over
    screen.fill(BLACK)
    game_over_text = font.render(f"Game Over! Final Score: {score}", True, WHITE)
    screen.blit(game_over_text, (WIDTH // 2 - 150, HEIGHT // 2))
    pygame.display.flip()
    pygame.time.wait(3000)

    pygame.quit()


if __name__ == "__main__":
    main()