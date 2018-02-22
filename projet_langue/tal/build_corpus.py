import urllib.request
import urllib.parse
import json

# 23h53 Yes!
base_request = "https://api.archives-ouvertes.fr/search/?wt=json&fl=docid,domain_s,authFullName_s,docType_s,title_s,language_s,modifiedDateY_i&fq=language_s:fr&indent=true&sort=docid%20desc&rows=100&cursorMark="
nb = 310 #1
request = base_request + 'AoFXtZUG' #'*'
try:
    while nb < 3100:
        print(f'call {nb:04d}', request)
        response = urllib.request.urlopen(request)
        raw_content = response.read()
        content = json.loads(raw_content)
        del raw_content
        if 'nextCursorMark' not in content:
            print('nextCursorMark not found!')
            if 'error' in content:
                print(content['error'])
            #[print(key) for key in content]
            break
        print(f'answer {nb:04d}', content['nextCursorMark'], len(content['response']['docs']))
        request = base_request + urllib.parse.quote(content['nextCursorMark'])
        output_file = open(f'output_{nb:04d}.txt', mode='w', encoding='utf8')
        json.dump(content, output_file, indent=4, ensure_ascii=False)
        output_file.close()
        nb += 1
except urllib.error.URLError as e:
    print('Impossible to reach the server:')
    print(f'    {e.reason}')

"""
with urllib.request.urlopen(first_request) as response:
"""

"""
import socket

def safe_addrinfo(r, port=80):
    try:
        a = socket.getaddrinfo(r, port)
    except socket.gaierror as e:
        print('Impossible to reach the server:')
        print(f'    {e}')
    if 'a' in locals():
        return a

a = safe_addrinfo('www.api.archives-ouverts.fr', 8080)
print(a)
a = safe_addrinfo('www.intranet.peopleonline.corp.thales/portal/')
print(a)

a = json.loads('[1,2,3,4]')
print(a[3])
a = json.loads('{"a" : "b"}')
print(a['a'])
"""

# Hum... j'ai un [Errno 11004] getaddrinfo failed
# https://docs.python.org/3.6/howto/urllib2.html
# https://docs.python.org/3.6/library/json.html
# https://stackoverflow.com/questions/7334199/getaddrinfo-failed-what-does-that-mean
# https://stackoverflow.com/questions/37469680/gaierror-errno-11004-getaddrinfo-failed?rq=1

"""
try:
    mysock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    mysock.connect(('www.pythonlearn.com', 80))
except:
    pass

a = safe_addrinfo('tlmatd01', 8036) # 15h40 YES! ça marche.
print(a) # [(<AddressFamily.AF_INET: 2>, 0, 0, '', ('172.16.4.143', 8036))]
"""
