# https://en.wikipedia.org/wiki/Digital_differential_analyzer_(graphics_algorithm)
try:
    import openpyxl
    from openpyxl.worksheet.write_only import WriteOnlyCell
    from openpyxl.styles import PatternFill
except ModuleNotFoundError:
    openpyxl = None
try:
    import pygame
except ModuleNotFoundError:
    pygame = None

# x = col
# y = row
class Matrix:

    def __init__(self, width, height=None, default=0):
        self.width = width
        self.height = height if height is not None else width
        self.data = []
        for x in range(0, self.width):
            self.data.append([])
            for y in range(0, self.height):
                self.data[-1].append(default)

    def set(self, x, y, v):
        self.data[x][y] = v

    def fill(self, v):
        for y in range(0, self.height):
            for x in range(0, self.width):
                self.data[x][y] = v

    def print(self):
        self.to_console()
    
    def to_console(self):
        for y in range(0, self.height):
            for x in range(0, self.width):
                print(self.data[x][y], '', end='')
            print()
    
    def to_excel(self, title="output.xlsx"):
        if openpyxl is None:
            raise Exception("Module openpyxl not available.")
        else:
            wb = openpyxl.Workbook(write_only=True)
            ws = wb.create_sheet("One")
            ws.sheet_format.defaultColWidth = 3.0
            ws.defaultRowHeight = 4.0
            fill = PatternFill("solid", fgColor="FF0000")
            for y in range(0, self.height):
                row = []
                for x in range(0, self.width):
                    cell = WriteOnlyCell(ws, value=self.data[x][y])
                    cell.fill = fill
                    row.append(cell)
                    #row.append(self.data[x][y])
                ws.append(row)
            wb.save(title)

    def to_image(self, filename="output.png", colors=None, factor=32):
        if pygame is None:
            raise Exception("Module pygame not available.")
        else:
            #pygame.init()
            pygame.font.init()
            font = pygame.font.SysFont("arial", 16)
            surf = pygame.Surface((factor * self.width, factor * self.height))
            for y in range(0, self.height):
                for x in range(0, self.width):
                    color = (255, 0, 0) if colors is None else colors[self.data[x][y]]
                    pygame.draw.rect(surf, color, (x*factor, y*factor, factor, factor), 0)
                    pygame.draw.rect(surf, (255, 255, 255), (x*factor, y*factor, factor, factor), 1)
                    tex = font.render(str(self.data[x][y]), True, (255, 255, 255))
                    surf.blit(tex, (x*factor+10, y*factor+8))
            if filename is not None: pygame.image.save(surf, filename)
            return surf
    
    def to_screen(self):
        pass


def line(start, end, filename):
    matrix = Matrix(10)
    surf = matrix.to_image(
        filename = None,
        colors = {0 : (0, 0, 0), 1 : (255, 0, 0), 2 : (0, 255, 0), 3 : (0, 0, 255), 4 : (255, 255, 0)},
        factor = 40
    )
    # real coord
    x, y = start[0], start[1]
    end_x, end_y = end[0], end[1]
    # map coord
    map_x = int(x)
    map_y = int(y)
    end_map_x = int(end_x)
    end_map_y = int(end_y)
    matrix.set(map_x, map_y, 2)
    matrix.set(end_map_x, end_map_y, 1)
    diff_x = end_x - x
    diff_y = end_y - y
    if abs(diff_x) > abs(diff_y):
        delta_x = 1 if diff_x > 0 else -1
        delta_y = diff_y / abs(diff_x)
    else:
        delta_x = diff_x / abs(diff_y)
        delta_y = 1 if diff_y > 0 else -1
    pygame.draw.rect(surf, (120, 120, 120), (map_x * 40 + 1, map_y * 40 + 1, 40 - 2, 40 - 2), 0)
    pygame.draw.circle(surf, (0, 0, 255), (int(x * 40), int(y * 40)), 5, 0)
    while map_x != end_map_x or map_y != end_map_y:
        print('------------------')
        print(f'     x = {round(x, 1):3.1f}      y = {round(y, 1):3.1f}')
        x += delta_x
        y += delta_y
        map_x = int(x)
        map_y = int(y)
        print('map x =', map_x)
        print('map y =', map_y)
        pygame.draw.rect(surf, (120, 120, 120), (map_x * 40 + 1, map_y * 40 + 1, 40 - 2, 40 - 2), 0)
        pygame.draw.circle(surf, (255, 0, 0), (int(x * 40), int(y * 40)), 5, 0)
        matrix.set(map_x, map_y, 3)
    print('------------------')
    print(f'     x = {round(x, 1):3.1f}      y = {round(y, 1):3.1f}')
    pygame.draw.circle(surf, (0, 0, 255), (int(end[0] * 40), int(end[1] * 40)), 5, 0)
    pygame.draw.line(surf, (255, 255, 0), (start[0] * 40, start[1] * 40), (end[0] * 40, end[1] * 40))
    pygame.image.save(surf, filename)


if __name__ == '__main__':
    m = Matrix(10)
    m.set(0, 0, 1)
    m.set(9, 0, 2)
    m.set(9, 9, 3)
    m.set(0, 9, 4)
    #m.print()
    #m.to_excel()
    surf = m.to_image(
        filename = "zorba.png",
        colors = {0 : (0, 0, 0), 1 : (255, 0, 0), 2 : (0, 255, 0), 3 : (0, 0, 255), 4 : (255, 255, 0)},
        factor = 40
    )
    #line(surf, m, (1.3, 2.2), (7.4, 5.7))
    line((1.3, 2.2), (6.4, 4.7), "t1.png")
    line((6.4, 4.7), (1.3, 2.2), "t2.png")
    line((1.7, 4.7), (6.7, 4.7), "t3.png")
    #m.fill(5)
    #m.print()
