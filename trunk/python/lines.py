#-----------------------------------------------------------------------

# JesuScript : a complete micro-language

#-----------------------------------------------------------------------

import sys # puts

keywords = ['while', 'end', 'if', 'begin']
operators= ['=']

def puts(*suite):
    for elem in suite:
        sys.stdout.write(elem)
    sys.stdout.write('\n')

#-----------------------------------------------------------------------

class Context:
  def __init__(self):
    pass

#-----------------------------------------------------------------------

class Executable:
  def display(self,level=0):
    pass
  def do(self):
    pass
  def space(self,level):
    s = ''
    for i in range(0,level*2):
      s += ' '
    return s
  
#-----------------------------------------------------------------------

class Block(Executable):
  def __init__(self, father):
    self.father = father
    self.executables = []
    self.kind = None
  
  def append(self, l):
    self.executables.append(l)
  
  def display(self,level=0):
    puts(self.space(level), 'Block of %d executables <%s>:' % (len(self.executables), self.kind))
    for ex in self.executables:
      ex.display(level+2)
  
  def guess(self):
    if len(self.executables)>0:
      if isinstance(self.executables[0], Block):
        self.kind = 'EnclosingBlock'
      elif isinstance(self.executables[0], Line):
        self.kind = self.executables[0].kind

#-----------------------------------------------------------------------

class Line(Executable):
  def __init__(self, raw):
    self.raw = raw
    self.tokens = []
    self.tokenize()
    self.kind = self.guess()
  
  def display(self, level=0):
    puts(self.space(level), '"%s" [%d tokens] <%s>' % (self.raw, len(self.tokens), self.kind))
    for t in self.tokens:
      t.display(level+2)
  
  def tokenize(self):
    w = ''
    i = 0
    for c in self.raw:
      #print i, c, w, len(self.raw)
      if c != ' ':
        w += c
        if i+1 == len(self.raw):
          self.tokens.append(Token(w))
      else:
        self.tokens.append(Token(w))
        w = ''
      i+=1
    #print len(self.tokens)
  
  def guess(self):
    if len(self.tokens) >= 1:
      if self.tokens[0] == 'while':
        return 'WHILE'
      elif self.tokens[0] == 'if':
        return 'IF'
      elif self.tokens[0] == 'end':
        return 'END'
      elif self.tokens[0] == 'begin':
        return 'BEGIN'
      if len(self.tokens) >= 2:
        if self.tokens[1] == '=':
          return 'AFFECTATION'
        else:
          return 'EXPRESSION'
      else:
        return 'EXPRESSION'
    else:
      return 'EMPTY'
  
  def block(self):
    if self.guess() in ['WHILE', 'IF', 'BEGIN']:
      return 1 # open
    elif self.guess() == 'END':
      return -1 # close
    else:
      return 0 # go on

#-----------------------------------------------------------------------

class Token(Executable):
  def __init__(self, raw):
    self.raw = raw
    self.kind = None
    self.guess()
  
  def guess(self):
    global keywords
    global operators
    if self.raw in keywords:
      self.kind = 'KEYWORDS'
    elif self.raw in operators:
      self.kind = 'OPERATORS'
    else:
      self.kind = 'IDENTIFIER'
  
  def display(self, level=0):
    puts(self.space(level), '%s <%s>' % (self.raw, self.kind))

#-----------------------------------------------------------------------

escape = False
prompt = '>>> '
lines = []
root = Block(None)
current = root

while not escape:
  r = raw_input(prompt)
  if r != 'exit':
    l=Line(r)
    lines.append(l)
    block = l.block()
    #print block
    if block == 0:
      current.append(l)
    elif block == -1:
      current.append(l)
      current.guess()
      if current.father == None:
        raise Exception('Block closure without block')
      current.father.append(current)
      current = current.father
    elif block == 1:
      current = Block(current)
      current.append(l)
  else:
    escape = True

print
print '%d lines:' % (len(lines),)
root.display()

#for l in lines:
#  print 'svg: %s [%d tokens] <%s>' % (l.raw, len(l.tokens), l.kind)
#  for t in l.tokens:
#    print '\t %s' % (t,)

