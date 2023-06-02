import math
import random
import matplotlib.pyplot as plt


class Polygon:
    def __init__(self, graph, points, size, color):
        self.graph = graph
        self.points = points
        self.size = size
        self.color = color
        self.finished = False
        self.lines = []


    def finish_polygon(self):
        self.finished = True

        self.lines.append(self.graph.draw_line(
                self.points[-1], self.points[0], self.color, self.size))

    def draw_lines(self):
        self.earse(self.finished)

        for p in range(len(self.points)-1):
            self.lines.append(self.graph.draw_line(
                self.points[p], self.points[p+1], self.color, self.size))

    def move(self, x, y):
        for p in range(len(self.points)):
            self.points[p][0] += x
            self.points[p][1] += y

        self.draw_lines()
        if self.finished:
            self.finish_polygon()

    def add_point(self, x,y):
        if len(self.points) > 0:
            self.lines.append(self.graph.draw_line(self.points[-1], (x,y), self.color, self.size))
        self.points.append([x,y])

    def add_points(self, points):
        self.points.clear()
        for x, y in points:
            self.add_point(x,y)
        self.finish_polygon()

    def earse(self, finished):
        for figure in self.lines:
            self.graph.delete_figure(figure)
        self.lines.clear()
        self.finished = finished

    def delete_figure(self, index):
        self.graph.delete_figure(self.lines[index])
        self.lines.pop(index)
        self.points.pop(index)

