import pygame
import sys

WIDTH, HEIGHT = 800, 600
# screen será passado ou usado globalmente, mas por enquanto assume que está definido

# Cores
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 100, 255)
RED = (255, 50, 50)
GREEN = (50, 255, 100)
YELLOW = (255, 255, 0)


# SET PIXEL

def set_pixel(screen, x, y, color):
    if 0 <= x < WIDTH and 0 <= y < HEIGHT:
        screen.set_at((x, y), color)


# BRESENHAM (RETA)

def draw_line(screen, x1, y1, x2, y2, color):
    dx = abs(x2 - x1)
    dy = abs(y2 - y1)
    sx = 1 if x1 < x2 else -1
    sy = 1 if y1 < y2 else -1
    err = dx - dy

    while True:
        set_pixel(screen, x1, y1, color)
        if x1 == x2 and y1 == y2:
            break
        e2 = 2 * err
        if e2 > -dy:
            err -= dy
            x1 += sx
        if e2 < dx:
            err += dx
            y1 += sy


# CIRCUNFERÊNCIA (MIDPOINT)

def draw_circle(screen, xc, yc, r, color):
    x = 0
    y = r
    p = 1 - r

    def plot_circle_points(xc, yc, x, y):
        points = [
            (xc+x, yc+y), (xc-x, yc+y),
            (xc+x, yc-y), (xc-x, yc-y),
            (xc+y, yc+x), (xc-y, yc+x),
            (xc+y, yc-x), (xc-y, yc-x)
        ]
        for px, py in points:
            set_pixel(screen, px, py, color)

    plot_circle_points(xc, yc, x, y)

    while x < y:
        x += 1
        if p < 0:
            p += 2*x + 1
        else:
            y -= 1
            p += 2*(x - y) + 1
        plot_circle_points(xc, yc, x, y)


# ELIPSE (MIDPOINT)

def draw_ellipse(screen, xc, yc, rx, ry, color):
    x = 0
    y = ry

    rx2 = rx * rx
    ry2 = ry * ry

    p1 = ry2 - rx2 * ry + 0.25 * rx2

    dx = 2 * ry2 * x
    dy = 2 * rx2 * y

    def plot_ellipse(xc, yc, x, y):
        set_pixel(screen, xc + x, yc + y, color)
        set_pixel(screen, xc - x, yc + y, color)
        set_pixel(screen, xc + x, yc - y, color)
        set_pixel(screen, xc - x, yc - y, color)

    # Região 1
    while dx < dy:
        plot_ellipse(xc, yc, x, y)
        x += 1
        dx += 2 * ry2
        if p1 < 0:
            p1 += dx + ry2
        else:
            y -= 1
            dy -= 2 * rx2
            p1 += dx - dy + ry2

    # Região 2
    p2 = (ry2)*(x+0.5)**2 + (rx2)*(y-1)**2 - rx2*ry2

    while y >= 0:
        plot_ellipse(xc, yc, x, y)
        y -= 1
        dy -= 2 * rx2
        if p2 > 0:
            p2 += rx2 - dy
        else:
            x += 1
            dx += 2 * ry2
            p2 += dx - dy + rx2


# FLOOD FILL

def flood_fill(screen, x, y, target_color, new_color):
    if target_color == new_color:
        return

    stack = [(x, y)]

    while stack:
        px, py = stack.pop()

        if (0 <= px < WIDTH and 0 <= py < HEIGHT and
            screen.get_at((px, py))[:3] == target_color):

            set_pixel(screen, px, py, new_color)

            stack.append((px+1, py))
            stack.append((px-1, py))
            stack.append((px, py+1))
            stack.append((px, py-1))


# FERRAMENTAS DE PIXEL ART PARA FUNDO

def draw_rect_fill(screen, x1, y1, x2, y2, color):
    for y in range(y1, y2):
        for x in range(x1, x2):
            set_pixel(screen, x, y, color)


def draw_sky(screen):
    for y in range(HEIGHT):
        r = int(255 * (1 - y / HEIGHT))
        g = int(150 * (1 - y / HEIGHT))
        b = int(200 * (y / HEIGHT))
        for x in range(WIDTH):
            set_pixel(screen, x, y, (r, g, b))


def draw_sun(screen, cx, cy, radius, color):
    for y in range(-radius, radius):
        for x in range(-radius, radius):
            if x*x + y*y <= radius*radius:
                set_pixel(screen, cx + x, cy + y, color)


def draw_water(screen):
    for y in range(HEIGHT // 2, HEIGHT):
        for x in range(WIDTH):
            set_pixel(screen, x, y, (20, 50, 120))


def draw_boat(screen):
    for y in range(350, 380):
        for x in range(300, 500):
            if (y > 360 and (x < 320 or x > 480)):
                continue
            set_pixel(screen, x, y, (80, 40, 0))


def draw_fisherman(screen):
    draw_rect_fill(screen, 380, 300, 400, 350, (0, 0, 0))
    draw_rect_fill(screen, 380, 280, 400, 300, (255, 220, 180))
    draw_rect_fill(screen, 370, 270, 410, 280, (50, 30, 0))
    for i in range(100):
        set_pixel(screen, 400 + i, 300 - i // 2, (0, 0, 0))
    for i in range(50):
        set_pixel(screen, 500, 250 + i, (255, 255, 255))



# CURSOR ANZOL COM SET PIXEL

def create_hook_cursor_pixelart():
    """Cria um cursor customizado em forma de anzol usando set_pixel"""
    cursor_size = 32
    cursor_surface = pygame.Surface((cursor_size, cursor_size))
    cursor_surface.fill(BLACK)
    cursor_surface.set_colorkey(BLACK)  # Faz o preto ficar transparente
    
    # Função para desenhar pixel no cursor
    def draw_hook_pixel(x, y, color):
        if 0 <= x < cursor_size and 0 <= y < cursor_size:
            cursor_surface.set_at((x, y), color)
    
    # Haste vertical do anzol
    for y in range(3, 18):
        draw_hook_pixel(15, y, WHITE)
        draw_hook_pixel(16, y, WHITE)
    
    # Curva do anzol (gancho)
    # Parte superior do gancho
    for x in range(12, 19):
        draw_hook_pixel(x, 18, WHITE)
    
    # Lado esquerdo da curva
    draw_hook_pixel(12, 19, WHITE)
    draw_hook_pixel(12, 20, WHITE)
    draw_hook_pixel(11, 21, WHITE)
    
    # Fundo do gancho
    draw_hook_pixel(11, 21, WHITE)
    draw_hook_pixel(11, 22, WHITE)
    draw_hook_pixel(12, 23, WHITE)
    
    # Lado direito da curva
    draw_hook_pixel(13, 24, WHITE)
    draw_hook_pixel(14, 24, WHITE)
    
    # Ponta do anzol (afiada)
    draw_hook_pixel(15, 25, WHITE)
    draw_hook_pixel(14, 26, WHITE)
    draw_hook_pixel(15, 26, WHITE)
    draw_hook_pixel(16, 26, WHITE)
    
    # Define o cursor
    pygame.mouse.set_cursor((8, 2), cursor_surface)


# DESENHAR MENU

def draw_menu(screen):
    draw_sky(screen)
    draw_sun(screen, 600, 150, 60, (255, 180, 0))
    draw_water(screen)
    draw_boat(screen)
    draw_fisherman(screen)

    # Título do jogo
    title_font = pygame.font.SysFont("Arial", 48, bold=True)
    title_text = title_font.render("Pescaria CG", True, WHITE)
    screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, 100))

    # Opções do menu
    option_font = pygame.font.SysFont("Arial", 36)
    iniciar_text = option_font.render("Iniciar", True, WHITE)
    instrucoes_text = option_font.render("Instruções", True, WHITE)
    sair_text = option_font.render("Sair", True, WHITE)

    iniciar_rect = iniciar_text.get_rect(center=(WIDTH // 2, 250))
    instrucoes_rect = instrucoes_text.get_rect(center=(WIDTH // 2, 320))
    sair_rect = sair_text.get_rect(center=(WIDTH // 2, 390))

    screen.blit(iniciar_text, iniciar_rect)
    screen.blit(instrucoes_text, instrucoes_rect)
    screen.blit(sair_text, sair_rect)

    # Retorna os retângulos para detecção de clique
    return iniciar_rect, instrucoes_rect, sair_rect

# LOOP PRINCIPAL

def main(screen):
    # Define o cursor como anzol
    create_hook_cursor_pixelart()
    
    clock = pygame.time.Clock()
    running = True

    while running:
        iniciar_rect, instrucoes_rect, sair_rect = draw_menu(screen)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "sair"

            # Detecção de clique do mouse
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Botão esquerdo do mouse
                    mouse_pos = event.pos
                    if iniciar_rect.collidepoint(mouse_pos):
                        return "iniciar"
                    elif instrucoes_rect.collidepoint(mouse_pos):
                        return "instrucoes"
                    elif sair_rect.collidepoint(mouse_pos):
                        return "sair"

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    return "iniciar"
                elif event.key == pygame.K_2:
                    return "instrucoes"
                elif event.key == pygame.K_3:
                    return "sair"

        clock.tick(60)
