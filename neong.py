import pygame
import sys
import time

# --- Inicialización ---
pygame.init()
ANCHO, ALTO = 900, 500
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Neon Platformer")

# --- Configuración ---
clock = pygame.time.Clock()
FPS = 120
fuente = pygame.font.SysFont("consolas", 22)
fuente_grande = pygame.font.SysFont("consolas", 48)

# --- Colores ---
NEON_RED = (255, 50, 50)
NEON_BLUE = (50, 200, 255)
NEON_GREEN = (0, 255, 128)
NEON_PURPLE = (200, 0, 255)
NEON_YELLOW = (255, 255, 100)
FONDO = (0, 0, 0)

# --- Constantes físicas ---
GRAVEDAD = 1250
FUERZA_SALTO = -600
VEL_JUGADOR = 300
VEL_ENEMIGO = 120

# --- Jugador ---
jugador = pygame.Rect(100, 400, 30, 40)
vel_y = 0
en_suelo = False
vel_x = 0

# --- Mundo ---
plataformas = [
    pygame.Rect(0, 460, 900, 40),
    pygame.Rect(200, 380, 120, 10),
    pygame.Rect(400, 300, 120, 10),
    pygame.Rect(650, 340, 150, 10),
    pygame.Rect(0, 0, 10, 500),
    pygame.Rect(890, 0, 10, 500),
]

# --- Enemigos ---
enemigos = [
    pygame.Rect(500, 430, 30, 30),
    pygame.Rect(700, 310, 30, 30)
]
dir_enemigo = [1, -1]

# --- Vida y tiempo ---
vida = 100
ultimo_mov_tiempo = time.time()
ultimo_estatico_tiempo = time.time()
movimiento_activo = False

# --- Funciones auxiliares ---
def dibujar_neon(rect, color, ancho=2):
    for i in range(5, 0, -1):
        pygame.draw.rect(pantalla, color, rect.inflate(i, i), ancho)

def dibujar_barra_vida(x, y, vida_actual, vida_max):
    ancho_barra = 200
    alto_barra = 20
    proporcion = max(vida_actual / vida_max, 0)
    barra_rect = pygame.Rect(x, y, ancho_barra * proporcion, alto_barra)
    borde_rect = pygame.Rect(x, y, ancho_barra, alto_barra)
    color = NEON_GREEN if proporcion > 0.5 else NEON_YELLOW if proporcion > 0.2 else NEON_RED
    pygame.draw.rect(pantalla, color, barra_rect)
    pygame.draw.rect(pantalla, NEON_BLUE, borde_rect, 2)

def mover_jugador(jugador, vel_x, vel_y, plataformas, dt):
    jugador.x += vel_x * dt
    for p in plataformas:
        if jugador.colliderect(p):
            if vel_x > 0:
                jugador.right = p.left
            elif vel_x < 0:
                jugador.left = p.right

    jugador.y += vel_y * dt
    en_suelo = False
    for p in plataformas:
        if jugador.colliderect(p):
            if vel_y > 0:
                jugador.bottom = p.top
                vel_y = 0
                en_suelo = True
            elif vel_y < 0:
                jugador.top = p.bottom
                vel_y = 0
    return vel_y, en_suelo

def mover_enemigos(enemigos, direcciones, plataformas, ancho, dt):
    for i, e in enumerate(enemigos):
        e.x += direcciones[i] * VEL_ENEMIGO * dt
        if e.left < 0 or e.right > ancho:
            direcciones[i] *= -1
        for p in plataformas:
            if e.colliderect(p):
                direcciones[i] *= -1
                break

# --- Bucle principal ---
puntos = 0
while True:
    dt = clock.tick_busy_loop(FPS) / 1000.0
    ahora = time.time()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Movimiento del jugador
    teclas = pygame.key.get_pressed()
    vel_x = 0
    if teclas[pygame.K_LEFT]:
        vel_x = -VEL_JUGADOR
    if teclas[pygame.K_RIGHT]:
        vel_x = VEL_JUGADOR
    if teclas[pygame.K_SPACE] and en_suelo:
        vel_y = FUERZA_SALTO
        en_suelo = False

    # Sistema de vida: movimiento vs quietud
    if vel_x != 0:
        if not movimiento_activo:
            movimiento_activo = True
            ultimo_mov_tiempo = ahora
        if ahora - ultimo_mov_tiempo > 0.5:
            vida = min(vida + 0.3, 100)
    else:
        if movimiento_activo:
            movimiento_activo = False
            ultimo_estatico_tiempo = ahora
        if ahora - ultimo_estatico_tiempo > 0.5:
            vida -= 0.5

    # Física
    vel_y += GRAVEDAD * dt
    if vel_y > 1000:
        vel_y = 1000
    vel_y, en_suelo = mover_jugador(jugador, vel_x, vel_y, plataformas, dt)

    # Enemigos
    mover_enemigos(enemigos, dir_enemigo, plataformas, ANCHO, dt)

    for e in enemigos:
        if jugador.colliderect(e):
            pygame.quit()
            sys.exit()

    # Game over
    if vida <= 0:
        pantalla.fill(FONDO)
        texto = fuente_grande.render("GAME OVER", True, NEON_RED)
        pantalla.blit(texto, (ANCHO // 2 - 150, ALTO // 2 - 30))
        pygame.display.flip()
        pygame.time.wait(2000)
        pygame.quit()
        sys.exit()

    # Dibujo
    pantalla.fill(FONDO)
    for p in plataformas:
        dibujar_neon(p, NEON_BLUE)
    dibujar_neon(jugador, NEON_GREEN)
    for e in enemigos:
        dibujar_neon(e, NEON_RED)

    dibujar_barra_vida(10, 40, vida, 100)
    puntos += dt * 60
    texto = fuente.render(f"Puntos: {int(puntos // 10)}", True, NEON_PURPLE)
    pantalla.blit(texto, (10, 10))
    pygame.display.flip()
