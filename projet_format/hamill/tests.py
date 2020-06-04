import hamill
import locale
import datetime

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
                print('>>>', i, s[i], check[i])
        if msg is not None:
            raise AssertionError("Pb on : " + str(answer))
        else:
            raise AssertionError("Pb")

# Test 1
res = hamill.process_string("**bold** ''italic'' __underline__ --strike-- ^^super^^")
verify(res, "<b>bold</b> <i>italic</i> <u>underline</u> <s>strike</s> <sup>super</sup>", "process_string => Bold/Italic error")

# Test 2
res = hamill.process_string("@@code@@")
verify(res, '<code><span class="TokenType.NORMAL">code</span></code>', "process_string => Code error")

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
verify(res, check, "process_lines => List error on simple list unordered")

# Test 4
par = """+ item 1
+ item 2
+ item 3"""
res = hamill.process_lines(par.split('\n'))
check = """<ol>
  <li>item 1</li>
  <li>item 2</li>
  <li>item 3</li>
</ol>
"""
verify(res, check, "process_lines => List error on simple list ordered")

# Test 5
par = """- item 1
- item 2
- item 3"""
res = hamill.process_lines(par.split('\n'))
check = """<ol reversed>
  <li>item 1</li>
  <li>item 2</li>
  <li>item 3</li>
</ol>
"""
verify(res, check, "process_lines => List error on simple list ordered reversed")

# Test 6
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

# Test 7
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

# Test 8
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

# Test 9
par = """{{.jumbotron}}
Je suis dans une div !
{{end}}"""
res = hamill.process_lines(par.split('\n'))
check = """<div class="jumbotron">
<p>Je suis dans une div !</p>
</div>
"""
verify(res, check, "process_lines => Div creation with class error")

# Test 10
par = """{{#content-div}}
Je suis dans une div !
{{end}}"""
res = hamill.process_lines(par.split('\n'))
check = """<div id="content-div">
<p>Je suis dans une div !</p>
</div>
"""
verify(res, check, "process_lines => Div creation with ID error")

# Test 11
par = """{{#content-div .jumbotron}}
Je suis dans une div !
{{end}}"""
res = hamill.process_lines(par.split('\n'))
check = """<div id="content-div" class="jumbotron">
<p>Je suis dans une div !</p>
</div>
"""
verify(res, check, "process_lines => Div creation with ID and class error")

# Test 12
par = """{{.red rouge}} ou {{.green vert}} ou {{rien}}"""
res = hamill.process_string(par)
check = """<span class="red">rouge</span> ou <span class="green">vert</span> ou <span>rien</span>"""
verify(res, check, "process_string => Span class error")

# Test 13
par = """{{.signature}}ceci est une signature"""
res = hamill.process_lines([par])
check = """<p class="signature">ceci est une signature</p>\n"""
verify(res, check, "process_lines => Paragraph creation with class error")

# Test 14
par = """{{#signature}}ceci est une signature"""
res = hamill.process_lines([par])
check = """<p id="signature">ceci est une signature</p>\n"""
verify(res, check, "process_lines => Paragraph creation with ID error")

# Test 15
par = """{{#signid .signclass}}ceci est une signature"""
res = hamill.process_lines([par])
check = """<p id="signid" class="signclass">ceci est une signature</p>\n"""
verify(res, check, "process_lines => Paragraph creation with ID and class error")

# Test 16 Direct link to URL
par = """[>https://pipo.html]"""
res = hamill.process_lines([par])
check = """<p><a href="https://pipo.html">https://pipo.html</a></p>
"""
verify(res, check, "Direct link to URL => Error")

# Test 17 Direct link to REF
par = """[>REF]
[REF]: https://zembla.org"""
res = hamill.process_lines(par.split('\n'))
check = """<p><a href="https://zembla.org">REF</a></p>
"""
verify(res, check, "Direct link to REF => Error")

# Test 18 Named link to URL
par = """[pipo->https://pipo.html]"""
res = hamill.process_lines([par])
check = """<p><a href="https://pipo.html">pipo</a></p>
"""
verify(res, check, "Named link to URL => Error")

# Test 19 Named link to REF
par = """[this is a REF->REF]
[REF]: https://zembla.org"""
res = hamill.process_lines(par.split('\n'))
check = """<p><a href="https://zembla.org">this is a REF</a></p>
"""
verify(res, check, "Named link to REF => Error")

# Test 20 Named link to TITLE through #
par = """[this goes to a title->#]
# This goes to a title"""
res = hamill.process_lines(par.split('\n'))
check = """<p><a href="#this-goes-to-a-title">this goes to a title</a></p>
<h1 id="this-goes-to-a-title">This goes to a title</h1>
"""
verify(res, check, "Named link to TITLE through # => Error")

# Test 21 Not a link 1
par = """https://pipo.html"""
res = hamill.process_lines([par])
check = """<p>https://pipo.html</p>
"""
verify(res, check, "Not a link 1 => Error")

# Test 22 Not a link 2
par = """>https://pipo.html"""
res = hamill.process_lines([par])
check = """<p>&gt;https://pipo.html</p>
"""
verify(res, check, "Not a link 2 => Error")

# Test 23 List and direct link
par = """* [>https://pipo.html]"""
res = hamill.process_lines([par])
check = """<ul>
  <li><a href="https://pipo.html">https://pipo.html</a></li>
</ul>
"""
verify(res, check, "List and direct link => Error")

# Test 24 Title transformation
par = """## Les jeux"""
res = hamill.process_lines([par])
check = """<h2 id="les-jeux">Les jeux</h2>
"""
verify(res, check, "Title transformation => Error")

# Test 25 display a constant (English date) in process_string
par = "This text has been generated on [=GENDATE]"
res = hamill.process_string(par, hamill.Generation(default_lang='en'))
dt = datetime.datetime.now().strftime('%d %B %Y')
check = f"This text has been generated on {dt}"
verify(res, check, "Output English gendate from process_string => Error")

# Test 26 display a constant (French date) in process_string
par = "Ce texte a été généré le [=GENDATE]"
res = hamill.process_string(par, hamill.Generation(default_lang='fr'))
try:
    locale.setlocale(locale.LC_TIME, 'fr_FR.UTF-8')
except locale.Error:
    locale.setlocale(locale.LC_TIME, '')
dt = datetime.datetime.now().strftime('%d %B %Y')
check = f"Ce texte a été généré le {dt}"
verify(res, check, "Output French gendate from process_string => Error")

# Test 27 display a constant (French date) in process_lines
par = "Ce texte a été généré le [=GENDATE]"
res = hamill.process_lines([par], hamill.Generation(default_lang='fr'))
try:
    locale.setlocale(locale.LC_TIME, 'fr_FR.UTF-8')
except locale.Error:
    locale.setlocale(locale.LC_TIME, '')
dt = datetime.datetime.now().strftime('%d %B %Y')
check = f"<p>Ce texte a été généré le {dt}</p>\n"
verify(res, check, "Output French gendate from process_lines => Error")


