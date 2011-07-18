# -*- coding: utf-8; -*-

import json

def hiscore_sort(a,b):
    if a[1] < b[1]:
        return 1
    if a[1] > b[1]:
        return -1

    if a[2] > b[2]:
        return 1
    return -1

class Hiscore(object):
    def __init__(self, filename, url):
        self.local = []
        self.remote = []
        self.placement = -1
        self.filename = filename
        self.url = url
        
        try:
            fp = open(self.filename, 'r')
            self.local = json.load(fp)
            fp.close()
        except IOError:
            pass
        
        # Ensure all rows has a flag field. (for backwards compability)
        for i,x in enumerate(self.local):
            if len(x) == 3:
                self.local[i] = (x[0], x[1], x[2], 0)
    
    # Add a score to local db.
    def add(self, name, distance, time):
        result = (name, distance, time, 0)
        self.local.append(result)
        self.local.sort(cmp=hiscore_sort)
        
        # Find placement
        i = 0
        for i, (_name,_distance,_time, _flags) in enumerate(self.local):
            if _name == name and _distance == distance and _time == time:
                break
        else:
            i += 1
        self.placement = i
    
    # Save local db.
    def store(self):
        fp = open(self.filename, 'w')
        json.dump(self.local[:10], fp)
        fp.close()
    
    # Fetch score from master db.
    def fetch(self):
        pass
    
    # Push local results to master db.
    def push(self):
        pass
    
    def print_local(self):
        print '-*' * 20
        print 'Pos           Name   Dist   Time'
        for i, (_name,_distance,_time, _flags) in enumerate(self.local[:10]):
            print ' %2d %14.14s  %4dm   %3ds %s' % (i+1, _name, _distance, _time, i == self.placement and '*' or '')
        print '-*' * 20
