import pygame
import sys
import math
from core.canvas import Canvas
from core.scanline import Scanline
from core.transforms import Transforms

WIDTH, HEIGHT = 800, 600
FPS = 60


def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    canvas = Canvas(WIDTH, HEIGHT)

    # Vértices ORIGINAIS centrados na origem (0,0)
    peixe_modelo = [
        ((50, 0),   (255, 215, 0)),  # Nariz
        ((0, -30),  (255, 69, 0)),   # Topo
        ((-50, 0),  (218, 165, 32)),  # Centro/Cauda
        ((0, 30),   (255, 215, 0))   # Baixo
    ]

    angle = 0
    pos_x = 400

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        canvas.clear((10, 30, 60))

        # --- Lógica de Animação ---
        angle = (angle + 2) % 360  # Gira continuamente
        oscilacao = math.sin(pygame.time.get_ticks() *
                             0.005) * 50  # Sobe e desce

        # --- Construção da Matriz de Transformação ---
        # 1. Escala (pulsação leve)
        s = 1 + math.sin(pygame.time.get_ticks() * 0.01) * 0.1
        m_escala = Transforms.scale(s, s)

        # 2. Rotação
        m_rotacao = Transforms.rotation(angle)

        # 3. Translação (posição na tela)
        m_translac = Transforms.translation(pos_x, 300 + oscilacao)

        # Combinar: T * R * S (Ordem importa! Escala primeiro, depois gira, depois move)
        m_final = Transforms.multiply(
            m_translac, Transforms.multiply(m_rotacao, m_escala))

        # Aplicar transformação nos vértices
        peixe_transformado = []
        for pt, color in peixe_modelo:
            novo_pt = Transforms.apply(m_final, pt)
            peixe_transformado.append((novo_pt, color))

        # Desenhar
        Scanline.fill_gradient_polygon(canvas, peixe_transformado)

        screen.blit(canvas.get_surface(), (0, 0))
        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()


if __name__ == "__main__":
    main()
