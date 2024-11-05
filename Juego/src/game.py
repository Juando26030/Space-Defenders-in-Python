import pygame
from src.player import Player
from src.enemy import Enemy
from src.asteroid import Asteroid
from src.bullet import Bullet
from src.utils import cargar_imagen

# Inicializamos Pygame
pygame.init()

# Configuraciones iniciales
ANCHO, ALTO = 800, 600
VENTANA = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Space Defender")

# Colores
NEGRO = (0, 0, 0)
BLANCO = (255, 255, 255)

# Variables de juego
FPS = 60
clock = pygame.time.Clock()

def main_menu():
    """Función para mostrar el menú principal"""
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
                return False
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_RETURN:
                    esperar = False
    return True

def game_loop():
    """Bucle principal del juego"""
    jugador = Player(ANCHO // 2, ALTO - 50)
    enemigos = []
    asteroides = []
    balas = []

    corriendo = True
    while corriendo:
        clock.tick(FPS)
        VENTANA.fill(NEGRO)
        teclas = pygame.key.get_pressed()

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                corriendo = False
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_SPACE:
                    balas.append(jugador.shoot())

        # Movimiento y actualización del jugador
        jugador.mover(teclas)
        jugador.dibujar(VENTANA)

        # Actualizar enemigos y asteroides
        if len(enemigos) < 5:  # Aparece un nuevo enemigo cada cierto tiempo
            enemigos.append(Enemy())
        if len(asteroides) < 3:  # Aparece un asteroide cada cierto tiempo
            asteroides.append(Asteroid())

        for enemigo in enemigos:
            enemigo.mover()
            enemigo.dibujar(VENTANA)

        for asteroide in asteroides:
            asteroide.mover()
            asteroide.dibujar(VENTANA)

        # Actualizar balas
        for bala in balas:
            bala.mover()
            bala.dibujar(VENTANA)

        # Actualizar pantalla
        pygame.display.flip()

    pygame.quit()

# Inicia el juego
if __name__ == "__main__":
    if main_menu():
        game_loop()
