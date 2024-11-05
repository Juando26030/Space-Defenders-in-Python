import pygame
import random
from src.utils import cargar_imagen

class Asteroid:
    def __init__(self):
        self.image = cargar_imagen("asteroid.png")
        self.rect = self.image.get_rect(center=(random.randint(50, 750), -50))
        self.speed = random.randint(2, 5)

    def mover(self):
        self.rect.y += self.speed

    def dibujar(self, ventana):
        ventana.blit(self.image, self.rect)