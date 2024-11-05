import pygame
from src.bullet import Bullet
from src.utils import cargar_imagen

class Player:
    def __init__(self, x, y):
        self.image = cargar_imagen("player_ship.png")
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = 5

    def mover(self, keys):
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] and self.rect.right < 800:
            self.rect.x += self.speed
        if keys[pygame.K_UP] and self.rect.top > 0:
            self.rect.y -= self.speed
        if keys[pygame.K_DOWN] and self.rect.bottom < 600:
            self.rect.y += self.speed

    def shoot(self):
        # Dispara una bala hacia arriba
        return Bullet(self.rect.centerx, self.rect.top, -1)

    def dibujar(self, ventana):
        ventana.blit(self.image, self.rect)
