import regex

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
                  r'\+', '-', r'\*', '/', '//', r'\*\*', '%', # mathematical
                  '&', '|', '~', '>>', '<<', # bitwise
                  '<', '<=', '>', '>=', '==', '!=', # comparison
                  '.'], # call
    'AFFECTATION' : ['='],
    'COMBINED_AFFECTATION' : [r'\+=', '-=', r'\*=', '/=', '//=', r'\*\*=', '%='],
    'TYPE' : [':', '->'],
    'FAST' : ['=>'],
    'LABEL' : ['::'],
    'UNARY_OPERATOR' : ['-', 'not', '#', '~'],
    'NEWLINE' : ['\n'],
    'INTEGER' : [r'\d+'],
    'IDENTIFIER' : [r'[\a_][\w_\d]*'],
    'COMMENT' : ['--'],
    'WRONGINT' : [r'\d+\w+'], #
    }

definitionsTEST = {
    'KEYWORD' : ['bonjour', 'bon'],
    'IDENTIFIER' : [r'[\a_]\w*'],
    #'MONOID' : [r'[\a_]'], # because \w+ is no OPTIONNAL in the previous
    'INTEGER' : ['08789'],
    'ALL_INTEGER' : [r'\d+'],
    'OPERATOR' : ['\+', '\+='],
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
    
    def __init__(self, typ, pattern, debug=False):
        self.typ = typ
        self.regex = regex.Regex(pattern, debug)
    
    def __str__(self):
        return f"{self.typ} {self.regex}"

    def __repr__(self):
        return str(self)


class ParcoursTokenDef:

    def __init__(self, tokdef):
        self.tokdef = tokdef
        self.inner = regex.Parcours(tokdef.regex)

    def test(self, c):
        return self.inner.test(c)

    def __str__(self):
        return str(self.inner)
    
    def __repr__(self):
        return repr(self.inner)

    def complex(self):
        return self.tokdef.regex.complex()

    def typ(self):
        return self.tokdef.typ


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
            def_ok.append((ParcoursTokenDef(tokdef), regex.Parcours.MAYBE))
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
                if val > regex.Parcours.NO:
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
                    exact_filtered = list(filter(lambda elem: elem[1] == regex.Parcours.COMPLETE, def_ok))
                    regex_removed = list(filter(lambda elem: not elem[0].complex(), exact_filtered))
                    if self.debug:
                        print('    Exact filtered:', exact_filtered)
                        print('    Regex removed:', regex_removed)
                    if len(exact_filtered) == 1 or len(regex_removed) == 1:
                        if len(exact_filtered) == 1:
                            tok = Token(exact_filtered[0][0].typ(), current)
                        else: # regex_removed == 1
                            tok = Token(regex_removed[0][0].typ(), current)
                        if self.debug:
                            print('**producing:', tok)
                        tokens.append(tok)
                        # On fait un reset de DEF_OK en disant que toutes les définitions sont MAYBE,
                        # on fait un rest de la séquence actuelle et
                        # <IMPORTANT> on revient d'un dans notre parcours : INDEX -= 1 </IMPORTANT>
                        current = ''
                        def_ok = []
                        for tokdef in self.tokendefs:
                            def_ok.append((ParcoursTokenDef(tokdef), regex.Parcours.MAYBE))
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
