import pygame


class Canvas:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        # Criamos uma superfície vazia onde os pixels serão desenhados
        self.surface = pygame.Surface((width, height))

    def set_pixel(self, x, y, color):
        """
        Usa a função set_at nativa do PyGame, que é estritamente uma função set_pixel.
        """
        x, y = int(x), int(y)

        # O Clipping garante que não tentaremos pintar fora da tela, o que causaria erro
        if 0 <= x < self.width and 0 <= y < self.height:
            self.surface.set_at((x, y), color)

    def get_pixel(self, x, y):
        """
        Lê a cor de um pixel usando a função nativa get_at.
        Útil para a futura implementação do Flood Fill.
        """
        x, y = int(x), int(y)
        if 0 <= x < self.width and 0 <= y < self.height:
            color = self.surface.get_at((x, y))
            return (color.r, color.g, color.b)
        return None

    def clear(self, color=(0, 0, 0)):
        """Preenche a superfície com uma cor de fundo."""
        self.surface.fill(color)

    def get_surface(self):
        """Retorna a superfície para o PyGame exibir na tela."""
        return self.surface
