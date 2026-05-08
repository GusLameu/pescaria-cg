import pygame
import random
import math
from game.entities import PeixeNormal, PeixeLendario, Barco, Pescador, VaraDePesca
from core.rasterizer import Rasterizer
from core.scanline import Scanline
from core.constants import gerar_textura_procedural
from core.clipping import Clipping


class Simulation:
    def __init__(self, width, height):
        self.width, self.height = width, height

        self.barco = Barco(width // 2, 350)
        self.pescador = Pescador(self.barco)
        self.vara = VaraDePesca(self.pescador)

        self.textura_lendaria = gerar_textura_procedural(64)
        self.peixe_lendario = PeixeLendario(
            random.randint(100, 700), 480, self.textura_lendaria)

        PEIXE_Y_MIN = 400
        PEIXE_Y_MAX = height - 5
        self._peixe_y_min = PEIXE_Y_MIN
        self._peixe_y_max = PEIXE_Y_MAX

        self.peixes_normais = [
            PeixeNormal(random.randint(0, width), random.randint(
                PEIXE_Y_MIN, PEIXE_Y_MAX), random.choice([-2, -1, 1, 2]))
            for _ in range(5)
        ]

        self.zoom = 1.0
        self.target_zoom = 1.0
        self.pontuacao = 0

        self.qte_ativo = False
        self.qte_progresso = 0.0
        self.qte_decaimento = 0.004
        self.qte_ganho = 0.12

        self.peixe_fisgado = None
        self.lendario_capturado = False
        self.fuga_tempo = 0

        self.wave_offset = 0.0

        self.tempo_inicio = pygame.time.get_ticks()
        self.duracao_jogo = 90000

    def get_tempo_restante(self):
        tempo_decorrido = pygame.time.get_ticks() - self.tempo_inicio
        return max(0, (self.duracao_jogo - tempo_decorrido) // 1000)

    def tempo_acabou(self):
        return pygame.time.get_ticks() - self.tempo_inicio >= self.duracao_jogo

    def update(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT] and self.barco.x > 100:
            self.barco.x -= 4
            self.barco.direcao = -1
        if keys[pygame.K_RIGHT] and self.barco.x < self.width - 100:
            self.barco.x += 4
            self.barco.direcao = 1

        self.barco.direcao_smooth += (self.barco.direcao - self.barco.direcao_smooth) * 0.1

        if keys[pygame.K_DOWN] and self.vara.profundidade_linha < self.height - 70:
            self.vara.profundidade_linha += 3
        if keys[pygame.K_UP] and self.vara.profundidade_linha > 0:
            self.vara.profundidade_linha -= 3

        self.target_zoom = 0.5 if keys[pygame.K_z] else 1.0
        self.zoom += (self.target_zoom - self.zoom) * 0.1

        self.wave_offset += 0.04

        self.peixe_lendario.update()
        for p in self.peixes_normais:
            antes_x = p.x
            p.update()
            if (antes_x > 850 and p.x < 0) or (antes_x < -50 and p.x > 800):
                p.y = random.randint(self._peixe_y_min, self._peixe_y_max)

        self._check_collisions()

        anzol_x = self.barco.x + (80 * self.barco.direcao_smooth)
        anzol_y = self.barco.y - 70 + self.vara.profundidade_linha
        AGUA_Y = 370

        if self.qte_ativo:
            self.peixe_lendario.x = anzol_x
            self.peixe_lendario.y = anzol_y

        if self.lendario_capturado:
            self.vara.profundidade_linha = max(0, self.vara.profundidade_linha - 3)
            self.peixe_lendario.x = anzol_x
            self.peixe_lendario.y = max(anzol_y, AGUA_Y)
            if anzol_y <= AGUA_Y:
                self.pontuacao += 100
                self.peixe_lendario.x = random.randint(100, 700)
                self.peixe_lendario.y = random.randint(self._peixe_y_min, self._peixe_y_max)
                self.vara.profundidade_linha = 0
                self.lendario_capturado = False

        if self.peixe_fisgado is not None:
            self.vara.profundidade_linha = max(0, self.vara.profundidade_linha - 3)
            self.peixe_fisgado.x = anzol_x
            self.peixe_fisgado.y = max(anzol_y, AGUA_Y)
            if anzol_y <= AGUA_Y:
                self.pontuacao += 10
                self.peixe_fisgado.x = -150 if self.peixe_fisgado.velocidade > 0 else 950
                self.peixe_fisgado.y = random.randint(self._peixe_y_min, self._peixe_y_max)
                self.peixe_fisgado = None
                self.vara.profundidade_linha = 0

        if self.qte_ativo:
            self.qte_progresso -= self.qte_decaimento
            if self.qte_progresso <= 0.0:
                self.qte_ativo = False
                self.qte_progresso = 0.0
                self.peixe_lendario.x = random.randint(100, 700)
                self.peixe_lendario.y = random.randint(self._peixe_y_min, self._peixe_y_max)
                self.fuga_tempo = pygame.time.get_ticks()

    def _check_collisions(self):
        anzol_x = self.barco.x + (80 * self.barco.direcao_smooth)
        anzol_y = self.barco.y - 70 + self.vara.profundidade_linha

        dist_lendario = math.sqrt(
            (anzol_x - self.peixe_lendario.x)**2 + (anzol_y - self.peixe_lendario.y)**2)
        if (dist_lendario < 45
                and not self.qte_ativo
                and not self.lendario_capturado
                and self.peixe_fisgado is None):
            self.qte_ativo = True
            self.qte_progresso = 0.25

        for p in self.peixes_normais:
            if (self.peixe_fisgado is None
                    and not self.qte_ativo
                    and not self.lendario_capturado
                    and math.sqrt((anzol_x - p.x)**2 + (anzol_y - p.y)**2) < 30):
                self.peixe_fisgado = p

    def tentar_capturar_lendario(self):
        if self.qte_ativo and not self.lendario_capturado:
            self.qte_progresso += self.qte_ganho
            if self.qte_progresso >= 1.0:
                self.qte_ativo = False
                self.qte_progresso = 0.0
                self.lendario_capturado = True

    def get_world_to_screen(self):
        ww, wh = self.width * self.zoom, self.height * self.zoom
        off_x, off_y = (self.width - ww) / 2, (self.height - wh) / 2
        return lambda x, y: ((x - off_x) * (self.width / ww), (y - off_y) * (self.height / wh))

    def draw_digit(self, canvas, digit, x, y, size, color):
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
            Rasterizer.draw_line(canvas, int(p1[0]), int(p1[1]), int(p2[0]), int(p2[1]), color)

    def draw_hud(self, canvas):
        score_str = str(self.pontuacao).zfill(4)
        for i, char in enumerate(score_str):
            self.draw_digit(canvas, char, 25 + i * 20, 25, 12, (255, 255, 255))
        Rasterizer.draw_line(canvas, 15, 15, 115, 15, (200, 200, 200))
        Rasterizer.draw_line(canvas, 15, 15, 15, 65, (200, 200, 200))

        tempo = self.get_tempo_restante()
        minutos = tempo // 60
        segundos = tempo % 60
        cx = self.width // 2 - 30
        self.draw_digit(canvas, minutos, cx, 20, 14, (255, 255, 100))
        canvas.set_pixel(cx + 20, 28, (255, 255, 100))
        canvas.set_pixel(cx + 20, 32, (255, 255, 100))
        canvas.set_pixel(cx + 21, 28, (255, 255, 100))
        canvas.set_pixel(cx + 21, 32, (255, 255, 100))
        self.draw_digit(canvas, segundos // 10, cx + 26, 20, 14, (255, 255, 100))
        self.draw_digit(canvas, segundos % 10, cx + 46, 20, 14, (255, 255, 100))

    def render_minimap(self, canvas):
        mx, my, mw, mh = self.width - 170, 10, 160, 120
        zoom = 1.5
        w2s = self.get_world_to_screen()
        cx, cy = w2s(
            self.barco.x + (80 * self.barco.direcao_smooth),
            self.barco.y - 70 + self.vara.profundidade_linha
        )
        cx, cy = int(cx), int(cy)
        src_w, src_h = mw // zoom, mh // zoom
        src_x = cx - src_w // 2
        src_y = cy - src_h // 2
        for dy in range(mh):
            for dx in range(mw):
                src_px = src_x + dx // zoom
                src_py = src_y + dy // zoom
                resultado = Clipping.cohen_sutherland(
                    src_px, src_py, src_px, src_py,
                    0, 0, self.width, self.height
                )
                if resultado:
                    cor = canvas.get_pixel(src_px, src_py)
                    if cor:
                        canvas.set_pixel(mx + dx, my + dy, cor)
        for x1, y1, x2, y2 in [
            (mx, my, mx+mw, my), (mx+mw, my, mx+mw, my+mh),
            (mx+mw, my+mh, mx, my+mh), (mx, my+mh, mx, my)
        ]:
            Rasterizer.draw_line(canvas, x1, y1, x2, y2, (255, 255, 255))

    def _draw_qte_bar(self, canvas, w2s):
        if not self.qte_ativo:
            return
        bx = self.width // 2
        by = self.height - 80
        bar_w = 200
        bar_h = 18
        half = bar_w // 2
        filled = int(bar_w * self.qte_progresso)
        for y in range(by, by + bar_h):
            for x in range(bx - half, bx + half):
                canvas.set_pixel(x, y, (30, 30, 30))
        if self.qte_progresso > 0.6:
            cor_barra = (50, 220, 50)
        elif self.qte_progresso > 0.3:
            cor_barra = (220, 220, 50)
        else:
            cor_barra = (220, 50, 50)
        for y in range(by, by + bar_h):
            for x in range(bx - half, bx - half + filled):
                canvas.set_pixel(x, y, cor_barra)
        Rasterizer.draw_line(canvas, bx - half, by,         bx + half, by,         (255, 255, 255))
        Rasterizer.draw_line(canvas, bx - half, by + bar_h, bx + half, by + bar_h, (255, 255, 255))
        Rasterizer.draw_line(canvas, bx - half, by,         bx - half, by + bar_h, (255, 255, 255))
        Rasterizer.draw_line(canvas, bx + half, by,         bx + half, by + bar_h, (255, 255, 255))
        pisca = (pygame.time.get_ticks() // 250) % 2 == 0
        cor_texto = (255, 255, 80) if pisca else (180, 120, 0)
        font = pygame.font.SysFont("Arial", 16, bold=True)
        surf = font.render("!! APERTE ESPACO !!", True, cor_texto)
        tx = bx - surf.get_width() // 2
        ty = by - 22
        for px in range(surf.get_width()):
            for py in range(surf.get_height()):
                pixel = surf.get_at((px, py))
                if pixel.a > 128:
                    canvas.set_pixel(tx + px, ty + py, (pixel.r, pixel.g, pixel.b))

    def _draw_fuga_msg(self, canvas):
        if self.fuga_tempo == 0:
            return
        decorrido = pygame.time.get_ticks() - self.fuga_tempo
        if decorrido > 1500:
            self.fuga_tempo = 0
            return
        font = pygame.font.SysFont("Arial", 32, bold=True)
        surf = font.render("O PEIXE FUGIU!", True, (255, 70, 70))
        tx = self.width // 2 - surf.get_width() // 2
        ty = self.height // 2 - surf.get_height() // 2
        for px in range(surf.get_width()):
            for py in range(surf.get_height()):
                pixel = surf.get_at((px, py))
                if pixel.a > 128:
                    canvas.set_pixel(tx + px, ty + py, (pixel.r, pixel.g, pixel.b))

    def render(self, canvas):
        w2s = self.get_world_to_screen()

        sky_horizon_y = int(w2s(0, 370)[1])
        sky_bands = [
            (120, 190, 255), (110, 180, 250), (100, 170, 245),
            (90,  160, 238), (80,  150, 230), (70,  138, 220),
            (60,  125, 210), (50,  112, 200),
        ]
        band_h = max(1, sky_horizon_y // len(sky_bands))
        for i, cor in enumerate(sky_bands):
            y0 = i * band_h
            y1 = y0 + band_h if i < len(sky_bands) - 1 else sky_horizon_y
            canvas.surface.fill(cor, (0, y0, self.width, y1 - y0))

        for amp, freq, speed, cor_onda in [
            (5,  0.022, 1.0,  (70, 140, 220)),
            (3,  0.038, 1.7,  (110, 175, 240)),
        ]:
            prev_sx, prev_sy = None, None
            steps = 60
            for i in range(steps + 1):
                wx = i * self.width / steps
                wy = 370 + amp * math.sin(wx * freq + self.wave_offset * speed)
                sx, sy = w2s(wx, wy)
                if prev_sx is not None:
                    Rasterizer.draw_line(canvas, int(prev_sx), int(prev_sy), int(sx), int(sy), cor_onda)
                prev_sx, prev_sy = sx, sy

        for p in self.peixes_normais:
            p.render(canvas, w2s)
        self.peixe_lendario.render(canvas, w2s)
        self.barco.render(canvas, w2s)
        self.pescador.render(canvas, w2s)
        self.vara.render(canvas, w2s)
        self.draw_hud(canvas)
        self.render_minimap(canvas)
        self._draw_qte_bar(canvas, w2s)
        self._draw_fuga_msg(canvas)
