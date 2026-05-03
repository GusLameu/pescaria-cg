class Scanline:
    @staticmethod
    def fill_polygon(canvas, vertices, color):
        """
        Preenche um polígono qualquer definido por uma lista de vértices [(x, y), ...].
        """
        if not vertices:
            return

        # 1. Encontrar os limites verticais (Y min e Y max)
        y_coords = [v[1] for v in vertices]
        y_min = int(min(y_coords))
        y_max = int(max(y_coords))

        # 2. Iterar por cada linha horizontal (scanline)
        for y in range(y_min, y_max + 1):
            intersections = []

            # 3. Encontrar interseções com as arestas do polígono
            for i in range(len(vertices)):
                p1 = vertices[i]
                # Próximo vértice (fecha o polígono)
                p2 = vertices[(i + 1) % len(vertices)]

                # Verifica se a scanline y cruza a aresta entre p1 e p2
                if (p1[1] <= y < p2[1]) or (p2[1] <= y < p1[1]):
                    # Cálculo da interseção no eixo X (regra da semelhança de triângulos)
                    # x = x1 + (y - y1) * (x2 - x1) / (y2 - y1)
                    intersect_x = p1[0] + (y - p1[1]) * \
                        (p2[0] - p1[0]) / (p2[1] - p1[1])
                    intersections.append(intersect_x)

            # 4. Ordenar as interseções da esquerda para a direita
            intersections.sort()

            # 5. Preencher os pixels entre pares de interseções
            for i in range(0, len(intersections), 2):
                if i + 1 < len(intersections):
                    x_start = int(intersections[i])
                    x_end = int(intersections[i+1])
                    for x in range(x_start, x_end + 1):
                        canvas.set_pixel(x, y, color)

    @staticmethod
    def _interpolate_color(c1, c2, t):
        """Auxiliar para interpolar entre duas cores RGB com proteção de limites."""
        # Garante que t esteja entre 0 e 1
        t = max(0, min(1, t))

        r = int(c1[0] * (1 - t) + c2[0] * t)
        g = int(c1[1] * (1 - t) + c2[1] * t)
        b = int(c1[2] * (1 - t) + c2[2] * t)

        # Garante que os valores fiquem entre 0 e 255 e sejam inteiros
        r = max(0, min(255, r))
        g = max(0, min(255, g))
        b = max(0, min(255, b))

        return (r, g, b)

    @staticmethod
    def fill_gradient_polygon(canvas, vertices_with_colors):
        """
        Preenche um polígono com gradiente.
        vertices_with_colors: lista de tuplas [((x, y), (r, g, b)), ...]
        """
        if not vertices_with_colors:
            return

        # 1. Limites verticais
        y_coords = [v[0][1] for v in vertices_with_colors]
        y_min, y_max = int(min(y_coords)), int(max(y_coords))

        for y in range(y_min, y_max + 1):
            intersections = []

            for i in range(len(vertices_with_colors)):
                p1, c1 = vertices_with_colors[i]
                p2, c2 = vertices_with_colors[(
                    i + 1) % len(vertices_with_colors)]

                # Verifica se a scanline y cruza a aresta
                if (p1[1] <= y < p2[1]) or (p2[1] <= y < p1[1]):
                    # Fração da distância vertical percorrida (t)
                    t_y = (y - p1[1]) / (p2[1] - p1[1])

                    # Interpolação do X e da Cor na borda
                    intersect_x = p1[0] + t_y * (p2[0] - p1[0])
                    intersect_color = Scanline._interpolate_color(c1, c2, t_y)

                    intersections.append((intersect_x, intersect_color))

            # 2. Ordena interseções pelo X
            intersections.sort(key=lambda x: x[0])

            # 3. Preenchimento horizontal com interpolação
            for i in range(0, len(intersections), 2):
                if i + 1 < len(intersections):
                    x_start, color_start = intersections[i]
                    x_end, color_end = intersections[i+1]

                    x_start_int, x_end_int = int(x_start), int(x_end)

                    for x in range(x_start_int, x_end_int + 1):
                        if x_end_int != x_start_int:
                            t_x = (x - x_start) / (x_end - x_start)
                        else:
                            t_x = 0

                        # Adicione esta linha para garantir que o t_x não saia de [0, 1]
                        t_x = max(0, min(1, t_x))

                        pixel_color = Scanline._interpolate_color(
                            color_start, color_end, t_x)
                        canvas.set_pixel(x, y, pixel_color)
