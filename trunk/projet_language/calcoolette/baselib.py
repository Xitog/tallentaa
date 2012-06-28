import sys

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
            if isinstance(target, int):
                return self.send_int(target, msg, par, scope)
            elif isinstance(target, float):
                return self.send_flt(target, msg, par, scope)
      
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
        else:
            raise Exception("Function not known for integer")
    
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
        else:
            raise Exception("Function not known for float")
