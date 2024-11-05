import pygame
import random
from src.utils import cargar_imagen, crear_mascara

class Enemy:
    def __init__(self):
        self.image = cargar_imagen("enemy_ship.png")
        self.rect = self.image.get_rect(center=(random.randint(50, 750), -50))
        self.mask = crear_mascara(self.image)  # Máscara de colisión
        self.speed = random.randint(1, 3)

    def mover(self):
        self.rect.y += self.speed

    def dibujar(self, ventana):
        ventana.blit(self.image, self.rect)
