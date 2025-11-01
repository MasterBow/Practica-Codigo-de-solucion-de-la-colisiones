import pygame
import sys

# Inicialización
pygame.init()
ANCHO, ALTO = 900, 500
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Neon Platformer")

# Colores neón
NEON_RED = (255, 50, 50)
NEON_BLUE = (50, 200, 255)
NEON_GREEN = (0, 255, 128)
NEON_PURPLE = (200, 0, 255)
FONDO = (0, 0, 0)

clock = pygame.time.Clock()
fuente = pygame.font.SysFont("consolas", 22)

# Jugador
jugador = pygame.Rect(100, 400, 30, 40)
vel_y = 0
en_suelo = False
vel_x = 0

# Mundo / plataformas
plataformas = [
    pygame.Rect(0, 460, 900, 40),   # suelo
    pygame.Rect(200, 380, 120, 10),
    pygame.Rect(400, 300, 120, 10),
    pygame.Rect(650, 340, 150, 10),
    pygame.Rect(0, 10, 0, 500),#paredes laterales
    pygame.Rect(897, 10, 0, 500),
]

# Enemigos
enemigos = [
    pygame.Rect(500, 430, 30, 30),
    pygame.Rect(700, 310, 30, 30)
]

# Movimiento enemigo
dir_enemigo = [1, -1]

# Función de dibujo neón
def dibujar_neon(rect, color, ancho=2):
    for i in range(5, 0, -1):
        pygame.draw.rect(pantalla, color, rect.inflate(i, i), ancho)

# Bucle principal
puntos = 0
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Movimiento del jugador
    teclas = pygame.key.get_pressed()
    vel_x = 0
    if teclas[pygame.K_LEFT]:
        vel_x = -5
    if teclas[pygame.K_RIGHT]:
        vel_x = 5
    if teclas[pygame.K_SPACE] and en_suelo:
        vel_y = -15
        en_suelo = False

    # Gravedad
    vel_y += 1
    if vel_y > 10:
        vel_y = 10

    # Movimiento horizontal
    jugador.x += vel_x

    # Colisión horizontal
    for p in plataformas:
        if jugador.colliderect(p):
            print("Colicion con horizontal")
            if vel_x > 0:
                jugador.right = p.left
            if vel_x < 0:
                jugador.left = p.right

    # Movimiento vertical
    jugador.y += vel_y

    # Colisión vertical
    en_suelo = False
    for p in plataformas:
        if jugador.colliderect(p):
            print("vertical")
            if vel_y > 0:
                jugador.bottom = p.top
                en_suelo = True
                vel_y = 0
            elif vel_y < 0:
                jugador.top = p.bottom
                vel_y = 0

    # Movimiento enemigo simple
    for i, e in enumerate(enemigos):
        e.x += dir_enemigo[i] * 2
        if e.left < 0 or e.right > ANCHO:
            dir_enemigo[i] *= -1
        # Colisión jugador-enemigo
        if jugador.colliderect(e):
            pygame.quit()
            sys.exit()

    # Fondo
    pantalla.fill(FONDO)

    # Dibujar plataformas y suelo
    for p in plataformas:
        dibujar_neon(p, NEON_BLUE)

    # Dibujar jugador
    dibujar_neon(jugador, NEON_GREEN)

    # Dibujar enemigos
    for e in enemigos:
        dibujar_neon(e, NEON_RED)

    # Puntos (incrementan con el tiempo)
    puntos += 1
    texto = fuente.render(f"Puntos: {puntos // 10}", True, NEON_PURPLE)
    pantalla.blit(texto, (10, 10))

    pygame.display.flip()
    clock.tick(60)

