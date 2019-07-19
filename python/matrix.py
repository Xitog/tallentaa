try:
    import openpyxl
except ModuleNotFoundError:
    openpyxl = None

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
            for y in range(0, self.height):
                row = []
                for x in range(0, self.width):
                    row.append(self.data[x][y])
                ws.append(row)
            wb.save(title)

    def to_image(self):
        if pygame is None:
            raise Exception("Module pygame not available.")
        else:
            pass
    
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
    m.fill(5)
    m.print()
