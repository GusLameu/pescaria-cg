# main.py

import pygame
import sys
import math
from core.canvas import Canvas
from core.scanline import Scanline
from core.transforms import Transforms
from core.constants import gerar_textura_procedural, PEIXE_MODELO_UV, COR_MAR
from core.menu import main as menu_main

WIDTH, HEIGHT = 800, 600
FPS = 60


def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Motor Gráfico 2D - Jogo de Pesca")
    clock = pygame.time.Clock()

    while True:
        # Executa o menu inicial
        choice = menu_main(screen)

        if choice == "iniciar":
            break  # Sai do loop do menu e inicia o jogo
        elif choice == "comandos":
            # Mostra comandos (simples por enquanto)
            screen.fill((0,0,0))
            font = pygame.font.SysFont("Arial", 24)
            text = font.render("Comandos: Use as teclas para jogar. Pressione ESPAÇO para voltar.", True, (255,255,255))#informar as teclas do jogo
            screen.blit(text, (50, 300))
            pygame.display.update()
            waiting = True
            while waiting:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                        waiting = False
        elif choice == "sair":
            pygame.quit()
            sys.exit()

    canvas = Canvas(WIDTH, HEIGHT)

    # 1. Pré-processamento: Gera a matriz de textura uma única vez
    textura_matriz = gerar_textura_procedural(64)

    angle = 0
    pos_x = 400

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Limpa o fundo do mar importado das constantes
        canvas.clear(COR_MAR)

        # --- Lógica de Animação ---
        angle = (angle + 2) % 360
        oscilacao = math.sin(pygame.time.get_ticks() * 0.005) * 50
        s = 1 + math.sin(pygame.time.get_ticks() * 0.01) * 0.1

        # --- Matrizes de Transformação ---
        m_escala = Transforms.scale(s, s)
        m_rotacao = Transforms.rotation(angle)
        m_translac = Transforms.translation(pos_x, 300 + oscilacao)

        m_final = Transforms.multiply(
            m_translac, Transforms.multiply(m_rotacao, m_escala))

        # --- Pipeline de Vértices ---
        peixe_transformado_uv = []
        for pt, uv in PEIXE_MODELO_UV:
            # Aplica a transformação APENAS nas coordenadas (x, y)
            novo_pt = Transforms.apply(m_final, pt)
            # Mantém a coordenada (u, v) original atrelada ao novo ponto
            peixe_transformado_uv.append((novo_pt, uv))

        # --- Renderização ---
        # Desenha usando a função procedural que lê a nossa matriz gerada
        Scanline.fill_textured_polygon_procedural(
            canvas, peixe_transformado_uv, textura_matriz)

        screen.blit(canvas.get_surface(), (0, 0))
        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
