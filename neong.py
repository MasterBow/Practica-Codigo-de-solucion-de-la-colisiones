import pygame
import sys

# --- Inicialización ---
pygame.init()
ANCHO, ALTO = 900, 500
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Neon Platformer")

# --- Configuración ---
clock = pygame.time.Clock()
FPS = 120
fuente = pygame.font.SysFont("consolas", 22)

# --- Colores ---
NEON_RED = (255, 50, 50)
NEON_BLUE = (50, 200, 255)
NEON_GREEN = (0, 255, 128)
NEON_PURPLE = (200, 0, 255)
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

# --- Funciones auxiliares ---
def dibujar_neon(rect, color, ancho=2):
    for i in range(5, 0, -1):
        pygame.draw.rect(pantalla, color, rect.inflate(i, i), ancho)

def mover_jugador(jugador, vel_x, vel_y, plataformas, dt):
    # Movimiento horizontal
    jugador.x += vel_x * dt
    for p in plataformas:
        if jugador.colliderect(p):
            if vel_x > 0:
                jugador.right = p.left
            elif vel_x < 0:
                jugador.left = p.right

    # Movimiento vertical
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

    # Física con delta
    vel_y += GRAVEDAD * dt
    if vel_y > 1000:
        vel_y = 1000
    vel_y, en_suelo = mover_jugador(jugador, vel_x, vel_y, plataformas, dt)

    # Movimiento enemigos
    mover_enemigos(enemigos, dir_enemigo, plataformas, ANCHO, dt)

    # Colisión con enemigos (final inmediato)
    for e in enemigos:
        if jugador.colliderect(e):
            pygame.quit()
            sys.exit()

    # Dibujo
    pantalla.fill(FONDO)
    for p in plataformas:
        dibujar_neon(p, NEON_BLUE)
    dibujar_neon(jugador, NEON_GREEN)
    for e in enemigos:
        dibujar_neon(e, NEON_RED)

    puntos += dt * 60
    texto = fuente.render(f"Puntos: {int(puntos // 10)}", True, NEON_PURPLE)
    pantalla.blit(texto, (10, 10))
    pygame.display.flip()
