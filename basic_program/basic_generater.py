#!/usr/bin/python
# coding=utf-8

class BasicGenerater(object):
    def __init__(self):
        pass

    def __del__(self):
        print "call del"


class AdvaceGenerator(BasicGenerater):
    def __init__(self):
        pass


if __name__ == "__main__":
    basic = BasicGenerater()
    print "end"
