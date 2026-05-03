import collections


class Rasterizer:
    @staticmethod
    def draw_line(canvas, x0, y0, x1, y1, color):
        """Algoritmo de Bresenham para retas."""
        x0, y0, x1, y1 = int(x0), int(y0), int(x1), int(y1)
        dx = abs(x1 - x0)
        dy = abs(y1 - y0)
        sx = 1 if x0 < x1 else -1
        sy = 1 if y0 < y1 else -1
        err = dx - dy

        while True:
            canvas.set_pixel(x0, y0, color)
            if x0 == x1 and y0 == y1:
                break
            e2 = 2 * err
            if e2 > -dy:
                err -= dy
                x0 += sx
            if e2 < dx:
                err += dx
                y0 += sy

    @staticmethod
    def draw_circle(canvas, xc, yc, r, color):
        """Algoritmo do Ponto Médio para circunferências."""
        xc, yc, r = int(xc), int(yc), int(r)
        x = 0
        y = r
        d = 1 - r

        def draw_circle_points(xc, yc, x, y, color):
            # Simetria de 8 pontos
            canvas.set_pixel(xc + x, yc + y, color)
            canvas.set_pixel(xc - x, yc + y, color)
            canvas.set_pixel(xc + x, yc - y, color)
            canvas.set_pixel(xc - x, yc - y, color)
            canvas.set_pixel(xc + y, yc + x, color)
            canvas.set_pixel(xc - y, yc + x, color)
            canvas.set_pixel(xc + y, yc - x, color)
            canvas.set_pixel(xc - y, yc - x, color)

        draw_circle_points(xc, yc, x, y, color)
        while x < y:
            if d < 0:
                d += 2 * x + 3
            else:
                d += 2 * (x - y) + 5
                y -= 1
            x += 1
            draw_circle_points(xc, yc, x, y, color)

    @staticmethod
    def draw_ellipse(canvas, xc, yc, rx, ry, color):
        """Algoritmo do Ponto Médio para elipses."""
        xc, yc, rx, ry = int(xc), int(yc), int(rx), int(ry)
        x = 0
        y = ry

        # Região 1
        d1 = (ry**2) - (rx**2 * ry) + (0.25 * rx**2)
        dx = 2 * ry**2 * x
        dy = 2 * rx**2 * y

        def draw_ellipse_points(xc, yc, x, y, color):
            # Simetria de 4 pontos
            canvas.set_pixel(xc + x, yc + y, color)
            canvas.set_pixel(xc - x, yc + y, color)
            canvas.set_pixel(xc + x, yc - y, color)
            canvas.set_pixel(xc - x, yc - y, color)

        while dx < dy:
            draw_ellipse_points(xc, yc, x, y, color)
            if d1 < 0:
                x += 1
                dx += 2 * ry**2
                d1 += dx + ry**2
            else:
                x += 1
                y -= 1
                dx += 2 * ry**2
                dy -= 2 * rx**2
                d1 += dx - dy + ry**2

        # Região 2
        d2 = ((ry**2) * ((x + 0.5)**2)) + \
            ((rx**2) * ((y - 1)**2)) - (rx**2 * ry**2)
        while y >= 0:
            draw_ellipse_points(xc, yc, x, y, color)
            if d2 > 0:
                y -= 1
                dy -= 2 * rx**2
                d2 += rx**2 - dy
            else:
                y -= 1
                x += 1
                dx += 2 * ry**2
                dy -= 2 * rx**2
                d2 += dx - dy + rx**2

    @staticmethod
    def flood_fill(canvas, x, y, fill_color):
        """Preenchimento Flood Fill usando Pilha (Stack)."""
        target_color = canvas.get_pixel(x, y)
        if target_color == fill_color:
            return

        stack = [(int(x), int(y))]

        while stack:
            curr_x, curr_y = stack.pop()

            if canvas.get_pixel(curr_x, curr_y) == target_color:
                canvas.set_pixel(curr_x, curr_y, fill_color)

                # Adiciona vizinhos (4-conectividade)
                if curr_x + 1 < canvas.width:
                    stack.append((curr_x + 1, curr_y))
                if curr_x - 1 >= 0:
                    stack.append((curr_x - 1, curr_y))
                if curr_y + 1 < canvas.height:
                    stack.append((curr_x, curr_y + 1))
                if curr_y - 1 >= 0:
                    stack.append((curr_x, curr_y - 1))
