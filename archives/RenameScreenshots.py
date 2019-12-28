import os
import os.path
import time

doublon = []
for c in os.listdir('Change'):
    filepath_old = os.path.join('Change', c)
    s = time.strftime('Torment %Y-%m-%d-%H-%M-%S', time.localtime(os.path.getctime(filepath_old)))
    if s in doublon:
        raise Exception('Doublon !')
    else:
        doublon.append(s)
    filepath_new = os.path.join('Change', s + '.png')
    os.rename(filepath_old, filepath_new)
    print('Done :', filepath_old, 'to', filepath_new)

# https://docs.python.org/3/library/time.html#time.gmtime
# https://stackoverflow.com/questions/237079/how-to-get-file-creation-modification-date-times-in-python
# https://fr.ulule.com/biographie-gygax/news/
# http://www.sycko-fab.com/
# https://fr.ulule.com/designers/#comments
# https://www.evilhat.com/home/designers-dragons-1980s/
# https://datatofish.com/rename-file-python/
# os.rename(old, new)

