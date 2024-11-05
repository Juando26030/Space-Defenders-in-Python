import pygame
import random
from src.utils import cargar_imagen, crear_mascara

class Bee:
    def __init__(self):
        self.image = cargar_imagen("bee.png")
        self.rect = self.image.get_rect(center=(random.randint(50, 750), -50))
        self.mask = crear_mascara(self.image)
        self.speed = random.randint(2, 4)
        self.health = 2  # Necesita dos disparos para morir

    def mover(self):
        self.rect.y += self.speed

    def recibir_dano(self):
        """Reduce la vida de la Bee. Retorna True si está destruida."""
        self.health -= 1
        return self.health <= 0

    def dibujar(self, ventana):
        ventana.blit(self.image, self.rect)
