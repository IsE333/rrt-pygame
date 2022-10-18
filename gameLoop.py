from collections import namedtuple
import json
import pygame
from border import Border
from RRT import RRT


class GameLoop:
    def __init__(self) -> None:
        pygame.init()
        self.cw, self.ch = (
            pygame.display.Info().current_w,
            pygame.display.Info().current_h,
        )
        self.screen = pygame.display.set_mode((self.cw, self.ch), pygame.FULLSCREEN)
        self.lines = []
        self.deletedLines = []
        self.drawingLine = False
        self.running = True
        self.point_list = []
        self.rrt = RRT(self)
        # self.load()

    def loop(self):
        pygame.display.set_caption("Game")
        FPS = 200
        fpsClock = pygame.time.Clock()
        self.rrt_end = False

        self.clickRD = False
        while self.running:
            self.clickLU = False
            self.clickLD = False

            self.screen.fill((0, 0, 0))
            # self.draw()
            self.update()
            self.takeInput()
            pygame.display.update()
            pygame.display.flip()
            fpsClock.tick(FPS)

    def update(self):
        if not self.rrt_end:
            self.rrt.tick()
            self.draw()
            return
        self.draw()
        self.draw_path()

    def draw(self):

        pygame.draw.rect(self.screen, (0, 0, 255), (0, 0, 1200, 900))
        pygame.draw.rect(self.screen, (0, 0, 0), (5, 5, 1190, 890))
        for point in self.point_list:
            for child in point.children:
                pygame.draw.line(
                    self.screen,
                    (255, 255, 255),
                    (point.x, point.y),
                    (child.x, child.y),
                )

    def draw_path(self):
        point = self.rrt.end
        while point.parent is not None:
            pygame.draw.line(
                self.screen,
                (255, 0, 0),
                (point.x, point.y),
                (point.parent.x, point.parent.y),
            )
            point = point.parent

    def takeInput(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    self.clickLD = True
                if event.button == 3:
                    self.clickRD = True
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    self.clickLU = True
                if event.button == 3:
                    self.clickRD = False  # this is an expection, it will be false here, it will not be false in next frame unlike others
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
