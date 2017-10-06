#!/usr/bin/python
# coding=utf-8

class myArray(object):
    def __init__(self, start=1, step=1):
        self.start = start
        self.step = step
        self.changed = {}

    def __getitem__(self, key):
        try:
            return self.changed[key]
        except KeyError:
            return  self.start + key*self.step

    def __setitem__(self, key, value):
        self.changed[key] = value

if __name__ == "__main__":
    my_array = myArray()
    my_array['year'] = 50
    my_array['name'] = 'jack'

    print my_array['year'], my_array['name']