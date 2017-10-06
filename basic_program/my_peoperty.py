#!/usr/bin/python
# coding=utf-8

class MyProperty(object):
    def __init__(self):
        self._width = 0

    def set_width(self, value):
        self._width = value

    def get_width(self):
        return self._width

    w_width = property(get_width, set_width)

    def __str__(self):
        return str(self._width)

if __name__ == "__main__":
    my_array = MyProperty()
    my_array.w_width = 3
    print my_array