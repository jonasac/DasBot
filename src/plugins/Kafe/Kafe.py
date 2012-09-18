# -*- coding: utf-8 -*-
import urllib2
import time
import re
import json

class Kafe(object):
    
    def __init__(self, cafename):
        self.cafename = cafename
        self.url = 'http://dagensmiddag.net/index.json'
        self.update_offers()
        #        for cafe in self.middager['cafes']:
        #    if cafe['name'] == self.cafename:
        #        self.menu = cafe['menu']
        #        self.opening_hours = cafe['open']

    def update_offers(self):
        response = urllib2.urlopen(self.url)
        middager = json.load(response)
        self.week = int(time.strftime('%W'))
        self.weekday = int(time.strftime('%w'))
        self.db = [middager['week'], {}]
        kafeer = self.db[1]
        for cafe in middager['cafes']:
            name = cafe['name'].lower()
            kafeer[name] = {'open':self.__parse_time(cafe['open']),
                                    'menu':cafe['menu']}
            
    def __parse_time(self, tider):
        rarr = []
        for tid in tider:
            if tid == 'Stengt':
                rarr.append(tid)
            else:
                rarr.append(self.__parse_a_time(tid))
        return rarr

    def __parse_a_time(self, tid):
        return ((int(tid[0:2]),int(tid[3:5])), (int(tid[6:8]), int(tid[9:11])))

    def __compare_times(self, tid, db_tid):
        print(tid)
        tid = (int(tid[0:2]), int(tid[2:4]))
        if tid[0] == db_tid[0][0]:
            return tid[1] > db_tid[0][1]
        if tid[0] == db_tid[1][0]:
            return tid[1] < db_tid[1][1]
        return (db_tid[0][0] < tid[0]) and (db_tid[1][0] > tid[0])
            
    def __stengt(self, tid, tb_tid):
        if type(tid) == str:
            return True
        else:
            return self.__compare_times(tid, db_tid)
                
    def todaysDinner(self, kafe, check_closing=True):
        if not self.db[0] == self.week and self.weekday == int(time.strftime('%w')):
            self.update_offers()
        if kafe == None: kafe = self.cafename
        else:
            for key in self.db[1]:
                if key.startswith(kafe):
                    kafe = key
                    break;
            else:
                return (kafe, None)
                    
        if kafe in self.db[1]: 
            if check_closing and self.__stengt(time.strftime('%H%M'), self.db[1][kafe]['open'][self.weekday - 1]):
                return (kafe, "Stengt")
            else:
                return (kafe, self.make_response(self.db[1][kafe]['menu'][self.weekday - 1]))

    def make_response(self, dictionary):
        rarr = []
        for t in dictionary:
            rarr.append((t, dictionary[t][0]))
        return rarr
            
        # else:
        #     tmp = list()
        #     for dt in self.menu[self.weekday]:
        #         for j in self.menu[self.weekday][dt]:
        #             tmpstr = j.replace("     ", " ").strip(",").encode('utf-8')
        #             tmp.append(tmpstr)
        #     return tmp

if __name__ == "__main__":
    test = Kafe('Informatikkafeen')
    print test.todaysDinner(None)
    print test.todaysDinner(None, False)
    print test.todaysDinner('SV-kafeen', False)
    #print test.db
