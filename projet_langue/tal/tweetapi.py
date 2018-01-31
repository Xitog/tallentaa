from http.client import HTTPSConnection
from base64 import b64encode

# https://developer.twitter.com/en/docs/tweets/search/guides/build-standard-query
# https://api.twitter.com/1.1/search/tweets.json?q=%40twitterapi
# https://developer.twitter.com/en/docs/basics/authentication/overview/basic-auth
#         Authentication: Basic HTTP header
# http://docs.python-requests.org/en/master/user/authentication/
# https://pypi.python.org/pypi/requests#downloads
# https://stackoverflow.com/questions/6999565/python-https-get-with-basic-authentication
# https://stackoverflow.com/questions/14491814/httplib-invalidurl-nonnumeric-port
# https://stackoverflow.com/questions/7334199/getaddrinfo-failed-what-does-that-mean

import socket
print(socket.getaddrinfo('localhost', 80))
print('--------------------------------')

import urllib.request
s  = urllib.request.urlopen("http://damien.gouteux.free.fr").read()
print(s)

try:
    c = HTTPSConnection("http://damien.gouteux.free.fr:80")
    c.request('GET', '/')
    res = c.getresponse()
    data = res.read()
    print(data)

    print('--------------------------------')
    #This sets up the https connection
    c = HTTPSConnection("https://api.twitter.com")
    #we need to base 64 encode it 
    #and then decode it to acsii as python 3 stores it as a byte string
    password = input('>>> ')
    userAndPass = b64encode(b"damien.gouteux@gmail.com:" + password).decode("ascii")
    headers = { 'Authorization' : 'Basic %s' %  userAndPass }
    #then connect
    c.request('GET', '/1.1/search/tweets.json?q=%40twitterapi', headers=headers)
    #get the response back
    res = c.getresponse()
    # at this point you could check the status etc
    # this gets the page text
    data = res.read()
    print(data)
finally:
    pass
