import pygame
import numpy as np
from tracker import HandTracker

class RobotArmSimulation:
    def __init__(self, arm_length=44, max_x=176, max_y=88):
        """
        Initializes simulation

        :param arm_length: simulated arm length, both arm will be this length
        :param max_x: total len of x axis
        :param may_y: total high on y axis
        """

        self.screen_widht = 854
        self.screen_hight = 480

        self.tracker = HandTracker()
        self.arm_length = self.screen_hight / 2
        self.max_x = self.screen_widht
        self.max_y = self.screen_hight

        self.x0 = self.screen_widht / 2
        self.y0 = self.screen_hight

        pygame.init()
        self.screen = pygame.display.set_mode((self.screen_widht, self.screen_hight))
        pygame.display.set_caption("Robot Arm Simulation")

    def draw_robot_arm(self, x0, y0, x1, y1, x2, y2, current_dist):
        self.screen.fill((255, 255, 255))

        pygame.draw.line(self.screen, (0, 0, 255), (x0, y0), (x1, y1), 3)  # First link
        pygame.draw.line(self.screen, (255, 0, 0), (x1, y1), (x2, y2), 3)  # Second link
        pygame.draw.line(self.screen, (0, 255, 0), (0, 0), (10 * current_dist, -10), 3)  # Distance
        pygame.draw.circle(self.screen, (0, 0, 0), (x0, y0), 5)  # Base

        pygame.display.flip()

    def simulate(self):
        """
        Simulates robot arm until the user quits the application.
        """

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            # gets all info from webcamera feed
            stuff = self.tracker.getPalmCoords()

            # takes palm coords and calculates real coord with them
            scaled_coords = stuff[0]
            coords = self.tracker.getReal(scaled_coords[0], scaled_coords[1], self.max_x, self.max_y)

            # calcs distance between fingers compare to len of index finger
            dist = stuff[1]
            max_dist = dist[1] * 2
            current_dist = (dist[0] / max_dist) - 0.1
            if current_dist < 0:
                current_dist = 0

            # draws plots everything
            if coords:
                theta1, theta2 = self.tracker.calculateAnglesForSim(coords[0], coords[1], self.y0, self.arm_length,
                                                                  self.arm_length)

                x1 = self.x0 + self.arm_length * np.cos(theta1)
                y1 = self.y0 - self.arm_length * np.sin(theta1)

                x2 = x1 + self.arm_length * np.cos(theta1 + theta2)
                y2 = y1 - self.arm_length * np.sin(theta1 + theta2)

                self.draw_robot_arm(self.x0, self.y0, x1, y1, x2, y2, current_dist)

if __name__ == "__main__":
    robot_arm = RobotArmSimulation()
    robot_arm.simulate()
