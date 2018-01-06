import xlrd
file_name = 'toto.xlsx'
workbook = xlrd.open_workbook(file_name, on_demand=False)
for s in workbook.sheet_names():
    print(s)
applications = {}
projects = {}
content = None
authors = None
date = None

for s in workbook.sheets():
    print(s.name)
    print(s.ncols)
    print(s.nrows)
    if s.name == "Datas":
        for col in range(0, s.ncols):
            for row in range(0, s.nrows):
                v = s.cell_value(row, col)
                print("row =", row, "col = ", col, ':', v)
                if row == 2:
                    applications[v] = 0
                if col == 0 and row in [3, 4]:
                    projects[v] = 0
    elif s.name == "Content":
        for col in range(0, s.ncols):
            for row in range(0, s.nrows):
                v = s.cell_value(row, col)
                print("row =", row, "col = ", col, ':', v)
                if v == "Content":
                    content = s.cell_value(row, col + 1)
                elif v == "Authors":
                    authors = s.cell_value(row, col + 1)
                elif v == "Date":
                    date = xlrd.xldate_as_tuple(s.cell_value(row, col + 1), workbook.datemode)

print('-----------------------------------------------------')
print("Content :", content)
print("Authors :", authors)
print("Date :", date[2], '/', date[1], '/', date[0])
print()
print('> Projects')
for name, val in projects.items():
    print('    -', name)
print('> Applications')
for name, val in applications.items():
    print('    -', name)
