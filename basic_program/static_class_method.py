#!/usr/bin/python
# coding=utf-8

class MyMethod(object):
    def __str__(self):
        self.name = 'jack'

    @staticmethod
    def print_self():
        print "this is a static method"

    @classmethod
    def print_class(cls):
        print "this is a class method", cls


if __name__ == "__main__":
    MyMethod.print_self()
    MyMethod.print_class()
