import pygame
import os

def cargar_imagen(nombre_archivo):
    ruta = os.path.join("../assets", "images", nombre_archivo)
    try:
        imagen = pygame.image.load(ruta)
        return imagen
    except pygame.error as e:
        print(f"Error cargando la imagen {nombre_archivo}: {e}")
        return None

def cargar_sonido(nombre_archivo):
    ruta = os.path.join("../assets", "sounds", nombre_archivo)
    try:
        sonido = pygame.mixer.Sound(ruta)
        return sonido
    except pygame.error as e:
        print(f"Error cargando el sonido {nombre_archivo}: {e}")
        return None

def crear_mascara(imagen):
    """Crea una máscara para la imagen basada en la transparencia."""
    return pygame.mask.from_surface(imagen)
