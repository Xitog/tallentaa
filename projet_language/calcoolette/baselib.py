import sys    # getsizeof, stdout.write

class BaseLib:
    
    def send(self, target, msg, par, scope):
        if target is None:
            if msg in ['println', 'writeln']:
                print par
                return None
            elif msg in ['print', 'write']:
                sys.stdout.write(str(par))
                return None
            elif msg == 'read':
                return raw_input(par)
            else:
                raise Exception("Global function not known: %s" % (msg,))
        else:
            if isinstance(target, int) and not isinstance(target, bool):
                return self.send_int(target, msg, par, scope)
            elif isinstance(target, float):
                return self.send_flt(target, msg, par, scope)
            elif isinstance(target, bool):
                return self.send_boo(target, msg, par, scope)
            elif isinstance(target, str): 
                return self.send_str(target, msg, par, scope)
    
    def send_int(self, target, msg, par, scope):
        if msg == 'add':
            return target + par
        elif msg == 'sub':
            return target - par
        elif msg == 'div':
            return target / par
        elif msg == 'mul':
            return target * par
        elif msg == 'pow':
            return target ** par
        elif msg == 'mod':
            return target % par
        elif msg == 'abs':
            return abs(target)
        elif msg == 'inv':
            return -target
        elif msg == 'lshift':
            return target << par
        elif msg == 'rshift':
            return target >> par
        elif msg == 'and':
            return target & par
        elif msg == 'or':
            return target | par
        elif msg == 'xor':
            return target ^ par
        elif msg == 'invbin':
            return ~target
        elif msg == 'cmp':
            if target > par: return 1
            elif target < par: return -1
            else: return 0
        elif msg == 'to_s':
            return str(target)
        elif msg == 'to_f':
            return float(target)
        elif msg == 'to_i':
            return target
        elif msg == 'size':
            return sys.getsizeof(target)
        else:
            raise Exception("Function %s not known for integer" % (msg,))
    
    def send_flt(self, target, msg, par, scope):
        if msg == 'add':
            return target + par
        elif msg == 'sub':
            return target - par
        elif msg == 'div':
            return target / par
        elif msg == 'mul':
            return target * par
        elif msg == 'pow':
            return target ** par
        elif msg == 'mod':
            return target % par
        elif msg == 'abs':
            return abs(target)
        elif msg == 'inv':
            return -target
        elif msg == 'round':
            return round(target)
        elif msg == 'trunc':
            return float(int(target))
        else:
            raise Exception("Function %s not known for float" % (msg,))

    def send_str(self, target, msg, par, scope):
        pass

    def send_boo(self, target, msg, par, scope):
        if msg == 'and':
            return target and par
        elif msg == 'or':
            return target or par
        elif msg == 'xor':
            return (target or par) and not (target and par)

