import hamill

print(hamill.__version__)

nb = 0
def display(answer):
    global nb
    nb += 1
    print(f'Test n°{nb}')
    print('---')
    s = str(answer)
    print(s)
    if len(s) > 0 and s[-1] != '\n':
        print()

def verify(answer, check, msg=None):
    display(answer)
    s = str(answer)
    if s != check:
        print(f'up: res {len(s)} chars --- down {len(check)} chars : awaited result')
        print(check)
        for i in range(min(len(s), len(check))):
            if s[i] != check[i]:
                print(i, s[i], check[i])
        if msg is not None:
            raise AssertionError("Pb on : " + str(answer))
        else:
            raise AssertionError("Pb")

# Test 1
res = hamill.process_string("**bold** ''italic''")
verify(res, "<b>bold</b> <i>italic</i>", "process_string => Bold/Italic error")

# Test 2
res = hamill.process_string("@@code@@")
verify(res, '<code><span class="normal">code</span></code>', "process_string => Code error")

# Test 3
par = """* item 1
* item 2
* item 3"""
res = hamill.process_lines(par.split('\n'))
check = """<ul>
  <li>item 1</li>
  <li>item 2</li>
  <li>item 3</li>
</ul>
"""
verify(res, check, "process_lines => List error on simple list")

# Test 4
par = """* item 1
* item 2
* * item 2.1
* * item 2.2
* item 3"""
res = hamill.process_lines(par.split('\n'))
check = """<ul>
  <li>item 1</li>
  <li>item 2
    <ul>
      <li>item 2.1</li>
      <li>item 2.2</li>
    </ul>
  </li>
  <li>item 3</li>
</ul>
"""
verify(res, check, "process_lines => List error on list inner list (same)")

# Test 5
par = """* item 1
* item 2
% % item 2.1
% % item 2.2
* item 3"""
res = hamill.process_lines(par.split('\n'))
check = """<ul>
  <li>item 1</li>
  <li>item 2
    <ol>
      <li>item 2.1</li>
      <li>item 2.2</li>
    </ol>
  </li>
  <li>item 3</li>
</ul>
"""
verify(res, check, "process_lines => List error on list inner list (mixed)")

# Test 6
par = """* item 1
* item 2 première ligne
| item 2 seconde ligne
* item 3"""
res = hamill.process_lines(par.split('\n'))
check = """<ul>
  <li>item 1</li>
  <li>item 2 première ligne
  <br>item 2 seconde ligne</li>
  <li>item 3</li>
</ul>
"""
verify(res, check, "process_lines => List error on continuity")

# Test 7
par = """{{.jumbotron}}
Je suis dans une div !
{{end}}"""
res = hamill.process_lines(par.split('\n'))
check = """<div class="jumbotron">
<p>Je suis dans une div !</p>
</div>
"""
verify(res, check, "process_lines => Div creation and class error")

# Test 8
par = """{{content-div}}
Je suis dans une div !
{{end}}"""
res = hamill.process_lines(par.split('\n'))
check = """<div id="content-div">
<p>Je suis dans une div !</p>
</div>
"""
verify(res, check, "process_lines => Div creation and ID error")

# Test 9
par = """{{red rouge}} ou {{green vert}} ou {{rien}}"""
res = hamill.process_string(par)
check = """<span class="red">rouge</span> ou <span class="green">vert</span> ou <span>rien</span>"""
verify(res, check, "process_string => Span class error")
