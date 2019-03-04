import xlrd
wb = xlrd.open_workbook(
    r'C:\Users\etudiant\Desktop\river.xls',
    formatting_info=1)
#s = wb.sheets()[0]
s = wb.sheet_by_index(0)
print(wb.sheet_names()[0])
tex = []
uni = []
for row in range(0, s.nrows):
    cur_tex = []
    cur_uni = []
    for col in range(0, s.ncols):
        cell = s.cell(row, col)
        style = wb.xf_list[cell.xf_index]
        cur_tex.append(style.background.pattern_colour_index)
        if len(cell.value) != 0:
            cur_uni.append(cell.value)
        else:
            cur_uni.append('_')
    tex.append(cur_tex)
    uni.append(cur_uni)

for row in tex:
    for col in row:
        print(col, end=' ')
    print()

for row in uni:
    for col in row:
        print(col, end=' ')
    print()

for col in wb.colour_map:
    print(col, wb.colour_map[col])

# 10 (204, 0, 0) terre
# 48 (102, 102, 255) eau
# 50 (102, 204, 0) vert


