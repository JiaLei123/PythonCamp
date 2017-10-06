#!/usr/bin/python
# coding=utf-8


def flatten(nested):
    for sublist in nested:
        for element in sublist:
            yield element


if __name__ == "__main__":
    nested = [[1, 2], [3, 4], [5, 6]]
    for num in flatten(nested):
        print num
