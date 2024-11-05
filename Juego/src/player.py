import pygame
from src.bullet import Bullet
from src.utils import cargar_imagen, cargar_sonido, crear_mascara
import time


class Player:
    def __init__(self, x, y):
        self.image = cargar_imagen("player_ship.png")
        self.rect = self.image.get_rect(center=(x, y))
        self.mask = crear_mascara(self.image)  # Máscara de colisión
        self.speed = 5
        self.sonido_disparo = cargar_sonido("shoot.wav")

        # Balas
        self.max_balas = 3
        self.balas_disponibles = self.max_balas
        self.ultimo_disparo = 0
        self.tiempo_recarga = 1200  # 1.2 segundos para recargar completamente

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
        # Verificar si hay balas disponibles
        if self.balas_disponibles > 0:
            if self.sonido_disparo:
                self.sonido_disparo.play()
            self.balas_disponibles -= 1
            self.ultimo_disparo = pygame.time.get_ticks()  # Marca el tiempo del disparo
            return Bullet(self.rect.centerx, self.rect.top, -1)
        return None

    def recargar(self):
        # Si no tiene balas, verificar si ha pasado el tiempo de recarga
        tiempo_actual = pygame.time.get_ticks()
        if self.balas_disponibles == 0 and tiempo_actual - self.ultimo_disparo >= self.tiempo_recarga:
            self.balas_disponibles = self.max_balas  # Recarga completa

    def dibujar(self, ventana):
        ventana.blit(self.image, self.rect)

    def mostrar_balas(self, ventana):
        # Representación visual de balas
        for i in range(self.max_balas):
            color = (0, 255, 0) if i < self.balas_disponibles else (255, 0, 0)
            pygame.draw.circle(ventana, color, (760 + i * 15, 40), 5)  # Círculos para representar balas
