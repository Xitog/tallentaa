# Language:
#   Special chars for classes:
#       \a = alpha
#       \d = digit
#       \w = alpha + digit + _
#   Special chars for repeatability/optionality:
#       * repeat (0, n)
#       + repeat (1, n)
#       ? repeat (0, 1)
#   Escape special chars:
#       \? = a true ?
#       \* = a true *
#       \+ = a true +

# Ajout fonctionnel par rapport à mon langage du mémoire :
# - la répétabilité
# Suppression :
# - le groupement dans les choix, on ne peut pas faire [ (A B) C ]

# Changement technique :
# On ne déploie plus le patron
# Avant on le dépliait : [A B] C? D
#   A D
#   B D
#   A C D
#   B C D
# Maintenant on fait tout avec une boucle


#-------------------------------------------------
# This class handles the core of the Regex
# It compiles from a pattern (a simple string)
#-------------------------------------------------

class Regex:

    def __init__(self, pattern, debug):
        self.pattern = pattern
        self.debug = debug
        self.val = []
        self.repeat = []
        self.compile()
        # evaluate where the optionality start in order to be able to determine the completness of matching
        self.start_of_completness = len(self.val)
        inv_cpt = len(self.val) - 1
        while self.optionnal(inv_cpt):
            self.start_of_completness = inv_cpt
            inv_cpt -= 1

    def __str__(self):
        return f"Regex |{self.pattern}| (len={len(self)} (min={self.start_of_completness})"

    def __repr__(self):
        return f"Regex |{self.pattern}|"
    
    def compile(self):
        if self.debug:
            print('[re] regex :', self.pattern)
        index = 0
        while index < len(self.pattern):
            c = self.pattern[index]
            if c == '[': # choice
                if self.debug:
                    print('[re] choice :', c, '@', index, '/', len(self.pattern))
                sub = []
                sub_index = index + 1
                if sub_index >= len(self.pattern):
                    raise Exception("Uncomplete choice [")
                c = self.pattern[sub_index]
                while c != ']':
                    if c == '\\': # special in choice
                        if self.debug:
                            print('    [re] special in choice :', c, '@', sub_index, '/', len(self.pattern))
                        if sub_index + 1 < len(self.pattern):
                            cnext = self.pattern[sub_index + 1]
                            if cnext not in ['a', 'd', 'w', '?', '*', '+']:
                                raise Exception("Incorrect special char: \\" + cnext)
                            else:
                                if cnext in ['?', '*', '+']:
                                    sub.append(cnext)
                                else:
                                    sub.append(c + cnext)
                                sub_index += 2
                        else:
                            raise Exception("Unfinished special char")
                    elif c == '[': # no choice allowed in choice
                        raise Exception("No choice in choice")
                    elif c in ['*', '+', '?']: # no repeat in choice
                        raise Exception("No repeat in choice")
                    else: # normal
                        if self.debug:
                            print('    [re] normal in choice :', c, '@', sub_index, '/', len(self.pattern))
                        sub.append(c)
                        sub_index += 1
                    if sub_index < len(self.pattern):
                        c = self.pattern[sub_index]
                    else:
                        raise Exception("Uncomplete choice [")
                if len(sub) < 2:
                    raise Exception("Choice with one or zero element: not a choice")
                self.val.append(sub)
                index = sub_index + 1
            elif c == '\\': # special
                if self.debug:
                    print('[re] special :', c, '@', index, '/', len(self.pattern))
                if index + 1 < len(self.pattern):
                    cnext = self.pattern[index + 1]
                if cnext not in ['a', 'd', 'w', '?', '*', '+']:
                    raise Exception("Incorrect special char: \\" + cnext)
                else:
                    if cnext in ['?', '*', '+']:
                        self.val.append(cnext)
                    else:
                        self.val.append(c + cnext)
                    index += 2
            elif c in ['*', '+', '?']:
                while len(self.repeat) < len(self.val):
                    self.repeat.append(False)
                if len(self.repeat) == 0:
                    raise Exception(c + " without something to repeat. Did you miss to escape?")
                self.repeat[-1] = c
                index += 1
            else:
                if self.debug:
                    print('[re] normal :', c, '@', index, '/', len(self.pattern))
                self.val.append(c)
                index += 1
        while len(self.repeat) < len(self.val):
            self.repeat.append(False)
        if self.debug:
            index = 0
            print('[re] content of ' + self.pattern)
            while index < len(self.val):
                print('   [re] ', self.val[index], self.repeat[index])
                index += 1

    def check_at(self, char, index, choice=None):
        #print(char, index, choice)
        if choice is None:
            if index >= len(self.val):
                return False
            elem = self.val[index]
        else:
            if choice >= len(self.val[index]):
                return False
            elem = self.val[index][choice]
        if type(elem) == list: # choice
            res = False
            for i in range(0, len(elem)):
                res = self.check_at(char, index, i)
                if res:
                    break
        elif elem[0] == '\\': # special char
            if elem == '\\a':
                res = (char.isalpha())
            elif elem == '\\d':
                res = (char.isdigit())
            elif elem == '\\w':
                res = (char.isalnum() or char == '_')
            else:
                raiseException("Incorrect special char: " + elem)
        else: # normal char
            res = (char == elem)
        return res

    def complex(self):
        for r in self.repeat:
            if r in ['+', '*']: return True
        return False
    
    def optionnal(self, index):
        if index >= len(self.repeat):
            return False
        return self.repeat[index] in ['?', '*']

    def repeatable(self, index):
        if index >= len(self.repeat):
            return False
        return self.repeat[index] in ['+', '*']

    def __len__(self):
        return len(self.val)


#-------------------------------------------------
# This class handles the course of the Regex
# keeping an index of the actual element
#-------------------------------------------------

class Parcours:

    NO = 0
    MAYBE = 1
    COMPLETE = 2

    @staticmethod
    def p2s(v):
        if v == Parcours.NO:
            return 'NO'
        elif v == Parcours.MAYBE:
            return 'MAYBE'
        elif v == Parcours.COMPLETE:
            return 'COMPLETE'
        else:
            raise Exception('Value unknown for Parcours result:' + str(v))
    
    def __init__(self, regex, index=0):
        self.regex = regex
        self.index = index
        self.result = Parcours.MAYBE
        self.nb = 0

    def __str__(self):
        return f"{str(self.regex)}[{self.index}]"

    def __repr__(self):
        return f"{repr(self.regex)}[{self.index}]"
    
    def test(self, c):
        res = self.regex.check_at(c, self.index)
        # on est pas bon
        if res == False:
            # si on est pas bon mais qu'il est optionnel (? ou *)
            # si on est pas bon mais qu'on peut passer au suivant (+ car * a été traité avant)
            if self.regex.optionnal(self.index) or (self.regex.repeatable(self.index) and self.nb > 0):
                # on regarde celui d'après s'il existe
                if self.index + 1 < len(self.regex):
                    self.index += 1
                    res = self.test(c)
                else:
                    res = Parcours.NO
            else:
                res = Parcours.NO
        # on est bon
        else:
            self.nb += 1
            if not self.regex.repeatable(self.index):
                self.index += 1
                index_to_test = self.index
            else:
                index_to_test = self.index + 1
            if index_to_test >= self.regex.start_of_completness:
                res = Parcours.COMPLETE
            else:
                res = Parcours.MAYBE
        return res

#-------------------------------------------------
# Tests
#-------------------------------------------------

tests = (
    (r"[\a_]\w*", 2,
         (
             ("_a15", True),
         )
     ),
    ("abc", 3,
         (
             ("zor", False),
             ("ab", False),
             ("abc", True),
         )
     ),
    (r"\d", 1,
         (
             ("15", False),
             ("1", True),
         )
     ),
    (r"\d+", 1,
         (
             ("15", True),
             ("1", True),
         )
     ),
    (r"[\a_]\w*[\?!]?", 3,
         (
             ("_a15", True),
             ("4a", False),
             ("_isalpha?", True),
         )
     ), 
)

#-------------------------------------------------
# Running the tests if we are main
#-------------------------------------------------

if __name__ == '__main__':
    for t in tests:
        print('-----------------------')
        regex = Regex(t[0], False) #True)
        print(str(regex), " awaiting ", t[1], " elements", sep='', end='')
        assert len(regex) == t[1], t[0] + " length is not equal to = " + str(len(regex))
        print(' -> ok')
        for match in t[2]:
            candidate = match[0]
            result = match[1]
            p = Parcours(regex)
            res = Parcours.NO
            for letter in candidate:
                res = p.test(letter)
                if res == Parcours.NO:
                    break
            if res in [Parcours.NO, Parcours.MAYBE]:
                if not result:
                    print('    OK    comparing |', candidate, '| to regex, no match found (parcours is: ', Parcours.p2s(res), ')', sep='')
                else:
                    print('    ERROR comparing |', candidate, '| to regex, no match found (parcours is: ', Parcours.p2s(res), ') one was expected', sep='')
            else:
                if result:
                    print('    OK    comparing |', candidate, '| to regex, match found (parcours is: ', Parcours.p2s(res), ')', sep='')
                else:
                    print('    ERROR comparing |', candidate, '| to regex, match found (parcours is: ', Parcours.p2s(res), ') none was expected', sep='')

