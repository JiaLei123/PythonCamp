#!/usr/bin/python
# coding=utf-8

class BasicGenerater(object):
    def __init__(self):
        self.first_name = 'Jack'
        self.last_name = 'Freeman'

    def my_name(self):
        print '.'.join((self.first_name, self.last_name))

    def __del__(self):
        print "call del"


class AdvaceGenerator(BasicGenerater):
    def __init__(self):
        BasicGenerater.__init__(self)
        self.first_name = 'Bob'


class AdvaceGenerator2(BasicGenerater):
    def __init__(self):
        super(AdvaceGenerator2, self).__init__()
        self.first_name = 'Alon'


if __name__ == "__main__":
    basic = AdvaceGenerator2()
    basic.my_name()
    print "end"
