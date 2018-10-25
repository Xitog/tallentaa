definitions = {
    'KEYWORD' : ['if', 'then', 'else', 'end', 'while', 'do', 'for',
                 'break', 'next', 'return',
                 'var', 'fun', 'sub', 'get', 'set', 'class',
                 'import', 'from', 'as',
                 'try', 'catch', 'finally', 'raise'],
    'BOOLEAN_LITTERAL' : ['false', 'true'],
    'NIL_LITTERAL' : ['nil'], 
    'BINARY_OPERATOR' : ['and', 'or', # boolean
                  'in', # belongs to
                  '+', '-', '*', '/', '//', '**', '%', # mathematical
                  '&', '|', '~', '>>', '<<', # bitwise
                  '<', '<=', '>', '>=', '==', '!=', # comparison
                  '.'], # call
    'AFFECTATION' : ['='],
    'COMBINED_AFFECTATION' : ['+=', '-=', '*=', '/=', '//=', '**=', '%='],
    'TYPE' : [':', '->'],
    'FAST' : ['=>'],
    'LABEL' : ['::'],
    'UNARY_OPERATOR' : ['-', 'not', '#', '~'],
    'NEWLINE' : ['\n'],
    'INTEGER' : [r'[\d]+'],
    'IDENTIFIER' : [r'[\w_][\w_\d]*'],
    'COMMENT' : ['--'],
    }

definitions = {
    'KEYWORD' : ['bonjour', 'bon'],
    'IDENTIFIER' : [r'\u\w+'],
    'MONOID' : [r'\u'], # because \w+ is no OPTIONNAL in the previous
    'INTEGER' : ['08789'],
    'ALL_INTEGER' : [r'\d+'],
    'OPERATOR' : ['+', '+='],
    'NEWLINE' : ['\n'],
    'WRONGINT' : [r'\d+\w+'], #
    }

# \u : alpha ou _
# \w : alpha, digit ou _ (standard)
# \a : alpha
# \d : digit (standard)

texte = 'bonjour 08789 b2974 0b01111 breaka break'
texte = 'bonjour bon bonjour 08789 22 abc + += a+b \n c _d 2a2'
#texte = '22'
#texte = 'abc'
#texte = '2a2'
#texte = 'a+b'

class TokenDef:

    NO = -1
    MAYBE = 0
    EXACT = 1
    
    def __init__(self, typ, val, debug=False):
        self.typ = typ
        self.val = val
        self.i = 0
        self.nb = 0
        self.debug = debug
        self.regex = False
        if r'\d' in val or r'\w' in val or r'\a' in val or r'\u' in val:
            self.regex = True
            self.val = []
            self.repeat = []
            index = 0
            while index < len(val):
                c = val[index]
                if c == '\\':
                    if index + 1 >= len(val):
                        raise Exception('Malformed Regex :', val)
                    element = c + val[index + 1]
                    self.val.append(element)
                    if index + 2 < len(val) and val[index + 2] in ['+']:
                        self.repeat.append('+')
                        index += 1
                    else:
                        self.repeat.append(False)
                    index += 1
                else:
                    self.val.append(c)
                index += 1
            if debug:
                print('Val =', self.val)
    
    def __str__(self):
        if self.regex:
            return f"{self.typ} {self.val} [REGEX]"
        else:
            return f"{self.typ} {self.val}"

    def __repr__(self):
        return str(self)
    
    def reset(self):
        self.i = 0
        self.nb = 0

    def test_regex(self, c):
        if self.debug:
            print('Test for ', str(self), ' : |', c, '| i = ', self.i, '/', len(self.val), sep='', end=' ')
        if self.i >= len(self.val):
            if self.debug:
                print('not a match (too short)')
            res = TokenDef.NO
        else:
            val = self.val[self.i]
            if val == r'\a' and c.isalpha():
                if len(self.val)-1 == self.i:
                    res = TokenDef.EXACT
                else:
                    res = TokenDef.MAYBE
            elif val == r'\u' and (c.isalpha() or c == '_'):
                if len(self.val)-1 == self.i:
                    res = TokenDef.EXACT
                else:
                    res = TokenDef.MAYBE
            elif val == r'\w' and (c.isalpha() or c.isdigit() or c == '_'):
                if len(self.val)-1 == self.i:
                    res = TokenDef.EXACT
                else:
                    res = TokenDef.MAYBE
            elif val == r'\d' and c.isdigit():
                if len(self.val)-1 == self.i:
                    res = TokenDef.EXACT
                else:
                    res = TokenDef.MAYBE
            else:
                if self.debug:
                    print('not a match')
                res = TokenDef.NO
        # repeat or not
        if res == TokenDef.NO:
            if self.i < len(self.val) and self.repeat[self.i] and self.i + 1 < len(self.val): #memorize repeated at least once
                # pour +, on doit y être passé au moins une fois
                if self.repeat[self.i] == '+' and self.nb > 0:
                    self.i += 1
                    res = self.test_regex(c)
                    return res
                else:
                    res = TokenDef.NO
        else:
            self.nb += 1
            if not self.repeat[self.i]:
                self.i += 1
                self.nb = 0
        # result
        if self.debug:
            if res == TokenDef.EXACT:
                print('exact match')
            else: #res == TokenDef.MAYBE
                print('maybe a match')
        return res
    
    def test(self, c): # -1 : not, 0 : maybe, 1 : exact
        if self.regex:
            return self.test_regex(c)
        if self.debug:
            if self.i < len(self.val):
                print('Test for ', str(self), ' : |', c, '| vs ', self.val[self.i], sep='', end=' ')
            else:
                print('Test for ', str(self), ' : |', c, '| (too short : ', self.i, ' vs ', len(self.val), ')', sep='', end=' ')
        if self.i >= len(self.val):
            res = -1
        elif c == self.val[self.i]:
            if len(self.val)-1 == self.i:
                res = TokenDef.EXACT
            else:
                res = TokenDef.MAYBE
                self.i += 1
        else:
            res = TokenDef.NO
        if self.debug:
            if res == TokenDef.EXACT:
                print('exact match')
            elif res == TokenDef.MAYBE:
                print('maybe a match')
            else:
                print('not a match')
        return res


class Token:

    def __init__(self, typ, val):
        self.typ = typ
        self.val = val
    
    def __str__(self):
        return f"{self.typ} |{self.val}|"

    def __repr__(self):
        return str(self)


class Lexer:

    def __init__(self, definitions, debug=False):
        self.debug = debug
        self.tokendefs = []
        for typ, values in definitions.items():
            for val in values:
                self.tokendefs.append(TokenDef(typ, val, self.debug))
        if self.debug:
            print('----------------------------------------')
            print('Types :', len(definitions))
            print('Token definitions :', len(self.tokendefs))
            print('----------------------------------------')
            for tokdef in self.tokendefs:
                print(tokdef)
            print('----------------------------------------')
    
    def lex(self, texte):
        if texte[-1] != '\0':
            texte += '\0'
        def_ok = []
        index = 0
        tokens = []
        for tokdef in self.tokendefs:
            def_ok.append((tokdef, TokenDef.MAYBE))
        current = ''
        nb = 0
        # La boucle principale, on va parcourir le texte, un caractère à la fois
        # On stocke le caractère actuel dans C, son index dans INDEX
        # NB compte le nombre de tour fait
        while index < len(texte):
            c = texte[index]
            if self.debug:
                print('Nb = ', nb, ' Index = ', index, ' Char = ', c, ' PrevCurrent = |', current, '| --------------------------', sep='')
            next_ok = []
            # Pour tous les définitions de tokens DEF_OK qui sont exact ou maybe au tour d'avant,
            # on restest. On ne retient dans NEXT_OK que les tokens qui sont toujours exact ou maybe.
            # Maybe signifie "c'est potentiellement un début de mon définition de token".
            for tokdef, val in def_ok:
                val = tokdef.test(c)
                if val >= 0:
                    next_ok.append((tokdef, val))
            if self.debug:
                print('NEXT:', next_ok)
                print('PREV:', def_ok)
            # On regarde ensuite si on toujours du monde dans NEXT_OK
            # Si non, y'a un problème : la séquence actuelle (stockée dans current) ne correspond à rien !
            # On regarde alors si, au tour d'avant dans les DEF_OK, il y avait une correspondance.
            if len(next_ok) == 0:
                if len(def_ok) == 0:
                    # S'il y en a pas, c'est peut-être un espace, dans ce cas-là on passe.
                    # S'il y en a pas et que ce n'est pas un espace, on a trouvé un token inconnu.
                    if c.isspace() or c == '\0':
                        print('**whitespace (no prev)')
                        current = ''
                    else:
                        print(c)
                        raise Exception("Unknown token")
                else:
                    # Sinon, on filtre sur ceux qui ont un match EXACT
                    # On filtre également les EXACT étant des REGEX.
                    # En effet, si la séquence actuelle correspond à plusieurs définitions,
                    # mais dans ces définitions une seule n'est pas une REGEX, alors c'est celle-ci.
                    # Ex : "if" est captée à la fois comme l'IDENTIFIER \w+ et comme le KEYWORD if.
                    # On privilégie cette dernière définition car elle est plus fine
                    exact_filtered = list(filter(lambda elem: elem[1] == TokenDef.EXACT, def_ok))
                    regex_removed = list(filter(lambda elem: elem[0].regex == False, exact_filtered))
                    if self.debug:
                        print('    Exact filtered:', exact_filtered)
                        print('    Regex removed:', regex_removed)
                    if len(exact_filtered) == 1 or len(regex_removed) == 1:
                        if len(exact_filtered) == 1:
                            tok = Token(exact_filtered[0][0].typ, current)
                        else: # regex_removed == 1
                            tok = Token(regex_removed[0][0].typ, current)
                        if self.debug:
                            print('**producing:', tok)
                        tokens.append(tok)
                        # On fait un reset de DEF_OK en disant que toutes les définitions sont MAYBE,
                        # on fait un rest de la séquence actuelle et
                        # <IMPORTANT> on revient d'un dans notre parcours : INDEX -= 1 </IMPORTANT>
                        current = ''
                        def_ok = []
                        for tokdef in self.tokendefs:
                            tokdef.reset()
                            def_ok.append((tokdef, TokenDef.MAYBE))
                        index -= 1                        
                    else:
                        if (c.isspace() or c == '\0') and len(current) == 0:
                            if self.debug:
                                print('**whitespace (with prev)')
                            current = ''
                        else:
                            if len(exact_filtered) == 0:
                                raise Exception("No choice for " + current)
                            else:
                                raise Exception("Too many choices for " + current)
            else:
                def_ok = next_ok
                current += c
            # On avance dans l'INDEX et dans le NB, le nombre de tour
            # INDEX peut être manipulé pour revenir en arrière :
            #   si on prend un caractère qui n'appartient pas à la définition courante
            # NB ne peut être manipulé, il ne fait qu'augmenter de un à chaque tour
            index += 1
            nb += 1
        if self.debug:
            print('----------------------------------------')
            print('Tokens :', len(tokens))
            print('----------------------------------------')
            for tok in tokens:
                print(tok)
            if len(tokens) > 0:
                print('----------------------------------------')
        return tokens

lexer = Lexer(definitions, debug=True) # False
print('Language')
for tokdef in lexer.tokendefs:
    print('   ', tokdef)
print('Texte =', texte)
tokens = lexer.lex(texte)
for tok in tokens:
    print('   ', tok)

