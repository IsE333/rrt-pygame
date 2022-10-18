import math

import numpy
from border import Point
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from gameLoop import GameLoop


class RRT:
    def __init__(self, game) -> None:
        self.limit = 40
        self.iter_limit = 1000
        self.start = Point(500, 500, None)
        game.point_list.append(self.start)

        self.end = Point(100, 100, None)
        self.game = game

    def tick(self):
        if len(self.game.point_list) > self.iter_limit:
            self.game.rrt_end = True
            return

        random_point = self.random_point()
        nearest_point = self.get_nearest_point(random_point)

        if self.distance(random_point, nearest_point) > self.limit:
            random_point.x = nearest_point.x + self.limit * (
                random_point.x - nearest_point.x
            ) / self.distance(random_point, nearest_point)
            random_point.y = nearest_point.y + self.limit * (
                random_point.y - nearest_point.y
            ) / self.distance(random_point, nearest_point)
        random_point.parent = nearest_point
        nearest_point.children.append(random_point)
        self.game.point_list.append(random_point)

        if self.is_in_range(random_point, self.end):
            # self.game.rrt_end = True
            print("found")
            self.game.draw_path()
            self.end.parent = random_point
            self.game.rrt_end = True
            return

    def is_in_range(self, p1: Point, p2: Point) -> bool:
        return self.distance(p1, p2) < 20

    def get_nearest_point(self, p: Point) -> Point:
        nearest_point = self.start
        for point in self.game.point_list:
            if self.distance(p, point) < self.distance(p, nearest_point):
                nearest_point = point
        return nearest_point

    def distance(self, p1: Point, p2: Point) -> float:
        return math.sqrt((p1.x - p2.x) ** 2 + (p1.y - p2.y) ** 2)

    def random_point(self) -> Point:
        p = Point(numpy.random.randint(0, 1200), numpy.random.randint(0, 900), None)
        return p
