import math

import pygame


class Visualizer:
    def __init__(self, screen_size, fps):
        self.screen_size = screen_size
        self.fps = fps
        self.screen = pygame.display.set_mode((self.screen_size, self.screen_size))
        pygame.display.set_caption("Wii Balance Board Center of Pressure")
        self.font = pygame.font.SysFont(None, 36)
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.clock = pygame.time.Clock()

    def draw_target(self):
        """Draw a target in the center of the screen with concentric circles."""
        center = self.screen_size // 2
        num_circles = 5
        circle_spacing = center // num_circles

        # Draw concentric circles
        for i in range(1, num_circles + 1):
            pygame.draw.circle(self.screen, self.BLACK, (center, center), i * circle_spacing, 1)

        # Draw crosshairs
        pygame.draw.line(self.screen, self.BLACK, (center, 0), (center, self.screen_size), 1)
        pygame.draw.line(self.screen, self.BLACK, (0, center), (self.screen_size, center), 1)

    @staticmethod
    def calculate_color(distance):
        """Calculate the color of the dot based on its distance from the center."""
        # Normalize distance to the range 0 (center) to 1 (edge)
        max_distance = 1  # Maximum distance in normalized coordinates
        normalized_distance = distance / max_distance

        # Calculate color as a gradient from red to green
        red = int(255 * normalized_distance)
        green = int(255 * (1 - normalized_distance))
        return red, green, 0

    def visualize_cop(self, x_cop, y_cop, weight_kg):
        """Visualize the center of pressure on the pygame window."""
        self.screen.fill(self.WHITE)

        # Draw the target
        self.draw_target()

        # Convert normalized CoP to screen coordinates (center is at half of screen size)
        center = self.screen_size // 2
        x_screen = int(center + x_cop * center)
        y_screen = int(center - y_cop * center)

        # Calculate the distance from the center
        distance = math.sqrt(x_cop ** 2 + y_cop ** 2)

        # Calculate the color of the dot based on its distance from the center
        color = self.calculate_color(distance)

        # Draw the center of pressure as a colored dot
        pygame.draw.circle(self.screen, color, (x_screen, y_screen), 30)

        # Render the weight text
        weight_text = self.font.render(f"Weight: {weight_kg:.2f} kg", True, self.BLACK)
        self.screen.blit(weight_text, (10, 10))

        # Update the display
        pygame.display.flip()

    def tick(self):
        self.clock.tick(self.fps)
