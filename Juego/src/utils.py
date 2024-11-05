import pygame

def cargar_imagen(nombre_archivo):
    try:
        imagen = pygame.image.load(f"../assets/images/{nombre_archivo}")
        return imagen
    except pygame.error as e:
        print(f"Error cargando la imagen {nombre_archivo}: {e}")
        return None
