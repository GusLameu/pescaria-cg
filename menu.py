import pygame
import sys
from core.rasterizer import Rasterizer

# ---------------------------------------------------------------------------
# menu.py — tela de menu principal com pixel art desenhado manualmente
#
# Este arquivo usa as implementações de core/rasterizer.py (Bresenham, Ponto
# Médio, Flood Fill) em vez de reimplementá-las localmente.
#
# Adaptador _SurfaceCanvas:
#   O Rasterizer espera um objeto com .set_pixel() e .get_pixel(), mas o
#   menu opera diretamente sobre pygame.Surface. O adaptador faz a ponte
#   entre as duas interfaces sem copiar dados.
# ---------------------------------------------------------------------------

WIDTH, HEIGHT = 800, 600

BLACK  = (0, 0, 0)
WHITE  = (255, 255, 255)
BLUE   = (0, 100, 255)
RED    = (255, 50, 50)
GREEN  = (50, 255, 100)
YELLOW = (255, 255, 0)


class _SurfaceCanvas:
    # Adaptador leve: envolve um pygame.Surface na interface esperada pelo Rasterizer.
    # Criado temporariamente dentro de cada função de desenho.
    def __init__(self, surface):
        self.surface = surface
        self.width  = surface.get_width()
        self.height = surface.get_height()

    def set_pixel(self, x, y, color):
        x, y = int(x), int(y)
        if 0 <= x < self.width and 0 <= y < self.height:
            self.surface.set_at((x, y), color)

    def get_pixel(self, x, y):
        x, y = int(x), int(y)
        if 0 <= x < self.width and 0 <= y < self.height:
            c = self.surface.get_at((x, y))
            return (c.r, c.g, c.b)
        return None


# ---------------------------------------------------------------------------
# FUNÇÕES DE DESENHO DO FUNDO DO MENU
# ---------------------------------------------------------------------------

def draw_rect_fill(screen, x1, y1, x2, y2, color):
    # Retângulo preenchido pixel a pixel — sem equivalente direto no core.
    # Usado para corpo, cabeça e chapéu do pescador.
    c = _SurfaceCanvas(screen)
    for y in range(y1, y2):
        for x in range(x1, x2):
            c.set_pixel(x, y, color)


def draw_sky(screen):
    # Gradiente de céu calculado por fórmula linha a linha.
    # r e g decrescem de cima para baixo; b cresce → topo claro, base azul escuro.
    c = _SurfaceCanvas(screen)
    for y in range(HEIGHT):
        r = int(255 * (1 - y / HEIGHT))
        g = int(150 * (1 - y / HEIGHT))
        b = int(200 * (y / HEIGHT))
        for x in range(WIDTH):
            c.set_pixel(x, y, (r, g, b))


def draw_sun(screen, cx, cy, radius, color):
    # Contorno branco via Rasterizer (Ponto Médio) + preenchimento via Flood Fill.
    c = _SurfaceCanvas(screen)
    Rasterizer.draw_circle(c, cx, cy, radius, WHITE)
    Rasterizer.flood_fill(c, cx, cy, color)


def draw_water(screen):
    # Metade inferior preenchida com azul escuro simulando o mar.
    c = _SurfaceCanvas(screen)
    for y in range(HEIGHT // 2, HEIGHT):
        for x in range(WIDTH):
            c.set_pixel(x, y, (20, 50, 120))


def desenhar_poligono(screen, pontos, cor):
    # Contorno de polígono: Bresenham entre vértices consecutivos (fechado).
    c = _SurfaceCanvas(screen)
    qtd = len(pontos)
    for i in range(qtd):
        x1, y1 = pontos[i]
        x2, y2 = pontos[(i + 1) % qtd]
        Rasterizer.draw_line(c, x1, y1, x2, y2, cor)


def draw_boat(screen):
    # Casco trapezoidal: contorno branco (Bresenham) + flood fill marrom.
    casco = [(300, 360), (500, 360), (480, 380), (320, 380)]
    c = _SurfaceCanvas(screen)
    desenhar_poligono(screen, casco, WHITE)
    Rasterizer.flood_fill(c, 400, 370, (139, 69, 19))


def draw_fisherman(screen):
    # Pescador: retângulos (tronco/cabeça/chapéu), pixels manuais (vara/linha)
    # e elipses + flood fill (pés).
    c = _SurfaceCanvas(screen)
    draw_rect_fill(screen, 380, 300, 400, 350, (0, 0, 0))        # tronco
    draw_rect_fill(screen, 380, 280, 400, 300, (255, 220, 180))   # cabeça
    draw_rect_fill(screen, 370, 270, 410, 280, (50, 30, 0))       # chapéu

    # Vara de pesca: pixels diagonais manuais
    for i in range(100):
        c.set_pixel(400 + i, 300 - i // 2, (0, 0, 0))

    # Linha de pesca: coluna vertical branca
    for i in range(50):
        c.set_pixel(500, 250 + i, (255, 255, 255))

    draw_rect_fill(screen, 380, 300, 400, 350, (0, 0, 0))   # redesenha tronco sobre a linha

    # Pé esquerdo: elipse (Ponto Médio) + flood fill
    Rasterizer.draw_ellipse(c, 385, 355, 8, 4, WHITE)
    Rasterizer.flood_fill(c, 385, 355, BLACK)

    # Pé direito: elipse (Ponto Médio) + flood fill
    Rasterizer.draw_ellipse(c, 395, 355, 8, 4, WHITE)
    Rasterizer.flood_fill(c, 395, 355, BLACK)


# ---------------------------------------------------------------------------
# CURSOR PERSONALIZADO EM FORMA DE ANZOL
# ---------------------------------------------------------------------------

def create_hook_cursor_pixelart():
    # Cursor 32×32 desenhado pixel a pixel em forma de anzol.
    # set_colorkey(BLACK) torna o preto transparente.
    cursor_size    = 32
    cursor_surface = pygame.Surface((cursor_size, cursor_size))
    cursor_surface.fill(BLACK)
    cursor_surface.set_colorkey(BLACK)

    def draw_hook_pixel(x, y, color):
        if 0 <= x < cursor_size and 0 <= y < cursor_size:
            cursor_surface.set_at((x, y), color)

    for y in range(3, 18):          # haste vertical
        draw_hook_pixel(15, y, WHITE)
        draw_hook_pixel(16, y, WHITE)

    for x in range(12, 19):         # topo horizontal do gancho
        draw_hook_pixel(x, 18, WHITE)

    draw_hook_pixel(12, 19, WHITE)
    draw_hook_pixel(12, 20, WHITE)
    draw_hook_pixel(11, 21, WHITE)
    draw_hook_pixel(11, 22, WHITE)
    draw_hook_pixel(12, 23, WHITE)
    draw_hook_pixel(13, 24, WHITE)
    draw_hook_pixel(14, 24, WHITE)
    draw_hook_pixel(15, 25, WHITE)  # ponta afiada
    draw_hook_pixel(14, 26, WHITE)
    draw_hook_pixel(15, 26, WHITE)
    draw_hook_pixel(16, 26, WHITE)

    pygame.mouse.set_cursor((8, 2), cursor_surface)


# ---------------------------------------------------------------------------
# RENDERIZAÇÃO DO MENU
# ---------------------------------------------------------------------------

def draw_menu(screen):
    # Renderiza o fundo completo e os botões.
    # Retorna os Rects dos 3 botões para detecção de clique.
    draw_sky(screen)
    draw_sun(screen, 600, 150, 60, YELLOW)
    draw_water(screen)
    draw_boat(screen)
    draw_fisherman(screen)

    title_font  = pygame.font.SysFont("Arial", 48, bold=True)
    title_text  = title_font.render("Pescaria CG", True, WHITE)
    screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, 100))

    option_font     = pygame.font.SysFont("Arial", 36)
    iniciar_text    = option_font.render("Iniciar",    True, WHITE)
    instrucoes_text = option_font.render("Instruções", True, WHITE)
    sair_text       = option_font.render("Sair",       True, WHITE)

    iniciar_rect    = iniciar_text.get_rect(center=(WIDTH // 2, 250))
    instrucoes_rect = instrucoes_text.get_rect(center=(WIDTH // 2, 320))
    sair_rect       = sair_text.get_rect(center=(WIDTH // 2, 390))

    screen.blit(iniciar_text,    iniciar_rect)
    screen.blit(instrucoes_text, instrucoes_rect)
    screen.blit(sair_text,       sair_rect)

    return iniciar_rect, instrucoes_rect, sair_rect


# ---------------------------------------------------------------------------
# LOOP DO MENU
# ---------------------------------------------------------------------------

def main(screen):
    # Executa um loop próprio até o jogador escolher uma opção,
    # retornando "iniciar", "instrucoes" ou "sair".
    create_hook_cursor_pixelart()
    clock = pygame.time.Clock()

    while True:
        iniciar_rect, instrucoes_rect, sair_rect = draw_menu(screen)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "sair"

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
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
