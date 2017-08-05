#import subprocess
#result = subprocess.run(['net', 'group VM_MEL_NEOSAT /domain'], stdout=subprocess.PIPE)
#print(result.stdout)

import os
import os.path
import model
import json

def get_users(groupname):
    g = model.Group(groupname)
    print('Build group')
    g.build()
    print('To json')
    return g.to_json_object()

def get_files(dirpath):
    d = model.Dir(dirpath)
    print('Build dir')
    d.build()
    print('To json')
    return d.to_json_object()

def get_addons(dirpath):
    pass

def produce_maestro(sparkpath):
    if not os.path.isfile(sparkpath):
        raise Exception('ERROR: Spark not found!')
    f = open(sparkpath, 'r')
    c = f.read()
    f.close()
    c = json.loads(c)
    def explore(dic):
        new = {}
        for k, v in dic.items():
            if k == '__GET_FILES__':
                print('Get files command')
                d = get_files(v)
                new.update(d)
            elif k.startswith('__GET_GROUP__'): # __GET_USERS__ : VM_MEL_NEOSAT
                print('Get users command')
                g = get_users(v)
                print('Creating key:', v)
                new[v] = g # VM_MEL_NEOSAT = { ... }
            elif type(v) == dict:
                new[k] = explore(v)
            else:
                new[k] = v
        return new
    c = explore(c)
    f = open('maestro.json', 'w')
    json.dump(c, f, indent="    ")
    f.close()

produce_maestro('maestro_spark.json')

from time import gmtime, strftime
s = strftime("%Y-%m-%d %H:%M:%S", gmtime())

print(f"End of Crawler at {s}")
