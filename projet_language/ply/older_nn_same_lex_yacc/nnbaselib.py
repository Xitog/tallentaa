class Ref: 
    def __init__(self, name, scope): 
        self.name = name 
        self.scope = scope 
        if scope.has_key(name):  
            self.val = scope[name] 
        else: 
            self.val = None 
            scope[name] = None 
     
    def get(self): 
        return self.val 
     
    def set(self, value): 
        self.val = value 
        self.scope[self.name] = value
        return value 
     
    def __str__(self): 
        return str(self.val) 
 
def base_eval(token, scope): 
    if token.typ == 'list': 
        if token.par == 'sta': 
            r = None 
            for sta in token.sbg: 
                r = base_eval(sta, scope) 
            return r
        elif token.par == 'expr':
            l = []
            for e in token.sbg:
                l.append(base_eval(e, scope))
            return l
        elif token.par == 'dict':
            d = {}
            for e in token.sbg:
                d.update({e: base_eval(token.sbg[e], scope)})
            return d 
        else: 
            raise Exception('Par list not handled') 
    elif token.typ == 'value': 
        if token.par == 'int': 
            return int(token.sbg) 
        elif token.par == 'flt': 
            return float(token.sbg) 
        elif token.par == 'id': 
            return Ref(token.par, scope) 
        elif token.par == 'str':
            return token.sbg
        else:
            raise Exception('Value type unknown') 
    elif token.typ == 'affectation': 
        if token.par == '=':
            return base_eval(token.sbg, scope).set(base_eval(token.sbd, scope))
        else:
            var = base_eval(token.sbg, scope)
            val = base_eval(token.sbd, scope)
            if isinstance(var.get(), int):
                return var.set(base_int(var.get(), token.par.rstrip('='), val))
            elif isinstance(var.get(), float):
                return var.set(base_flt(var.get(), token.par.rstrip('='), val)) 
    elif token.typ == 'binop': 
        left = base_eval(token.sbg, scope) 
        right = base_eval(token.sbd, scope) 
        if isinstance(left, int): 
            return base_int(left, token.par, right) 
        elif isinstance(left, float): 
            return base_flt(left, token.par, right) 
        else: 
            raise Exception('Operand Type not handled %s' % (left,))
    elif token.typ == 'unaop':
        left = base_eval(token.sbg, scope)
        if isinstance(left, int):
            return base_int(left, token.par)
        elif isinstance(left, float):
            return base_flt(left, token.par) 
    else: 
        raise Exception('Token Type not handled %s' % (token.typ,)) 
 
def base_int(rec, op, *par):
    if len(par) == 0:
        if op == '-':
            return -rec 
    
    p = par[0] 
    if isinstance(p, Ref): 
        p = p.get()
     
    if op == '+': 
        return rec + p 
    elif op == '-': 
        return rec - p 
    elif op == '*': 
        return rec * p 
    elif op == '/': 
        if isinstance(p, float): 
            return float(rec) / p 
        else: 
            return int(rec / p) 
    elif op == '%': 
        return rec % p 
    elif op == '**': 
        return rec ** p 
    elif op == '//': 
        return int(rec / p)
    elif op == '>':
        return rec > p
    elif op == '<':
        return rec < p
    elif op == '>=':
        return rec >= p
    elif op == '<=':
        return rec <= p 
    elif op == '==':
        return rec == p
    elif op == '!=':
        return rec != p
 
def base_flt(rec, op, *par):
    if len(par) == 0:
        if op == '-':
            return -rec
    
    p = par[0] 
    if isinstance(p, Ref):
        p = p.get()
 
    if op == '+': 
        return rec + p 
    elif op == '-': 
        return rec - p 
    elif op == '*': 
        return rec * p 
    elif op == '/': 
        return rec / p 
    elif op == '%': 
        return rec % p 
    elif op == '**': 
        return rec ** p 
    elif op == '//': 
        return int(rec / p)
    elif op == '>':
        return rec > p
    elif op == '<':
        return rec < p
    elif op == '>=':
        return rec >= p
    elif op == '<=':
        return rec <= p
    elif op == '==':
        return rec == p
    elif op == '!=':
        return rec != p

