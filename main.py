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
            elif escolha == "instrucoes":
                estado = "INSTRUCOES"
            elif escolha == "sair":
                running = False

        elif estado == "INSTRUCOES":
            screen.fill((10, 30, 60))
            font = pygame.font.SysFont("Arial", 22)
            titulo = pygame.font.SysFont("Arial", 28, bold=True).render("CONTROLES:", True, (255, 255, 255))
            screen.blit(titulo, (60, 50))

            controles = [
                ("Seta Esquerda / Direita", "mover barco"),
                ("Seta Cima / Baixo",       "anzol sobe/desce"),
                ("Z",                        "zoom"),
                ("ESC",                      "voltar ao menu"),
            ]
            col1_x, col2_x = 60, 340
            for i, (tecla, acao) in enumerate(controles):
                t1 = font.render(tecla, True, (200, 200, 200))
                t2 = font.render(acao, True, (255, 255, 255))
                y = 110 + i * 36
                screen.blit(t1, (col1_x, y))
                screen.blit(t2, (col2_x, y))

            pontos = [
                ("Peixe normal:",   "+10 pontos"),
                ("Peixe lendario:", "+100 pontos"),
            ]
            titulo2 = pygame.font.SysFont("Arial", 28, bold=True).render("PONTUACAO:", True, (255, 255, 255))
            screen.blit(titulo2, (60, 280))
            for i, (nome, pts) in enumerate(pontos):
                t1 = font.render(nome, True, (200, 200, 200))
                t2 = font.render(pts, True, (255, 255, 0))
                y = 325 + i * 36
                screen.blit(t1, (col1_x, y))
                screen.blit(t2, (col2_x, y))

            rodape = font.render("Pressione qualquer tecla para voltar", True, (180, 180, 180))
            screen.blit(rodape, (60, 500))
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                    estado = "MENU"

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
