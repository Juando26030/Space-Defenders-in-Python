import pygame
from src.utils import cargar_imagen

class Bullet:
    def __init__(self, x, y, direction):
        self.image = cargar_imagen("bullet.png")
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = 10 * direction

    def mover(self):
        self.rect.y += self.speed

    def dibujar(self, ventana):
        ventana.blit(self.image, self.rect)
