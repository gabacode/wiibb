import sys

import pygame

from wiibb import WiiBalanceBoard, Visualizer


class App:
    def __init__(self, screen_size=1024, fps=60):
        self.visualizer = Visualizer(screen_size, fps)
        self.wiibb = WiiBalanceBoard()

    def run(self):
        board = self.wiibb.get_device()
        if not board:
            sys.exit("Balance board not found.")

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            data = self.wiibb.get_raw_measurement()
            x_cop, y_cop = self.wiibb.calculate_cop(data)
            weight_kg = sum(data)
            self.visualizer.visualize_cop(x_cop, y_cop, weight_kg)
            self.visualizer.tick()


if __name__ == "__main__":
    App().run()
