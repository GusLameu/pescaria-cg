import pygame
import random
import math
from game.entities import PeixeNormal, PeixeLendario, Barco, Pescador, VaraDePesca
from core.rasterizer import Rasterizer
from core.constants import gerar_textura_procedural


class Simulation:
    def __init__(self, width, height):
        self.width, self.height = width, height

        # 1. Entidades de Superfície
        self.barco = Barco(width // 2, 350)
        self.pescador = Pescador(self.barco)
        self.vara = VaraDePesca(self.pescador)

        # 2. Entidades Subaquáticas
        self.textura_lendaria = gerar_textura_procedural(64)
        self.peixe_lendario = PeixeLendario(
            random.randint(100, 700), 500, self.textura_lendaria)

        self.peixes_normais = [
            PeixeNormal(random.randint(0, width), random.randint(
                420, 580), random.choice([-2, -1, 1, 2]))
            for _ in range(5)
        ]

        # 3. Estado do Sistema (Zoom e Pontuação)
        self.zoom = 1.0
        self.target_zoom = 1.0
        self.pontuacao = 0

    def update(self):
        """Processa entradas do usuário e física do mundo."""
        keys = pygame.key.get_pressed()

        # Navegação do Barco
        if keys[pygame.K_LEFT] and self.barco.x > 100:
            self.barco.x -= 4
        if keys[pygame.K_RIGHT] and self.barco.x < self.width - 100:
            self.barco.x += 4

        # Movimentação do Anzol
        if keys[pygame.K_DOWN] and self.vara.profundidade_linha < 250:
            self.vara.profundidade_linha += 3
        if keys[pygame.K_UP] and self.vara.profundidade_linha > 20:
            self.vara.profundidade_linha -= 3

        # Controle de Câmera (Zoom) e Suavização via Lerp
        self.target_zoom = 0.5 if keys[pygame.K_z] else 1.0
        self.zoom += (self.target_zoom - self.zoom) * 0.1

        # Atualização de estados das entidades
        self.peixe_lendario.update()
        for p in self.peixes_normais:
            p.update()

        self._check_collisions()

    def _check_collisions(self):
        """Verifica intersecção entre anzol e peixes via distância euclidiana."""
        anzol_x = self.barco.x + 80
        anzol_y = self.barco.y - 70 + self.vara.profundidade_linha

        # Lógica de captura: Distância < Raio de Colisão
        dist_lendario = math.sqrt(
            (anzol_x - self.peixe_lendario.x)**2 + (anzol_y - self.peixe_lendario.y)**2)
        if dist_lendario < 45:
            self.pontuacao += 100
            self.peixe_lendario.x, self.peixe_lendario.y = random.randint(
                100, 700), random.randint(450, 550)
            self.vara.profundidade_linha = 20

        for p in self.peixes_normais:
            if math.sqrt((anzol_x - p.x)**2 + (anzol_y - p.y)**2) < 30:
                self.pontuacao += 10
                p.x = -150 if p.vel > 0 else 950
                self.vara.profundidade_linha = 20

    def get_world_to_screen(self):
        """Mapeamento Window-to-Viewport para implementação de Zoom."""
        ww, wh = self.width * self.zoom, self.height * self.zoom
        off_x, off_y = (self.width - ww) / 2, (self.height - wh) / 2

        # Retorna função de transformação para as coordenadas de tela
        return lambda x, y: ((x - off_x) * (self.width / ww), (y - off_y) * (self.height / wh))

    def draw_digit(self, canvas, digit, x, y, size, color):
        """Desenha caracteres usando segmentos de reta (Bresenham)."""
        pts = [(x, y), (x+size, y), (x, y+size), (x+size, y+size),
               (x, y+2*size), (x+size, y+2*size)]
        segments = {
            '0': [0, 1, 1, 3, 3, 5, 5, 4, 4, 2, 2, 0], '1': [1, 3, 3, 5],
            '2': [0, 1, 1, 3, 3, 2, 2, 4, 4, 5],       '3': [0, 1, 1, 3, 3, 2, 3, 5, 5, 4],
            '4': [0, 2, 2, 3, 1, 3, 3, 5],             '5': [1, 0, 0, 2, 2, 3, 3, 5, 5, 4],
            '6': [1, 0, 0, 2, 2, 4, 4, 5, 5, 3, 3, 2], '7': [0, 1, 1, 3, 3, 5],
            '8': [0, 1, 1, 3, 3, 5, 5, 4, 4, 2, 2, 0, 2, 3], '9': [3, 2, 2, 0, 0, 1, 1, 3, 3, 5, 5, 4]
        }
        seg_list = segments.get(str(digit), [])
        for i in range(0, len(seg_list), 2):
            p1, p2 = pts[seg_list[i]], pts[seg_list[i+1]]
            Rasterizer.draw_line(canvas, int(p1[0]), int(
                p1[1]), int(p2[0]), int(p2[1]), color)

    def draw_hud(self, canvas):
        """Renderiza o painel de pontuação na Viewport fixa."""
        score_str = str(self.pontuacao).zfill(4)
        for i, char in enumerate(score_str):
            self.draw_digit(canvas, char, 25 + i * 20, 25, 12, (255, 255, 255))
        # Moldura decorativa
        Rasterizer.draw_line(canvas, 15, 15, 115, 15, (200, 200, 200))
        Rasterizer.draw_line(canvas, 15, 15, 15, 65, (200, 200, 200))

    def render(self, canvas):
        """Gerencia a ordem de desenho (Depth Sorting manual)."""
        w2s = self.get_world_to_screen()

        # Ordem: Fundo -> Peixes -> Barco -> HUD
        for p in self.peixes_normais:
            p.render(canvas, w2s)
        self.peixe_lendario.render(canvas, w2s)
        self.barco.render(canvas, w2s)
        self.pescador.render(canvas, w2s)
        self.vara.render(canvas, w2s)
        self.draw_hud(canvas)
