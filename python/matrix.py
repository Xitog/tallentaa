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

    def to_image(self, title="output.png"):
        if pygame is None:
            raise Exception("Module pygame not available.")
        else:
            #pygame.init()
            pygame.font.init()
            font = pygame.font.SysFont("arial", 16)
            surf = pygame.Surface((32 * self.width, 32 * self.height))
            for y in range(0, self.height):
                for x in range(0, self.width):
                    pygame.draw.rect(surf, (255, 0, 0), (x*32, y*32, 32, 32), 2)
                    tex = font.render(str(self.data[x][y]), True, (255, 255, 255))
                    surf.blit(tex, (x*32+10, y*32+8))
            pygame.image.save(surf, title)
    
    def to_screen(self):
        pass


if __name__ == '__main__':
    m = Matrix(10)
    m.set(0, 0, 1)
    m.set(9, 0, 2)
    m.set(9, 9, 3)
    m.set(0, 9, 4)
    m.print()
    m.to_excel()
    m.to_image("zorba.png")
    m.fill(5)
    m.print()
