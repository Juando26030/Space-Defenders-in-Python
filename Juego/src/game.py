import sys

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
AMARILLO = (255, 255, 0)

# Variables de juego
FPS = 60
clock = pygame.time.Clock()
puntaje = 0

# Requisitos de nivel: tiempo en segundos y conteo de enemigos a destruir
niveles = {
    1: {"tiempo": 20, "enemigos": 10, "abejas": 0, "bolas_fuego": 0},
    2: {"tiempo": 45, "enemigos": 45, "abejas": 0, "bolas_fuego": 0},
    3: {"tiempo": 60, "enemigos": 70, "abejas": 0, "bolas_fuego": 0},
    4: {"tiempo": 80, "enemigos": 85, "abejas": 5, "bolas_fuego": 0},
    5: {"tiempo": 100, "enemigos": 100, "abejas": 15, "bolas_fuego": 0},
    6: {"tiempo": 120, "enemigos": 120, "abejas": 30, "bolas_fuego": 0},
    7: {"tiempo": 140, "enemigos": 145, "abejas": 45, "bolas_fuego": 5},
    8: {"tiempo": 165, "enemigos": 170, "abejas": 60, "bolas_fuego": 15},
    9: {"tiempo": 180, "enemigos": 200, "abejas": 75, "bolas_fuego": 30},
    10: {"tiempo": 200, "enemigos": 250, "abejas": 100, "bolas_fuego": 50}
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

    opciones = [
        "1. Modo Historia",
        "2. Modo Infinito",
        "3. Ver mis Puntajes",
        "4. Salir"
    ]

    for i, opcion in enumerate(opciones):
        texto = fuente.render(opcion, True, BLANCO)
        VENTANA.blit(texto, (ANCHO // 2 - texto.get_width() // 2, ALTO // 2 - 100 + i * 60))

    pygame.display.flip()

    esperar = True
    while esperar:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_1:
                    return "historia"
                elif evento.key == pygame.K_2:
                    return "infinito"
                elif evento.key == pygame.K_3:
                    return "puntajes"
                elif evento.key == pygame.K_4:
                    pygame.quit()
                    sys.exit()
            elif evento.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                for i in range(len(opciones)):
                    texto_rect = pygame.Rect(
                        ANCHO // 2 - 100, ALTO // 2 - 100 + i * 60, 200, 50
                    )
                    if texto_rect.collidepoint(x, y):
                        return ["historia", "infinito", "puntajes", "salir"][i]


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
    condiciones = [
        f"Cumple:",
        f"- Sobrevive {requisitos['tiempo']} segundos",
        f"- Eliminar {requisitos['enemigos']} enemigos comunes"
    ]
    if requisitos["abejas"] > 0:
        condiciones.append(f"- Eliminar {requisitos['abejas']} abejas")
    if requisitos["bolas_fuego"] > 0:
        condiciones.append(f"- Eliminar {requisitos['bolas_fuego']} bolas de fuego")

    for i, condicion in enumerate(condiciones):
        texto_condicion = fuente.render(condicion, True, BLANCO)
        VENTANA.blit(texto_condicion, (ANCHO // 2 - texto_condicion.get_width() // 2, ALTO // 2 - 50 + i * 30))

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


def mostrar_contador(enemigos_destruidos, abejas_destruidas, bolas_fuego_destruidas, requisitos):
    fuente = pygame.font.Font(None, 36)

    # Mostrar solo los contadores necesarios para el nivel actual
    texto_enemigos = fuente.render(
        f"Enemigos comunes: {enemigos_destruidos}/{requisitos['enemigos']}", True, AMARILLO
    )
    VENTANA.blit(texto_enemigos, (10, 10))

    if requisitos["abejas"] > 0:
        texto_abejas = fuente.render(
            f"Abejas: {abejas_destruidas}/{requisitos['abejas']}", True, AMARILLO
        )
        VENTANA.blit(texto_abejas, (10, 40))

    if requisitos["bolas_fuego"] > 0:
        texto_bolas_fuego = fuente.render(
            f"Bolas de Fuego: {bolas_fuego_destruidas}/{requisitos['bolas_fuego']}", True, AMARILLO
        )
        VENTANA.blit(texto_bolas_fuego, (10, 70))


def game_loop(nivel_inicial=1):
    global puntaje
    jugador = Player(ANCHO // 2, ALTO - 50)
    enemigos = []
    asteroides = []
    abejas = []
    bolas_fuego = []
    balas = []

    nivel = nivel_inicial
    jugador_vivo = True
    corriendo = True
    nivel_completado = False

    # Contadores de enemigos destruidos
    enemigos_destruidos = 0
    abejas_destruidas = 0
    bolas_fuego_destruidas = 0

    while corriendo:
        mostrar_transicion(nivel, niveles[nivel])
        tiempo_inicio_nivel = pygame.time.get_ticks()  # Empezar el contador de tiempo después de la transición

        while not nivel_completado and corriendo:
            clock.tick(FPS)
            VENTANA.fill(NEGRO)
            teclas = pygame.key.get_pressed()

            tiempo_actual = pygame.time.get_ticks()
            tiempo_supervivencia = (tiempo_actual - tiempo_inicio_nivel) // 1000

            requisitos = niveles.get(nivel, {"tiempo": 180, "enemigos": puntaje + 200})
            tiempo_objetivo = requisitos["tiempo"]
            enemigos_objetivo = requisitos["enemigos"]
            abejas_objetivo = requisitos["abejas"]
            bolas_fuego_objetivo = requisitos["bolas_fuego"]
            tiempo_restante = tiempo_objetivo - tiempo_supervivencia

            # Comprobar si el nivel está completo
            if tiempo_restante <= 0 and (
                    enemigos_destruidos >= enemigos_objetivo and
                    abejas_destruidas >= abejas_objetivo and
                    bolas_fuego_destruidas >= bolas_fuego_objetivo
            ):
                nivel_completado = True
                level_complete_sound.play()
                enemigos.clear()
                asteroides.clear()
                abejas.clear()
                bolas_fuego.clear()
                mostrar_transicion_nivel()
                nivel += 1
                tiempo_inicio_nivel = pygame.time.get_ticks()
                enemigos_destruidos = 0
                abejas_destruidas = 0
                bolas_fuego_destruidas = 0
                nivel_completado = False
                break

            # Dificultad escalada
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

            # Manejo de eventos de entrada
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    corriendo = False
                if evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_SPACE and jugador_vivo:
                        nueva_bala = jugador.shoot()
                        if nueva_bala:
                            balas.append(nueva_bala)

            # Recargar balas del jugador
            jugador.recargar()
            if jugador_vivo:
                jugador.mover(teclas)
                jugador.dibujar(VENTANA)

            # Generar enemigos y obstáculos según las probabilidades
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

            # Procesar movimiento de balas y colisiones
            balas_a_eliminar = []
            for bala in balas:
                bala.mover()
                bala.dibujar(VENTANA)
                for enemigo in enemigos[:]:
                    if pygame.sprite.collide_mask(bala, enemigo):
                        enemigos.remove(enemigo)
                        enemigos_destruidos += 1
                        puntaje += 10
                        if sonido_explosion:
                            sonido_explosion.play()
                        balas_a_eliminar.append(bala)
                        break
                for asteroide in asteroides[:]:
                    if pygame.sprite.collide_mask(bala, asteroide):
                        asteroides.remove(asteroide)
                        enemigos_destruidos += 1
                        puntaje += 10
                        if sonido_explosion:
                            sonido_explosion.play()
                        balas_a_eliminar.append(bala)
                        break
                for abeja in abejas[:]:
                    if pygame.sprite.collide_mask(bala, abeja):
                        if abeja.recibir_dano():
                            abejas.remove(abeja)
                            abejas_destruidas += 1
                            puntaje += 30
                        balas_a_eliminar.append(bala)
                        break
                for fireball in bolas_fuego[:]:
                    if pygame.sprite.collide_mask(bala, fireball):
                        bolas_fuego.remove(fireball)
                        bolas_fuego_destruidas += 1
                        puntaje += 50
                        balas_a_eliminar.append(bala)
                        break
                if bala.rect.bottom < 0:
                    balas_a_eliminar.append(bala)

            # Eliminar balas fuera de pantalla o que colisionaron
            for bala in balas_a_eliminar:
                if bala in balas:
                    balas.remove(bala)

            # Procesar movimiento de enemigos y colisiones con el jugador
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

            # Manejo de pantalla de Game Over
            if not jugador_vivo:
                if game_over_screen():
                    puntaje = 0
                    return game_loop()
                else:
                    corriendo = False

            # Mostrar elementos de interfaz
            mostrar_marcador(puntaje, nivel)
            mostrar_balas(jugador)
            mostrar_tiempo_restante(tiempo_restante)
            mostrar_contador(enemigos_destruidos, abejas_destruidas, bolas_fuego_destruidas, requisitos)
            pygame.display.flip()

    pygame.quit()



if __name__ == "__main__":
    modo_seleccionado = main_menu()
    if modo_seleccionado == "historia":
        game_loop()
    elif modo_seleccionado == "infinito":
        # Implementación del modo infinito
        print("Modo Infinito: Implementar lógica.")
    elif modo_seleccionado == "puntajes":
        # Implementación para ver los puntajes
        print("Ver mis Puntajes: Implementar lógica.")