class Clipping:
    """
    Implementação do Algoritmo de Cohen-Sutherland para recorte de linhas.
    Utiliza códigos binários de região (Outcodes) para determinar a visibilidade.
    """
    INSIDE = 0  # 0000
    LEFT = 1  # 0001
    RIGHT = 2  # 0010
    BOTTOM = 4  # 0100
    TOP = 8  # 1000

    @staticmethod
    def _get_region_code(x, y, xmin, ymin, xmax, ymax):
        # Define a posição relativa do ponto em relação à janela de recorte (Viewport)
        code = Clipping.INSIDE
        if x < xmin:
            code |= Clipping.LEFT
        elif x > xmax:
            code |= Clipping.RIGHT
        if y < ymin:
            code |= Clipping.BOTTOM
        elif y > ymax:
            code |= Clipping.TOP
        return code

    @staticmethod
    def cohen_sutherland(x1, y1, x2, y2, xmin, ymin, xmax, ymax):
        # Atribui códigos de região aos pontos terminais da reta
        code1 = Clipping._get_region_code(x1, y1, xmin, ymin, xmax, ymax)
        code2 = Clipping._get_region_code(x2, y2, xmin, ymin, xmax, ymax)

        while True:
            # Caso 1: Aceitação trivial (reta totalmente dentro da janela)
            if not (code1 | code2):
                return x1, y1, x2, y2

            # Caso 2: Rejeição trivial (reta totalmente fora em um mesmo semi-plano)
            if code1 & code2:
                return None

            # Caso 3: Recorte iterativo (a reta cruza os limites da janela)
            code_out = code1 if code1 != 0 else code2

            # Cálculo de interseção usando semelhança de triângulos
            if code_out & Clipping.TOP:
                x = x1 + (x2 - x1) * (ymax - y1) / (y2 - y1)
                y = ymax
            elif code_out & Clipping.BOTTOM:
                x = x1 + (x2 - x1) * (ymin - y1) / (y2 - y1)
                y = ymin
            elif code_out & Clipping.RIGHT:
                y = y1 + (y2 - y1) * (xmax - x1) / (x2 - x1)
                x = xmax
            elif code_out & Clipping.LEFT:
                y = y1 + (y2 - y1) * (xmin - x1) / (x2 - x1)
                x = xmin

            # Atualiza o ponto recortado e recalcula seu código de região
            if code_out == code1:
                x1, y1 = x, y
                code1 = Clipping._get_region_code(
                    x1, y1, xmin, ymin, xmax, ymax)
            else:
                x2, y2 = x, y
                code2 = Clipping._get_region_code(
                    x2, y2, xmin, ymin, xmax, ymax)
