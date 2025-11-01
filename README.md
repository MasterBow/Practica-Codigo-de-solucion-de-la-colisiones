# 🟪 Neon Platformer — Solución de Colisiones con Física Independiente del FPS

## 📘 Descripción general

**Neon Platformer** es un proyecto en **Python** con **Pygame**, cuyo objetivo principal es demostrar una **solución integral de colisiones** dentro de un entorno 2D.  
El código implementa detección y respuesta física para:

- **Colisiones jugador–plataformas** (verticales y horizontales).  
- **Colisiones jugador–enemigo** con daño, invulnerabilidad temporal y *knockback físico*.  

El sistema de física utiliza **delta time (`dt`)**, lo que garantiza un comportamiento constante sin importar la tasa de cuadros por segundo (FPS).  
Esto desacopla la lógica del juego del rendimiento gráfico, permitiendo un movimiento y colisiones consistentes incluso en equipos con distinto hardware.

---

## Ejecución del programa

### Requisitos previos

- Python 3.10 o superior  
- Biblioteca `pygame` instalada:

```bash
pip install pygame
▶️ Ejecución

Ubícate en el directorio del proyecto y ejecuta:

python neong.py
```

El juego abrirá una ventana de 900x500 píxeles con entorno tipo platformer de estética neón.

| Elemento | Descripción |
|---|---|
| **Movimiento** | Flechas ← → para desplazarse, **Espacio** para saltar. |
| **Gravedad** | Constante de `1250 px/s²` aplicada mediante *delta time*. |
| **Colisiones con plataformas** | Bloquean movimiento vertical y horizontal, evitando traspaso. |
| **Colisiones con enemigos** | Aplican daño (-33%), generan knockback lateral y pequeño rebote vertical. |
| **Invulnerabilidad temporal** | Tras recibir daño, el jugador parpadea y no recibe daño por `0.4 s`. |
| **Vida dinámica** | Disminuye al estar quieto, se regenera al moverse. Si llega a `0`, el juego termina. |
| **Knockback** | Empuje físico suave (`200 px/s`), disipado progresivamente mediante decaimiento. |

## Diseño técnico
1. Física independiente de FPS

Se utiliza:

dt = clock.tick_busy_loop(FPS) / 1000.0


Esto convierte cada actualización en segundos reales, garantizando coherencia física sin depender del rendimiento gráfico.

### 2. Estructura modular

El programa divide su lógica en funciones reutilizables:

mover_jugador(): gestiona movimiento y colisiones del jugador.

mover_enemigos(): controla desplazamiento de enemigos y sus direcciones.

dibujar_neon(): genera efectos visuales tipo neón.

dibujar_barra_vida(): muestra vida en tiempo real con colores dinámicos.

### 3. Control de límites

El jugador siempre permanece dentro del área jugable:

if jugador.left < 0:
    jugador.left = 0
if jugador.right > ANCHO:
    jugador.right = ANCHO

### 4. Knockback controlado

En lugar de mover directamente al jugador, se aplica una velocidad lateral temporal que se disipa gradualmente:

knock_vel_x -= KNOCK_DECAY * knock_vel_x * dt


Esto evita el error clásico de salir del mapa al recibir impacto cerca de una pared.

### Inteligencia artificial asistiva en el desarrollo

Durante la fase de  investigación, depuración, optimización, se emplearon herramientas de asistencia por IA para apoyo sintáctico y estructural, manteniendo la autoría conceptual del desarrollador.

### Modelos y herramientas utilizadas:

GitHub Copilot IntelliCode — sugerencias contextuales en Visual Studio Code.

Qwen Code 2B y LLaMA 3.2 8B — ejecución y ajuste local mediante Ollama.

ChatGPT (GPT-5) — documentación técnica y justificación teórica.

Estas herramientas se usaron de forma local o en entorno seguro, con fines educativos.

### Referencias (formato APA, 7ª edición)

Harrison, P. (2024). Pygame documentation (v2.6.1). Pygame Community.
Recuperado de https://www.pygame.org/docs/

Tech With Tim. (2023). Pygame Platformer Tutorial – Collision and Physics [Video]. YouTube.
Recuperado de https://www.youtube.com/watch?v=Ongc4EVqRJo

Real Python. (2022). Working with Pygame in Python: A Developer’s Guide.
Recuperado de https://realpython.com/pygame-a-primer/

Microsoft. (2025). GitHub Copilot IntelliCode: AI-assisted code completion.
Recuperado de https://learn.microsoft.com/en-us/visualstudio/intellicode/

Alibaba Cloud. (2025). Qwen Code 2B: Lightweight Code Generation Model.
Recuperado de https://modelscope.cn/models/qwen/Qwen2.5-Coder-2B/

Meta AI. (2025). LLaMA 3.2 Technical Overview. Meta Research.
Recuperado de https://ai.meta.com/research/publications/llama-3/

Ollama Team. (2025). Running open-source LLMs locally. Ollama Documentation.
Recuperado de https://ollama.ai/

### Créditos

Desarrollado por [Rodriguez Fong Raul Alexi/Docente],
como parte del módulo Solución de Colisione.
