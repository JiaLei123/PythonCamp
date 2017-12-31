#coding=utf-8

from argparse import ArgumentParser

if __name__=="__main__":
    parser = ArgumentParser()
    parser.add_argument('-a')
    parser.add_argument('-b')
    group_c = parser.add_mutually_exclusive_group()
    group_c.add_argument('--cd', required=True)
    group_c.add_argument('--dd', required=True)
    group_d = parser.add_mutually_exclusive_group()
    group_d.add_argument('--ee')
    group_d.add_argument('--ff')
    args = parser.parse_args()
    print args