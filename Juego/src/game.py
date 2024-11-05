import pygame
from src.player import Player
from src.enemy import Enemy
from src.asteroid import Asteroid
from src.bullet import Bullet
from src.utils import cargar_sonido
import random

# Inicializamos Pygame y sonidos
pygame.init()
pygame.font.init()
pygame.mixer.init()

# Configuraciones iniciales
ANCHO, ALTO = 800, 600
VENTANA = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Space Defender")

# Colores
NEGRO = (0, 0, 0)
BLANCO = (255, 255, 255)
VERDE = (0, 255, 0)

# Variables de juego
FPS = 60
clock = pygame.time.Clock()
puntaje = 0

# Requisitos de nivel: tiempo en segundos y puntos requeridos
niveles = {
    1: {"tiempo": 30, "puntos": None},
    2: {"tiempo": 60, "puntos": None},
    3: {"tiempo": 90, "puntos": None},
    4: {"tiempo": 120, "puntos": None},
    5: {"tiempo": 150, "puntos": None},
    6: {"tiempo": 180, "puntos": 1000},
    7: {"tiempo": 195, "puntos": 1200},
    8: {"tiempo": 205, "puntos": 1400},
    9: {"tiempo": 225, "puntos": 1600},
    10: {"tiempo": 240, "puntos": 1800}
}

# Sonidos
sonido_explosion = cargar_sonido("explosion.wav")
sonido_game_over = cargar_sonido("game_over.wav")
intro_music = cargar_sonido("intro_music.wav")
next_level_sound = cargar_sonido("next_level.wav")
level_complete_sound = cargar_sonido("level_complete.wav")

# Cargar y reproducir la música de fondo usando mixer.music para poder pausar
pygame.mixer.music.load("../assets/sounds/back_music.wav")
pygame.mixer.music.set_volume(0.3)
pygame.mixer.music.play(loops=-1)


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
                return False
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_RETURN:
                    esperar = False
    return True


def mostrar_marcador(puntaje, nivel):
    fuente = pygame.font.Font(None, 36)
    texto = fuente.render(f"Nivel: {nivel}  Puntaje: {puntaje}", True, BLANCO)
    VENTANA.blit(texto, (ANCHO - texto.get_width() - 120, 20))


def mostrar_balas(jugador):
    """Muestra el estado de las balas en la esquina superior derecha."""
    for i in range(jugador.max_balas):
        color = (0, 255, 0) if i < jugador.balas_disponibles else (255, 0, 0)
        pygame.draw.circle(VENTANA, color, (760 + i * 15, 40), 5)

    # Indicador de recarga (barra que crece)
    if jugador.balas_disponibles == 0:
        tiempo_pasado = pygame.time.get_ticks() - jugador.ultimo_disparo
        ancho_barra = min(int((tiempo_pasado / jugador.tiempo_recarga) * 45), 45)
        pygame.draw.rect(VENTANA, (255, 255, 0), (750, 55, ancho_barra, 10))


def mostrar_tiempo_restante(tiempo_restante):
    """Muestra el temporizador en la parte inferior central de la pantalla."""
    fuente = pygame.font.Font(None, 36)
    color = VERDE if tiempo_restante <= 0 else BLANCO
    texto_tiempo = fuente.render(f"Tiempo restante: {max(tiempo_restante, 0)}s", True, color)
    VENTANA.blit(texto_tiempo, (ANCHO // 2 - texto_tiempo.get_width() // 2, ALTO - 40))


def mostrar_transicion_nivel():
    """Reproduce sonido de transición al pasar al siguiente nivel."""
    next_level_sound.play()  # Sonido del siguiente nivel
    pygame.mixer.music.pause()  # Pausar música de fondo

    # Mostramos el número de nivel y condiciones
    VENTANA.fill(NEGRO)
    fuente = pygame.font.Font(None, 50)
    texto_transicion = fuente.render("¡Nivel Completado!", True, VERDE)
    VENTANA.blit(texto_transicion, (ANCHO // 2 - texto_transicion.get_width() // 2, ALTO // 2))
    pygame.display.flip()
    pygame.time.delay(2000)  # Pausa para transición de 2 segundos

    pygame.mixer.music.unpause()  # Reanudar música de fondo


def mostrar_transicion(nivel, requisitos):
    """Pantalla de transición inicial de nivel, con la música de introducción."""
    pygame.mixer.music.pause()  # Pausar la música de fondo
    intro_music.play()  # Reproducir música de introducción al inicio del nivel

    VENTANA.fill(NEGRO)
    fuente = pygame.font.Font(None, 50)
    texto_nivel = fuente.render(f"Nivel {nivel}", True, BLANCO)
    texto_condiciones = fuente.render(
        f"Objetivo: {requisitos['tiempo']}s o {requisitos['puntos']} puntos" if requisitos["puntos"]
        else f"Sobrevive {requisitos['tiempo']}s", True, BLANCO
    )

    VENTANA.blit(texto_nivel, (ANCHO // 2 - texto_nivel.get_width() // 2, ALTO // 2 - 50))
    VENTANA.blit(texto_condiciones, (ANCHO // 2 - texto_condiciones.get_width() // 2, ALTO // 2 + 10))
    pygame.display.flip()
    pygame.time.delay(4000)  # Pausa de 4 segundos para transición

    pygame.mixer.music.unpause()  # Reanudar música de fondo


def game_over_screen():
    pygame.mixer.music.stop()  # Detenemos la música de fondo
    if sonido_game_over:
        sonido_game_over.play()  # Sonido de game over

    VENTANA.fill(NEGRO)
    fuente = pygame.font.Font(None, 50)
    texto = fuente.render("Game Over", True, BLANCO)
    retry_text = fuente.render("Presiona R para reiniciar", True, BLANCO)
    exit_text = fuente.render("Presiona ESC para salir", True, BLANCO)

    VENTANA.blit(texto, (ANCHO // 2 - texto.get_width() // 2, ALTO // 2 - 50))
    VENTANA.blit(retry_text, (ANCHO // 2 - retry_text.get_width() // 2, ALTO // 2 + 10))
    VENTANA.blit(exit_text, (ANCHO // 2 - exit_text.get_width() // 2, ALTO // 2 + 60))
    pygame.display.flip()

    esperar = True
    while esperar:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                return False
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_r:
                    pygame.mixer.music.play(loops=-1)  # Reiniciar música de fondo
                    return True
                elif evento.key == pygame.K_ESCAPE:
                    pygame.quit()
                    return False


def game_loop():
    global puntaje
    jugador = Player(ANCHO // 2, ALTO - 50)
    enemigos = []
    asteroides = []
    balas = []

    nivel = 1
    jugador_vivo = True
    corriendo = True
    tiempo_inicio_nivel = pygame.time.get_ticks()  # Tiempo de inicio del nivel
    nivel_completado = False

    mostrar_transicion(nivel, niveles[nivel])

    while corriendo:
        clock.tick(FPS)
        VENTANA.fill(NEGRO)
        teclas = pygame.key.get_pressed()

        tiempo_actual = pygame.time.get_ticks()
        tiempo_supervivencia = (tiempo_actual - tiempo_inicio_nivel) // 1000

        requisitos = niveles.get(nivel, {"tiempo": 180, "puntos": puntaje + 200})
        tiempo_objetivo = requisitos["tiempo"]
        puntos_objetivo = requisitos.get("puntos")
        tiempo_restante = tiempo_objetivo - tiempo_supervivencia

        if tiempo_restante <= 0 and not nivel_completado:
            nivel_completado = True
            level_complete_sound.play()  # Reproducir sonido de nivel completado
            enemigos.clear()
            asteroides.clear()
            mostrar_transicion_nivel()
            nivel += 1
            tiempo_inicio_nivel = pygame.time.get_ticks()
            mostrar_transicion(nivel, niveles.get(nivel, {"tiempo": 180, "puntos": None}))
            nivel_completado = False
            continue

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                corriendo = False
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_SPACE and jugador_vivo:
                    nueva_bala = jugador.shoot()
                    if nueva_bala:
                        balas.append(nueva_bala)

        jugador.recargar()
        if jugador_vivo:
            jugador.mover(teclas)
            jugador.dibujar(VENTANA)

        if random.randint(0, 30) == 0:
            enemigos.append(Enemy())
        if random.randint(0, 50) == 0:
            asteroides.append(Asteroid())

        for enemigo in enemigos[:]:
            enemigo.mover()
            enemigo.dibujar(VENTANA)
            if jugador_vivo and pygame.sprite.collide_mask(jugador, enemigo):
                jugador_vivo = False

        for asteroide in asteroides[:]:
            asteroide.mover()
            asteroide.dibujar(VENTANA)
            if jugador_vivo and pygame.sprite.collide_mask(jugador, asteroide):
                jugador_vivo = False

        for bala in balas[:]:
            bala.mover()
            bala.dibujar(VENTANA)
            for enemigo in enemigos[:]:
                if pygame.sprite.collide_mask(bala, enemigo):
                    enemigos.remove(enemigo)
                    balas.remove(bala)
                    puntaje += 10
                    if sonido_explosion:
                        sonido_explosion.play()
                    break
            for asteroide in asteroides[:]:
                if pygame.sprite.collide_mask(bala, asteroide):
                    asteroides.remove(asteroide)
                    balas.remove(bala)
                    puntaje += 10
                    if sonido_explosion:
                        sonido_explosion.play()
                    break
            if bala.rect.bottom < 0:
                balas.remove(bala)

        if not jugador_vivo:
            if game_over_screen():
                puntaje = 0
                return game_loop()
            else:
                corriendo = False

        mostrar_marcador(puntaje, nivel)
        mostrar_balas(jugador)
        mostrar_tiempo_restante(tiempo_restante)
        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    if main_menu():
        game_loop()
