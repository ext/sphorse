# -*- coding: utf-8; -*-

import json
import httplib
import re, sys, csv, os

def hiscore_sort(a,b):
    if a[1] < b[1]:
        return 1
    if a[1] > b[1]:
        return -1

    if a[2] > b[2]:
        return 1
    return -1

class Hiscore(object):
    def __init__(self, filename, host, url, version):
        self.local = []
        self.remote = []
        self.placement = -1
        self.filename = filename
        self.host = host
        self.url = url
        self.version = version
        
        if sys.platform == 'win32':
            self.filename = self.filename[1:] # remove . (setting hidden attr instead)
        
        try:
            fp = open(self.filename, 'r')
            self.local = json.load(fp)
            fp.close()
        except IOError:
            pass
        
        # Ensure all rows has a flag field. (for backwards compability)
        for i,x in enumerate(self.local):
            if len(x) == 3:
                self.local[i] = [x[0], x[1], x[2], 0]
    
    # Add a score to local db.
    def add(self, name, distance, time):
        result = [name, distance, time, 0]
        self.local.append(result)
        self.local.sort(cmp=hiscore_sort)
    
    # Save local db.
    def store(self):
        # unhide so it can write to it (wtf windows?)
        if sys.platform == 'win32':
            os.system('attrib -h -r "%s"' % self.filename)

        fp = open(self.filename, 'w')
        json.dump(self.local[:10], fp)
        fp.close()
        
        # hide file on windows
        if sys.platform == 'win32':
            os.system('attrib +h +r "%s"' % self.filename)
    
    # Fetch score from master db.
    def fetch(self, result=None):
        connection =  httplib.HTTPConnection(self.host)
        connection.request('GET', self.url + 'hiscore.csv?limit=10')
        response = connection.getresponse()
        if response.status != 200:
            raise RuntimeError, 'HTTP %d: %s' % (response.status, response.reason)
        
        rows = response.read().split("\n")
        self.remote = [[b.decode('utf-8'),float(c),int(d), 0] for a,b,c,d in csv.reader(rows, delimiter=';', escapechar="\\")]
        
        # Find placement
        if result is not None:
            name, distance, time = result
            i = 0
            for i, (_name,_distance,_time, _flags) in enumerate(self.remote):
                if _name == name and _distance == distance and _time == time:
                    break
            else:
                i += 1
            self.placement = i
    
    # Push local results to master db.
    def push(self):
        connection =  httplib.HTTPConnection(self.host)
        for i, row in enumerate(self.local):
            name, distance, time, flags = row
            if flags & 0x01: # already sent
                continue
            
            body = '"%s";%f;%d;%s' % (re.escape(name.encode('utf-8')), distance, time, self.version)
            connection.request('PUT', self.url, body)
            response = connection.getresponse()
            response.read() # must read or next request fails
            
            if response.status != 200:
                print >> sys.stderr, "Failed to upload score (%d %s):" % (response.status, response.reason), response.read()
                continue
            
            self.local[i][3] |= 0x01
        
        # save flags
        self.store()
    
    def print_local(self):
        self.print_result(self.local, self.placement)

    def print_global(self):
        self.print_result(self.remote, self.placement)
    
    @staticmethod
    def print_result(table, placement):
        print '-*' * 20
        print 'Pos           Name   Dist   Time'
        for i, (_name,_distance,_time, _flags) in enumerate(table[:10]):
            print ' %2d %14.14s  %4dm   %3ds %s' % (i+1, _name, _distance, _time, i == placement and '*' or '')
        print '-*' * 20