import pygame
from src.player import Player
from src.enemy import Enemy
from src.asteroid import Asteroid
from src.bullet import Bullet
from src.bee import Bee
from src.fireball import Fireball
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
    for i in range(jugador.max_balas):
        color = (0, 255, 0) if i < jugador.balas_disponibles else (255, 0, 0)
        pygame.draw.circle(VENTANA, color, (760 + i * 15, 40), 5)

    if jugador.balas_disponibles == 0:
        tiempo_pasado = pygame.time.get_ticks() - jugador.ultimo_disparo
        ancho_barra = min(int((tiempo_pasado / jugador.tiempo_recarga) * 45), 45)
        pygame.draw.rect(VENTANA, (255, 255, 0), (750, 55, ancho_barra, 10))


def mostrar_tiempo_restante(tiempo_restante):
    fuente = pygame.font.Font(None, 36)
    color = VERDE if tiempo_restante <= 0 else BLANCO
    texto_tiempo = fuente.render(f"Tiempo restante: {max(tiempo_restante, 0)}s", True, color)
    VENTANA.blit(texto_tiempo, (ANCHO // 2 - texto_tiempo.get_width() // 2, ALTO - 40))


def mostrar_transicion_nivel():
    next_level_sound.play()
    pygame.mixer.music.pause()
    VENTANA.fill(NEGRO)
    fuente = pygame.font.Font(None, 50)
    texto_transicion = fuente.render("¡Nivel Completado!", True, VERDE)
    VENTANA.blit(texto_transicion, (ANCHO // 2 - texto_transicion.get_width() // 2, ALTO // 2))
    pygame.display.flip()
    pygame.time.delay(2000)
    pygame.mixer.music.unpause()


def mostrar_transicion(nivel, requisitos):
    pygame.mixer.music.pause()
    intro_music.play()
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
    pygame.time.delay(4000)
    pygame.mixer.music.unpause()


def game_over_screen():
    pygame.mixer.music.stop()
    if sonido_game_over:
        sonido_game_over.play()

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
                    pygame.mixer.music.play(loops=-1)
                    return True
                elif evento.key == pygame.K_ESCAPE:
                    pygame.quit()
                    return False


def game_loop():
    global puntaje
    jugador = Player(ANCHO // 2, ALTO - 50)
    enemigos = []
    asteroides = []
    abejas = []
    bolas_fuego = []
    balas = []

    nivel = 1
    jugador_vivo = True
    corriendo = True
    tiempo_inicio_nivel = pygame.time.get_ticks()
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
            level_complete_sound.play()
            enemigos.clear()
            asteroides.clear()
            abejas.clear()
            bolas_fuego.clear()
            mostrar_transicion_nivel()
            nivel += 1
            jugador.balas_disponibles = jugador.max_balas
            tiempo_inicio_nivel = pygame.time.get_ticks()
            mostrar_transicion(nivel, niveles.get(nivel, {"tiempo": 180, "puntos": None}))
            nivel_completado = False
            continue

        if nivel <= 3:
            probabilidad_enemigo = 0.02
            probabilidad_asteroide = 0.03
            velocidad_enemigo = random.randint(1, 3)
            velocidad_asteroide = random.randint(2, 4)
        elif nivel <= 7:
            probabilidad_enemigo = 0.04
            probabilidad_asteroide = 0.05
            velocidad_enemigo = random.randint(2, 4)
            velocidad_asteroide = random.randint(3, 5)
        else:
            probabilidad_enemigo = 0.08
            probabilidad_asteroide = 0.1
            velocidad_enemigo = random.randint(3, 6)
            velocidad_asteroide = random.randint(4, 7)

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

        if random.random() < probabilidad_enemigo:
            enemigo = Enemy()
            enemigo.speed = velocidad_enemigo
            enemigos.append(enemigo)
        if random.random() < probabilidad_asteroide:
            asteroide = Asteroid()
            asteroide.speed = velocidad_asteroide
            asteroides.append(asteroide)
        if nivel >= 4 and random.random() < 0.02:
            abeja = Bee()
            abejas.append(abeja)
        if nivel >= 7 and random.random() < 0.01:
            fireball = Fireball()
            bolas_fuego.append(fireball)

        # Lista temporal para almacenar balas que deben ser eliminadas
        balas_a_eliminar = []

        for bala in balas:
            bala.mover()
            bala.dibujar(VENTANA)
            for enemigo in enemigos[:]:
                if pygame.sprite.collide_mask(bala, enemigo):
                    enemigos.remove(enemigo)
                    puntaje += 10
                    if sonido_explosion:
                        sonido_explosion.play()
                    balas_a_eliminar.append(bala)  # Marcar bala para eliminar
                    break
            for asteroide in asteroides[:]:
                if pygame.sprite.collide_mask(bala, asteroide):
                    asteroides.remove(asteroide)
                    puntaje += 10
                    if sonido_explosion:
                        sonido_explosion.play()
                    balas_a_eliminar.append(bala)
                    break
            for abeja in abejas[:]:
                if pygame.sprite.collide_mask(bala, abeja):
                    if abeja.recibir_dano():
                        abejas.remove(abeja)
                        puntaje += 30
                    balas_a_eliminar.append(bala)
                    break
            for fireball in bolas_fuego[:]:
                if pygame.sprite.collide_mask(bala, fireball):
                    bolas_fuego.remove(fireball)
                    puntaje += 50
                    balas_a_eliminar.append(bala)
                    break
            if bala.rect.bottom < 0:
                balas_a_eliminar.append(bala)

        # Eliminar las balas marcadas al final del ciclo
        for bala in balas_a_eliminar:
            if bala in balas:  # Verificar que la bala aún esté en la lista
                balas.remove(bala)

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

        for abeja in abejas[:]:
            abeja.mover()
            abeja.dibujar(VENTANA)
            if jugador_vivo and pygame.sprite.collide_mask(jugador, abeja):
                jugador_vivo = False

        for fireball in bolas_fuego[:]:
            fireball.mover()
            fireball.dibujar(VENTANA)
            if jugador_vivo and pygame.sprite.collide_mask(jugador, fireball):
                jugador_vivo = False

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
