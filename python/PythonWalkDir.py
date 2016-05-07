import os
import time

nbfiles = 0

# Set the directory you want to start from
rootDir = '.'
for dirName, subdirList, fileList in os.walk(rootDir):
    print('Found directory: %s' % dirName)
    nbfiles += 1
    for fname in fileList:
        st = os.stat(os.path.join(dirName, fname))
        print('\tfile name :', fname)
        print('\tfile last accessed:', time.asctime(time.localtime(st.st_atime)))
        print('\tfile last modified:', time.asctime(time.localtime(st.st_mtime)))
        print('\tfile created (windows):', time.asctime(time.localtime(st.st_ctime)))
        nbfiles += 1
       
print('nb files processed:', nbfiles)
