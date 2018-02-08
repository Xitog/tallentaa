# External libs
import xlrd
import os

class MatrixMap:
    
    def __init__(self, name, content):
        self.name = name
        self.content = content
        if content is None or not hasattr(content, '__len__') or \
            len(content) == 0 or not hasattr(content[0], '__len__') or \
            len(content[0]) == 0:
                raise Exception('Empty or malformed content')
        self.rows = len(self.content)
        self.columns = len(self.content[0])
        if hasattr(self.content[0][0], '__len__'):
            self.layers = len(self.content[0][0])
        else:
            self.layers = 1
    
    #-------
    # load
    #-------

    @staticmethod
    def load_map(dir_path, file_name, debug=False):
        print(f'Opening map file: {file_name}')
        workbook = xlrd.open_workbook(os.path.join(dir_path, file_name), on_demand=False)
        for s in workbook.sheets():
            if s.name == "ground":
                ground = s
            elif s.name == "doodad":
                doodad = s
            elif s.name == "info":
                pass
            else:
                raise Exception("Incorrect Map File: Sheet unknown: " + s.name)
        content = []
        for row in range(0, ground.nrows):
            content.append([])
            for col in range(0, ground.ncols):
                if debug:
                    print("col =", col, "row =", row)
                tex = int(ground.cell_value(row, col))
                doo = doodad.cell_value(row, col)
                doo = int(doo) if doo != '' else 0
                content[row].append([tex, doo])
        return MatrixMap(file_name, content)
    
    #-------
    # tests
    #-------
    
    def test_eq(self, val, col, row, lay=None):
        return val == self.get(col, row, lay)

    def test_eq_area(self, val, col, row, width, height, lay=None):
        for x in range(col, col + width):
            for y in range(row, row + height):
                if val != self.get(x, y, lay):
                    return False
        return True
    
    #-----
    # get
    #-----
    
    def get(self, row, col, lay=None):
        if lay is None:
            return self.content[row][col]
        else:
            return self.content[row][col][lay]
        
    #-----
    # set
    #-----
    
    def set(self, val, row, col, lay=None):
        if lay is None:
            self.content[row][col] = val
        else:
            self.content[row][col][lay] = val
    
    #----------
    # display
    #----------
    
    def dump(self):
        print(f"MatrixMap[{self.name}, columns={self.columns}, rows={self.rows}]")
        for layer in range(0, self.layers):
            print("LayerStart----------------")
            for row in range(0, self.rows):
                for col in range(0, self.columns):
                    if self.layers > 1:
                        print(self.content[row][col][layer], end=' ')
                    else:
                        print(self.content[row][col], end=' ')
                print()
            print("LayerEnd------------------")

if __name__ == '__main__':
    m = MatrixMap("The Lost Temple", [
        [11, 12, 13],
        [21, 22, 23],
        [31, 32, 33],
    ])
    m.dump()
    m = MatrixMap("The Forbidden Place", [
        [(111, 112, 113), (121, 122, 123), (131, 132, 133)],
        [(211, 212, 213), (221, 222, 223), (231, 232, 233)],
        [(311, 312, 313), (321, 322, 323), (331, 332, 333)],
    ])
    m.dump()
    m = MatrixMap("The Lonely Star", [
        [1, 2, 3, 4, 5]
    ])
    m.dump()
    for y in range(0, m.rows):
        for x in range(0, m.columns):
            print(m.get(x, y), '', end='')
        print()
    print(m.get(4, 0))
    print('Equality test 1 :', m.test_eq(5, 4, 0))
    m = MatrixMap("A Dire Situation", [
        [0, 0, 0, 1, 1],
        [0, 0, 0, 1, 1],
        [0, 0, 0, 2, 2],
    ])
    print('Equality test 2 :', m.test_eq_area(0, 0, 0, 3, 3))
    print('Equality test 3 :', m.test_eq_area(1, 3, 0, 2, 2))
    print('Equality test 4 :', m.test_eq_area(2, 3, 2, 2, 1))
        
# 4.3.0 format zip Advance a demandé

#        col = max(0, col)
#        col = min(col, self.columns - 1)
#        row = max(0, row)
#        row = min(row, self.rows - 1)
       
