import pygame
import random
from src.utils import cargar_imagen, crear_mascara

class Fireball:
    def __init__(self):
        self.image = cargar_imagen("fireball.png")
        self.rect = self.image.get_rect(center=(random.randint(50, 750), random.randint(50, 550)))
        self.mask = crear_mascara(self.image)
        self.speed = random.randint(3, 6)
        self.direction = random.choice([-1, 1])  # Movimiento horizontal

    def mover(self):
        self.rect.x += self.speed * self.direction
        # Cambiar de dirección si alcanza los bordes
        if self.rect.left <= 0 or self.rect.right >= 800:
            self.direction *= -1

    def dibujar(self, ventana):
        ventana.blit(self.image, self.rect)
