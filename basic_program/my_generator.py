#!/usr/bin/python
# coding=utf-8


def flatten(nested):
    for sublist in nested:
        for element in sublist:
            yield element


def flatten_recursion(nested):
    try:
        for sublist in nested:
            for element in flatten_recursion(sublist):
                yield element
    except TypeError:
        yield nested


if __name__ == "__main__":
    nested = [[1, 2], [3, 4], [5, 6]]
    for num in flatten(nested):
        print num

    nested_1 = [[1], 2, [[3, 4, [5, 6]], 7, 8], 9]
    for num_1 in flatten_recursion(nested_1):
        print num_1
