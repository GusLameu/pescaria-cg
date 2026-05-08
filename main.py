import pygame
import sys
from core.canvas import Canvas
from game.simulation import Simulation
import menu

WIDTH, HEIGHT = 800, 600
FPS = 60


def main():
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
                sim = Simulation(WIDTH, HEIGHT)
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
                ("ESPACO",                  "capturar peixe lendario (QTE)"),
                ("Z",                       "zoom"),
                ("ESC",                     "voltar ao menu"),
            ]
            col1_x, col2_x = 60, 340
            for i, (tecla, acao) in enumerate(controles):
                cor_tecla = (255, 220, 50) if tecla == "ESPACO" else (200, 200, 200)
                cor_acao  = (255, 220, 50) if tecla == "ESPACO" else (255, 255, 255)
                t1 = font.render(tecla, True, cor_tecla)
                t2 = font.render(acao, True, cor_acao)
                y = 110 + i * 36
                screen.blit(t1, (col1_x, y))
                screen.blit(t2, (col2_x, y))

            pontos = [
                ("Peixe normal:",   "+10 pontos"),
                ("Peixe lendario:", "+100 pontos  (requer QTE)"),
            ]
            titulo2 = pygame.font.SysFont("Arial", 28, bold=True).render("PONTUACAO:", True, (255, 255, 255))
            screen.blit(titulo2, (60, 305))
            for i, (nome, pts) in enumerate(pontos):
                cor_pts = (255, 200, 0) if i == 1 else (255, 255, 0)
                t1 = font.render(nome, True, (200, 200, 200))
                t2 = font.render(pts, True, cor_pts)
                y = 350 + i * 36
                screen.blit(t1, (col1_x, y))
                screen.blit(t2, (col2_x, y))

            dica = pygame.font.SysFont("Arial", 18).render(
                "* Ao fisgar o lendario, aperte ESPACO varias vezes para encher a barra!", True, (180, 220, 255))
            screen.blit(dica, (col1_x, 430))

            rodape = font.render("Pressione qualquer tecla para voltar", True, (180, 180, 180))
            screen.blit(rodape, (60, 500))
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                    estado = "MENU"

        elif estado == "JOGANDO":
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        estado = "MENU"
                    elif event.key == pygame.K_SPACE:
                        sim.tentar_capturar_lendario()

            sim.update()

            if sim.tempo_acabou():
                estado = "FIM_JOGO"

            canvas.clear((10, 30, 60))
            sim.render(canvas)
            screen.blit(canvas.get_surface(), (0, 0))
            pygame.display.flip()

        elif estado == "FIM_JOGO":
            screen.fill((10, 30, 60))

            font_titulo = pygame.font.SysFont("Arial", 48, bold=True)
            titulo = font_titulo.render("FIM DE JOGO", True, (255, 200, 0))
            titulo_rect = titulo.get_rect(center=(WIDTH // 2, 80))
            screen.blit(titulo, titulo_rect)

            font_grande = pygame.font.SysFont("Arial", 64, bold=True)
            pontos_text = font_grande.render(str(sim.pontuacao), True, (100, 255, 100))
            pontos_rect = pontos_text.get_rect(center=(WIDTH // 2, 220))
            screen.blit(pontos_text, pontos_rect)

            font_label = pygame.font.SysFont("Arial", 28)
            label = font_label.render("PONTOS", True, (200, 200, 200))
            label_rect = label.get_rect(center=(WIDTH // 2, 310))
            screen.blit(label, label_rect)

            font_small = pygame.font.SysFont("Arial", 20)
            instrucoes = font_small.render("Pressione ESPACO para voltar ao menu", True, (180, 180, 180))
            instrucoes_rect = instrucoes.get_rect(center=(WIDTH // 2, 450))
            screen.blit(instrucoes, instrucoes_rect)

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE or event.key == pygame.K_RETURN:
                        estado = "MENU"
                        sim = Simulation(WIDTH, HEIGHT)

        clock.tick(FPS)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
