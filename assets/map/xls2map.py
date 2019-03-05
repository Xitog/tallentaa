import xlrd
wb = xlrd.open_workbook(
    '2019_03_04_river.xls',
    formatting_info=1)
#s = wb.sheets()[0]
s = wb.sheet_by_index(0)
print(wb.sheet_names()[0])
tex = []
uni = []
fnt = []
for row in range(0, s.nrows):
    cur_tex = []
    cur_uni = []
    cur_fnt = []
    for col in range(0, s.ncols):
        cell = s.cell(row, col)
        style = wb.xf_list[cell.xf_index]
        # Récupération du fond de la cellule
        cur_tex.append(style.background.pattern_colour_index)
        if len(cell.value) != 0:
            # Récupération du texte de la cellule
            cur_uni.append(cell.value)
            # Récupération de la couleur de la font
            font = wb.font_list[style.font_index]
            cur_fnt.append(font.colour_index)
        else:
            cur_uni.append('_')
            cur_fnt.append('    0')
    tex.append(cur_tex)
    uni.append(cur_uni)
    fnt.append(cur_fnt)

for row in tex:
    for col in row:
        print(col, end=' ')
    print()

for row in uni:
    for col in row:
        print(col, end=' ')
    print()

for row in fnt:
    for col in row:
        print(col, end=' ')
    print()

for col in wb.colour_map:
    print(col, wb.colour_map[col])

# Attention, les index changent avec les couleurs qu'on ajoute !

# 16 (204, 0, 0) terre
# 48 (102, 102, 255) eau
# 50 (102, 204, 0) vert

# 10 (255, 0, 0) rouge des unités
# 12 (0, 0, 204) bleu des unités

