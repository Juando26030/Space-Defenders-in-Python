import pygame
import random

# Inicializamos Pygame
pygame.init()

# Configuraciones iniciales
ANCHO, ALTO = 800, 600
VENTANA = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Space Defender")

# Colores
NEGRO = (0, 0, 0)
BLANCO = (255, 255, 255)

# Clase para la nave del jugador
class Player:
    def __init__(self):
        self.image = pygame.image.load("player.png")  # Imagen de la nave del jugador
        self.rect = self.image.get_rect(center=(ANCHO // 2, ALTO - 50))
        self.velocidad = 5

    def mover(self, teclas):
        if teclas[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.velocidad
        if teclas[pygame.K_RIGHT] and self.rect.right < ANCHO:
            self.rect.x += self.velocidad
        if teclas[pygame.K_UP] and self.rect.top > 0:
            self.rect.y -= self.velocidad
        if teclas[pygame.K_DOWN] and self.rect.bottom < ALTO:
            self.rect.y += self.velocidad

    def dibujar(self, ventana):
        ventana.blit(self.image, self.rect)

# Función del menú principal
def main_menu():
    VENTANA.fill(NEGRO)
    fuente = pygame.font.Font(None, 50)
    texto = fuente.render("Presiona ENTER para iniciar", True, BLANCO)
    VENTANA.blit(texto, (ANCHO // 2 - texto.get_width() // 2, ALTO // 2 - texto.get_height() // 2))
    pygame.display.flip()

    esperar = True
    while esperar:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_RETURN:
                    esperar = False

# Bucle principal del juego
def game_loop():
    jugador = Player()
    corriendo = True

    while corriendo:
        VENTANA.fill(NEGRO)
        teclas = pygame.key.get_pressed()

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                corriendo = False

        # Movimiento del jugador
        jugador.mover(teclas)

        # Dibujar jugador
        jugador.dibujar(VENTANA)

        # Actualizamos pantalla
        pygame.display.flip()
        pygame.time.delay(30)

    pygame.quit()

# Ejecutamos el juego
main_menu()
game_loop()
