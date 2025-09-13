import pygame
import random
import statistics
import sys
import math
from pygame.locals import *

GOAL = 50000
num_rats = 20
initial_min_wt = 200
initial_max_wt = 600
initial_mode_wt = 300
mutate_odds = 0.15
mutate_min = 0.7
mutate_max = 1.5
litter_size = 12
litters_per_year = 12
generation_limit = 400

# ensure even number of rats for breeding pairs
if num_rats % 2 != 0:
    num_rats += 1

WIDTH, HEIGHT = 1000, 700
BACKGROUND_COLOR = (240, 240, 240)
TEXT_COLOR = (50, 50, 50)
BUTTON_COLOR = (70, 130, 180)
BUTTON_HOVER_COLOR = (100, 160, 210)
RAT_COLORS = [(139, 69, 19), (101, 67, 33), (121, 85, 72), (93, 64, 55)]


class Rat:
    def __init__(self, weight, x, y):
        self.weight = weight
        self.x = x
        self.y = y
        self.color = random.choice(RAT_COLORS)
        self.size = max(10, min(50, int(weight / 1000)))  # Visual size based on weight
        self.speed = random.uniform(0.5, 2.0)
        self.direction = random.uniform(0, 2 * math.pi)
        self.age = 0

    def update(self):
        # Move randomly
        self.direction += random.uniform(-0.2, 0.2)
        self.x += math.cos(self.direction) * self.speed
        self.y += math.sin(self.direction) * self.speed

        # Bounce off walls
        if self.x < 20 or self.x > WIDTH - 20:
            self.direction = math.pi - self.direction
        if self.y < 100 or self.y > HEIGHT - 100:
            self.direction = -self.direction

        self.x = max(20, min(WIDTH - 20, self.x))
        self.y = max(100, min(HEIGHT - 100, self.y))
        self.age += 1

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.size)
        # Draw weight text
        font = pygame.font.Font(None, 20)
        text = font.render(f"{self.weight}g", True, TEXT_COLOR)
        screen.blit(text, (int(self.x) - 20, int(self.y) - 25))


class Button:
    def __init__(self, x, y, width, height, text, action):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.action = action
        self.hovered = False

    def draw(self, screen):
        color = BUTTON_HOVER_COLOR if self.hovered else BUTTON_COLOR
        pygame.draw.rect(screen, color, self.rect, border_radius=8)
        pygame.draw.rect(screen, (50, 50, 50), self.rect, 2, border_radius=8)

        font = pygame.font.Font(None, 24)
        text_surf = font.render(self.text, True, (255, 255, 255))
        text_rect = text_surf.get_rect(center=self.rect.center)
        screen.blit(text_surf, text_rect)

    def check_hover(self, pos):
        self.hovered = self.rect.collidepoint(pos)
        return self.hovered

    def check_click(self, pos):
        return self.rect.collidepoint(pos)


def populate(num_rats, min_wt, max_wt, mode_wt):
    """Initialise a population with a triangular distribution of weights."""
    return [int(random.triangular(min_wt, max_wt, mode_wt)) for i in range(num_rats)]


def fitness(population, goal):
    """Measure population fitness based on attribute mean vs target."""
    ave = statistics.mean(population)
    return ave / goal


def select(population, to_retain):
    """Cull a population to retain only a specified number of members."""
    sorted_population = sorted(population)
    to_retain_by_sex = to_retain // 2
    members_per_sex = len(sorted_population) // 2
    females = sorted_population[:members_per_sex]
    males = sorted_population[members_per_sex:]
    selected_females = females[-to_retain_by_sex:]
    selected_males = males[-to_retain_by_sex:]
    return selected_females, selected_males


def breed(males, females, litter_size):
    """Crossover genes among members (weights) of a population."""
    random.shuffle(males)
    random.shuffle(females)
    children = []
    for male, female in zip(males, females):
        for child in range(litter_size):
            # Ensure we always have the smaller value first
            low = min(female, male)
            high = max(female, male)
            child_weight = random.randint(low, high)
            children.append(child_weight)
    return children


def mutate(children, mutate_odds, mutate_min, mutate_max):
    """Randomly alter rat weights using input odds and fractional changes."""
    for index, rat in enumerate(children):
        if mutate_odds >= random.random():
            children[index] = round(rat * random.uniform(mutate_min, mutate_max))
    return children


class SuperRatsSimulation:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("SuperRats Genetic Algorithm Simulation")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 32)
        self.small_font = pygame.font.Font(None, 24)

        # Simulation parameters
        self.generation = 0
        self.rat_objects = []
        self.population_weights = []
        self.paused = False
        self.speed = 1
        self.avg_weights = []
        self.max_weights = []

        # Buttons
        self.buttons = [
            Button(20, 20, 120, 40, "Pause/Resume", self.toggle_pause),
            Button(150, 20, 120, 40, "Speed +", self.increase_speed),
            Button(280, 20, 120, 40, "Speed -", self.decrease_speed),
            Button(410, 20, 120, 40, "Reset", self.reset_simulation),
            Button(540, 20, 150, 40, "Next Generation", self.next_generation)
        ]

        self.initialise_population()

    def initialise_population(self):
        self.population_weights = populate(num_rats, initial_min_wt, initial_max_wt, initial_mode_wt)
        self.rat_objects = []
        for i, weight in enumerate(self.population_weights):
            x = random.randint(50, WIDTH - 50)
            y = random.randint(150, HEIGHT - 150)
            self.rat_objects.append(Rat(weight, x, y))

    def toggle_pause(self):
        self.paused = not self.paused

    def increase_speed(self):
        self.speed = min(5, self.speed + 0.5)

    def decrease_speed(self):
        self.speed = max(0.5, self.speed - 0.5)

    def reset_simulation(self):
        self.generation = 0
        self.avg_weights = []
        self.max_weights = []
        self.initialise_population()
        self.paused = False

    def next_generation(self):
        if self.paused:
            return

        # Genetic algorithm operations
        selected_females, selected_males = select(self.population_weights, num_rats)
        children = breed(selected_males, selected_females, litter_size)
        children = mutate(children, mutate_odds, mutate_min, mutate_max)

        # Create new population
        self.population_weights = selected_males + selected_females + children

        # Update rat objects for visualization
        self.rat_objects = []
        for i, weight in enumerate(self.population_weights):
            x = random.randint(50, WIDTH - 50)
            y = random.randint(150, HEIGHT - 150)
            self.rat_objects.append(Rat(weight, x, y))

        self.generation += 1

        # Record data
        self.avg_weights.append(statistics.mean(self.population_weights))
        self.max_weights.append(max(self.population_weights))

    def draw_ui(self):
        # Draw background
        self.screen.fill(BACKGROUND_COLOR)

        # Draw title and info
        title = self.font.render("SuperRats Genetic Algorithm Simulation", True, TEXT_COLOR)
        self.screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 5))

        current_avg = statistics.mean(self.population_weights) if self.population_weights else 0
        current_max = max(self.population_weights) if self.population_weights else 0

        info_text = f"Generation: {self.generation} | Rats: {len(self.population_weights)} | "
        info_text += f"Avg Weight: {current_avg:.0f}g | "
        info_text += f"Max Weight: {current_max}g | "
        info_text += f"Goal: {GOAL}g"

        info = self.small_font.render(info_text, True, TEXT_COLOR)
        self.screen.blit(info, (20, 70))

        # Draw progress bar
        max_weight = current_max
        progress = min(1.0, max_weight / GOAL)
        bar_width = 300
        pygame.draw.rect(self.screen, (200, 200, 200), (WIDTH - bar_width - 20, 70, bar_width, 20))
        pygame.draw.rect(self.screen, (0, 150, 0), (WIDTH - bar_width - 20, 70, int(bar_width * progress), 20))

        # Draw generation info
        gen_info = f"Mutation: {mutate_odds * 100}% | Litter Size: {litter_size} | "
        gen_info += f"Years: {self.generation / litters_per_year:.1f}"
        gen_text = self.small_font.render(gen_info, True, TEXT_COLOR)
        self.screen.blit(gen_text, (20, 100))

        # Draw buttons
        for button in self.buttons:
            button.draw(self.screen)

        # Draw generation graph if we have data
        if len(self.avg_weights) > 1:
            self.draw_generation_graph()

    def draw_generation_graph(self):
        # Simple line graph of average weights
        graph_rect = pygame.Rect(20, HEIGHT - 200, WIDTH - 40, 180)
        pygame.draw.rect(self.screen, (255, 255, 255), graph_rect)
        pygame.draw.rect(self.screen, TEXT_COLOR, graph_rect, 2)

        if len(self.avg_weights) > 1:
            max_val = max(max(self.avg_weights), max(self.max_weights), GOAL)

            # Draw average weight line
            avg_points = []
            for i, weight in enumerate(self.avg_weights):
                x = graph_rect.left + (i / (len(self.avg_weights) - 1)) * (graph_rect.width - 20)
                y = graph_rect.bottom - (weight / max_val) * (graph_rect.height - 20)
                avg_points.append((x, y))

            if len(avg_points) > 1:
                pygame.draw.lines(self.screen, (255, 0, 0), False, avg_points, 2)

            # Draw max weight line
            max_points = []
            for i, weight in enumerate(self.max_weights):
                x = graph_rect.left + (i / (len(self.max_weights) - 1)) * (graph_rect.width - 20)
                y = graph_rect.bottom - (weight / max_val) * (graph_rect.height - 20)
                max_points.append((x, y))

            if len(max_points) > 1:
                pygame.draw.lines(self.screen, (0, 0, 255), False, max_points, 2)

            # Draw goal line
            goal_y = graph_rect.bottom - (GOAL / max_val) * (graph_rect.height - 20)
            pygame.draw.line(self.screen, (0, 150, 0),
                             (graph_rect.left, goal_y),
                             (graph_rect.right, goal_y), 2)

            # Draw labels
            goal_label = self.small_font.render(f"Goal: {GOAL}g", True, (0, 100, 0))
            self.screen.blit(goal_label, (graph_rect.right - 100, goal_y - 20))

            # Draw legend
            avg_label = self.small_font.render("Avg Weight", True, (255, 0, 0))
            max_label = self.small_font.render("Max Weight", True, (0, 0, 255))
            self.screen.blit(avg_label, (graph_rect.left + 10, graph_rect.top + 5))
            self.screen.blit(max_label, (graph_rect.left + 10, graph_rect.top + 25))

    def run(self):
        running = True
        auto_advance_timer = 0

        while running:
            dt = self.clock.tick(60) / 1000.0  # Delta time in seconds
            mouse_pos = pygame.mouse.get_pos()

            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False
                elif event.type == MOUSEBUTTONDOWN:
                    for button in self.buttons:
                        if button.check_click(mouse_pos):
                            button.action()

            # Update button hover states
            for button in self.buttons:
                button.check_hover(mouse_pos)

            # Update simulation if not paused
            if not self.paused:
                # Auto-advance generations every 2 seconds
                auto_advance_timer += dt
                if auto_advance_timer >= 2.0 / self.speed:
                    self.next_generation()
                    auto_advance_timer = 0

                # Update rat animations
                for rat in self.rat_objects:
                    rat.update()

            # Draw everything
            self.draw_ui()

            # Draw rats
            for rat in self.rat_objects:
                rat.draw(self.screen)

            # Check if goal is reached
            if self.population_weights and max(self.population_weights) >= GOAL:
                congrats = self.font.render("GOAL ACHIEVED! SUPER RAT CREATED!", True, (255, 0, 0))
                self.screen.blit(congrats, (WIDTH // 2 - congrats.get_width() // 2, HEIGHT // 2 - 50))
                self.paused = True

            pygame.display.flip()

        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    simulation = SuperRatsSimulation()
    simulation.run()
