import http.client
import xml.etree.ElementTree as etree

from enum import Enum

class JobType(Enum):
    START = 1
    STOP = 2
    CLEAN = 3
    BACKUP = 4
    UNKNOWN = 5
    IMPORT = 6

class Job:

    def __init__(self, name, url, color):
        self.name = name
        self.url = url
        self.color = color
        if self.color in ['blue_anime', 'aborted_anime', 'red_anime']:
            self.running = True
        else:
            self.running = False
        if self.color in ['blue', 'blue_anime']:
            self.last = 'ok'
        elif self.color in ['red', 'red_anime']:
            self.last = 'ko'
        elif self.color in ['aborted', 'aborted_anime']:
            self.last = 'aborted'
        if self.name.startswith('Start'):
            self.type = JobType.START
        elif self.name.startswith('Stop'):
            self.type = JobType.STOP
        elif self.name.startswith('Clean'):
            self.type = JobType.CLEAN
        elif self.name.startswith('Backup'):
            self.type = JobType.BACKUP
        elif self.name.startswith('Import'):
            self.type = JobType.IMPORT
        else:
            self.type = JobType.UNKNOWN
    
    def __str__(self):
        if self.running:
            return "%s [%s] is running" % (self.name, self.type)
        else:
            return "%s [%s] is not running" % (self.name, self.type)

def get_jobs(server, port):
    jobs = []
    url = "http://" + server + ":" + str(port) + "/api/xml"
    conn = http.client.HTTPConnection(server, port)
    conn.request("GET", url)
    r1 = conn.getresponse()
    content = r1.read()
    tree = etree.fromstring(content)
    for child in tree:
        print(child.tag)
        if child.tag == 'job':
            n = child.find('name').text
            u = child.find('url').text
            c = child.find('color').text
            j = Job(n, u, c)
            jobs.append(j)
    return jobs

list_of_jobs = get_jobs("tlmatd01", 8036)
for j in list_of_jobs:
    print(j)

exit()

start = "/view/Navigation%202137/job/Start%20Navigation/build?delay=0sec"
stop = "/view/Navigation%202137/job/Stop%20Navigation/build?delay=0sec"

conn = http.client.HTTPConnection("tlmatd01", 8036)
conn.request("GET", start)
r1 = conn.getresponse()
print(r1.status, r1.reason) # 302 Found
content = r1.read()
print(content)

if r1.status == 302 and r1.reason == "Found":
    print("Everything is fine.")

start_info = "http://tlmatd01:8036/view/Navigation%202137/job/Start%20Navigation/"
conn.request("GET", start_info)
r1 = conn.getresponse()
print(r1.status, r1.reason) # 200 OK
content = r1.read()
print(content)

# Last build (#
# Pour avoir le dernier build
# https://docs.python.org/3.4/library/http.client.html

import urllib

def launch_job(server, name):
    name_safe = urllib.quote(name)
    print(name)


