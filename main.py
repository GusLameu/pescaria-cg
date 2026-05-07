import pygame
import sys
from core.canvas import Canvas
from game.simulation import Simulation
import menu

WIDTH, HEIGHT = 800, 600
FPS = 60


def main():
    # 1. Inicialização do Pygame e do Canvas
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Pescaria CG")
    clock = pygame.time.Clock()

    canvas = Canvas(WIDTH, HEIGHT)

    sim = Simulation(WIDTH, HEIGHT)

    estado = "MENU"

    running = True
    while running:
        if estado == "MENU":
            escolha = menu.main(screen)

            if escolha == "iniciar":
                estado = "JOGANDO"
            elif escolha == "sair":
                running = False
            else:
                pass

        elif estado == "JOGANDO":
            # --- LÓGICA DE ENTRADA ---
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        estado = "MENU"  # Volta para o menu ao apertar ESC

            # --- ATUALIZAÇÃO (LOGICA) ---
            sim.update()

            # --- RENDERIZAÇÃO (DESENHO) ---
            # Limpa o canvas com a cor do mar profundo (Azul Marinho)
            canvas.clear((10, 30, 60))

            # Desenha todas as entidades (peixes, barco, pescador, anzol e HUD)
            sim.render(canvas)

            # Transfere o que foi pintado no Canvas para a tela do Pygame
            screen.blit(canvas.get_surface(), (0, 0))
            pygame.display.flip()

        # Mantém a taxa de quadros estável
        clock.tick(FPS)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
