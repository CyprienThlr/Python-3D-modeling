import pygame as pg
from matrix_functions import *  

class Object3D:
    def __init__(self, render):
        self.render = render
        self.vertexes = np.array([(0, 0, 0, 1), (0, 1, 0, 1), (1, 1, 0, 1), (1, 0, 0, 1),
                                  (0, 0, 1, 1), (0, 1, 1, 1), (1, 1, 1, 1), (1, 0, 1, 1)])

        self.faces = np.array([(0, 1, 2, 3), (4, 5, 6, 7), (0, 4, 5, 1), (2, 3, 7, 6), (1, 2, 6, 5), (0, 3, 7, 4)]) 

    def draw(self):
        self.screen_projection()

    def screen_projection(self):
        # Appliquer la matrice de caméra
        vertexes = self.vertexes @ self.render.camera.camera_matrix()
        print(f"Vertexes after camera matrix: {vertexes}")

        # Appliquer la matrice de projection
        vertexes = vertexes @ self.render.projection.projection_matrix
        print(f"Vertexes after projection matrix: {vertexes}")

        # Éviter les divisions par zéro
        w = vertexes[:, -1].reshape(-1, 1)
        w[w == 0] = 1  # Remplace les zéros par 1 pour éviter les divisions par zéro
        vertexes /= w
        print(f"Vertexes after division by w: {vertexes}")

        # Clipping : mettre les coordonnées hors écran à zéro
        vertexes[(vertexes > 1) | (vertexes < -1)] = 0
        print(f"Vertexes after clipping: {vertexes}")

        # Appliquer la transformation à l'écran
        vertexes = vertexes @ self.render.projection.to_screen_matrix
        vertexes = vertexes[:, :2]
        print(f"Vertexes after screen projection: {vertexes}")

        # Dessiner les faces
        for face in self.faces:
            polygon = vertexes[face]
            if not np.any((polygon == self.render.H_WIDTH) | (polygon == self.render.H_HEIGHT)):
                pg.draw.polygon(self.render.screen, pg.Color('orange'), polygon, 3)
            else:
                print(f"Polygon out of bounds: {polygon}")

        # Dessiner les vertexes
        for vertex in vertexes:
            if not np.any((vertex == self.render.H_WIDTH) | (vertex == self.render.H_HEIGHT)):
                vertex_int = vertex.astype(int)
                if len(vertex_int) == 2:
                    pg.draw.circle(self.render.screen, pg.Color('white'), vertex_int, 6)
                else:
                    print(f"Vertex out of bounds: {vertex_int}")

    def translate(self, pos):
        self.vertexes = self.vertexes @ translate(pos)
        print(f"Translated Vertexes: {self.vertexes}")

    def scale(self, scale_to):
        self.vertexes = self.vertexes @ scale(scale_to)
        print(f"Scaled Vertexes: {self.vertexes}")

    def rotate_x(self, angle):
        self.vertexes = self.vertexes @ rotate_x(angle)
        print(f"Rotated X Vertexes: {self.vertexes}")

    def rotate_y(self, angle):
        self.vertexes = self.vertexes @ rotate_y(angle)
        print(f"Rotated Y Vertexes: {self.vertexes}")

    def rotate_z(self, angle):
        self.vertexes = self.vertexes @ rotate_z(angle)
        print(f"Rotated Z Vertexes: {self.vertexes}")