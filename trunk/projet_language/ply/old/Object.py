# Object.py
# Root object and class

obj = { 'class' : None, 'id' : None, 'doc' : None, 'init' : None, 'to_s' : None }
cls = obj.copy()
cls.update ( { 'class' : 'Class', 'name' : 'Class', 'super' : None, 'instance_members' : None } )

def make_new(cls, *par):
    print 'new :', cls['name']
    o = obj.copy()
    o.update(cls['instance_members'])
    o['class'] = cls
    if len(par) == 0 or par[0] == []:
        o['init'](o)
    else:
        print '>', o
        print '>', par
        o['init'](o, *par)
    return o

def send(obj, method, *par):
    if method in obj:
        obj[method](obj, *par)
    else:
        obj['method_missing'](obj, *par)

# Utils

def is_class(obj):
    if isinstance(obj, dict):
        if 'class' in obj:
            if obj['class'] == 'Class':
                return True
    return False
