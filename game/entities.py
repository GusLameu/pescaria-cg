import math
import pygame
from core.rasterizer import Rasterizer
from core.scanline import Scanline
from core.transforms import Transforms
from core.constants import PEIXE_MODELO_UV

# --- ENTIDADES DE SUPERFÍCIE (LÓGICA PIXEL ART ESCALÁVEL) ---


class Barco:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.cor_madeira = (80, 40, 0)
        self.orig_w, self.orig_h = 200, 30
        self.trap_offset = 20

    def render(self, canvas, world_to_screen_func):
        # Mapeia centro e dimensões do mundo para pixels da tela (Zoom)
        sx, sy = world_to_screen_func(self.x, self.y)

        p1x, _ = world_to_screen_func(self.x - self.orig_w // 2, self.y)
        p2x, _ = world_to_screen_func(self.x + self.orig_w // 2, self.y)
        screen_w = int(abs(p2x - p1x))

        _, p1y = world_to_screen_func(self.x, self.y)
        _, p2y = world_to_screen_func(self.x, self.y + self.orig_h)
        screen_h = int(abs(p2y - p1y))

        ptx1, _ = world_to_screen_func(self.x, self.y)
        ptx2, _ = world_to_screen_func(self.x + self.trap_offset, self.y)
        screen_trap = int(abs(ptx2 - ptx1))

        h_meio = screen_w // 2
        trap_y_limit = screen_h // 3

        # Rasterização manual para preservar estilo Pixel Art
        for dy in range(0, screen_h):
            for dx in range(-h_meio, h_meio):
                if (dy > trap_y_limit and (dx < -h_meio + screen_trap or dx > h_meio - screen_trap)):
                    continue
                canvas.set_pixel(int(sx + dx), int(sy + dy), self.cor_madeira)


class Pescador:
    def __init__(self, barco):
        self.barco = barco
        self.cor_pele = (255, 220, 180)
        self.cor_roupa = (0, 0, 0)
        self.cor_chapeu = (50, 30, 0)

    def render(self, canvas, world_to_screen_func):
        # Ponto de ancoragem (assento do pescador no barco)
        sx, sy = world_to_screen_func(self.barco.x, self.barco.y)

        # Função para converter tamanho do mundo para pixels de tela
        def w_to_s(dim):
            v1, _ = world_to_screen_func(0, 0)
            v2, _ = world_to_screen_func(dim, 0)
            return int(abs(v2 - v1))

        # 1. Definir dimensões escaladas
        tw, th = w_to_s(20), w_to_s(40)  # Tronco
        cw, ch = w_to_s(20), w_to_s(20)  # Cabeça
        hw, hh = w_to_s(45), w_to_s(10)  # Chapéu (um pouco mais largo)

        # 2. Calcular Posições X (Centralização)
        # O tronco começa em um offset lateral fixo
        off_x = w_to_s(-10)
        tronco_x = int(sx + off_x)
        cabeca_x = tronco_x + (tw - cw) // 2
        chapeu_x = cabeca_x - (hw - cw) // 2

        # 3. Desenhar de baixo para cima (Empilhamento garantido)
        # Tronco
        for dy in range(int(sy - th), int(sy)):
            for dx in range(tronco_x, tronco_x + tw):
                canvas.set_pixel(dx, dy, self.cor_roupa)

        # Cabeça (Exatamente acima do tronco)
        topo_tronco = int(sy - th)
        for dy in range(topo_tronco - ch, topo_tronco):
            for dx in range(cabeca_x, cabeca_x + cw):
                canvas.set_pixel(dx, dy, self.cor_pele)

        # Chapéu (Exatamente acima da cabeça)
        topo_cabeca = topo_tronco - ch
        for dy in range(topo_cabeca - hh, topo_cabeca):
            for dx in range(chapeu_x, chapeu_x + hw):
                canvas.set_pixel(dx, dy, self.cor_chapeu)


class VaraDePesca:
    def __init__(self, pescador):
        self.pescador = pescador
        self.profundidade_linha = 100
        self.cor_vara, self.cor_linha = (0, 0, 0), (255, 255, 255)

    def render(self, canvas, world_to_screen_func):
        # Pontos transformados para uso com algoritmo de Bresenham
        orig_x, orig_y = world_to_screen_func(
            self.pescador.barco.x, self.pescador.barco.y - 30)
        ponta_x, ponta_y = world_to_screen_func(
            self.pescador.barco.x + 80, self.pescador.barco.y - 70)
        Rasterizer.draw_line(canvas, int(orig_x), int(
            orig_y), int(ponta_x), int(ponta_y), self.cor_vara)

        anzol_x, anzol_y = world_to_screen_func(self.pescador.barco.x + 80,
                                                self.pescador.barco.y - 70 + self.profundidade_linha)
        Rasterizer.draw_line(canvas, int(ponta_x), int(
            ponta_y), int(anzol_x), int(anzol_y), self.cor_linha)

# --- ENTIDADES SUBQUÁTICAS (TRANSFORMAÇÕES MATRICIAIS) ---


class PeixeNormal:
    def __init__(self, x, y, velocidade):
        self.x, self.y, self.velocidade = x, y, velocidade
        self.cor = (180, 170, 100)
        self.scale = 0.6
        self.vertices_base = [v[0] for v in PEIXE_MODELO_UV]

    def update(self):
        self.x += self.velocidade
        if self.x > 900:
            self.x = -100
        if self.x < -100:
            self.x = 900

    def render(self, canvas, world_to_screen_func):
        # Composição de matrizes: Translação * Flip (Direção) * Escala
        m_escala = Transforms.scale(self.scale, self.scale)
        m_flip = Transforms.scale(-1 if self.velocidade < 0 else 1, 1)
        m_trans = Transforms.translation(self.x, self.y)
        m_final = Transforms.multiply(
            m_trans, Transforms.multiply(m_flip, m_escala))

        pontos_render = []
        for pt in self.vertices_base:
            p_mundo = Transforms.apply(m_final, pt)
            pontos_render.append(world_to_screen_func(p_mundo[0], p_mundo[1]))

        Scanline.fill_polygon(canvas, pontos_render, self.cor)


class PeixeLendario:
    def __init__(self, x, y, textura_matriz):
        self.x, self.y, self.textura = x, y, textura_matriz
        self.angle, self.scale = 0, 1.3
        self.model = PEIXE_MODELO_UV

    def update(self):
        tempo = pygame.time.get_ticks() * 0.001
        self.angle = math.sin(tempo) * 20
        self.y += math.sin(tempo * 2) * 0.5

    def render(self, canvas, world_to_screen_func):
        # Pipeline: Transformação Local -> Mundo -> Viewport (Screen)
        m_final = Transforms.multiply(Transforms.translation(self.x, self.y),
                                      Transforms.multiply(Transforms.rotation(self.angle),
                                      Transforms.scale(self.scale, self.scale)))

        pontos_render = []
        for pt_local, uv in self.model:
            p_mundo = Transforms.apply(m_final, pt_local)
            pontos_render.append(
                (world_to_screen_func(p_mundo[0], p_mundo[1]), uv))

        Scanline.fill_textured_polygon_procedural(
            canvas, pontos_render, self.textura)
