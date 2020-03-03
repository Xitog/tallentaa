f = open('editor.py', mode='r', encoding='utf8')
content = f.readlines()
f.close()

class Method:
    def __init__(self, name):
        self.name = name
        self.calls = []

methods = {}

for line in content:
    line = line.strip()
    if line.startswith('def') and line.endswith(':'):
        name = line[4:-1]
        methods[name] = Method(name)

#for line in content:
#   if line.index('(') != -1:
#       print(line)

for m in methods:
    print(m)

print(f'Number of methods: {len(methods)}')
