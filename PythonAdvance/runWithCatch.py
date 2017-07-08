#coding=utf-8
from memoized import memoized

class TestClassA:
    def __init__(self):
        pass

    @memoized
    def testA(self, word):
        print (word)
        return word + "\n"

    @memoized
    def testB(self, *args, **kwargs):
        print args
        print kwargs
        return "ABC"


if __name__=="__main__":
    a = "test1"
    b = "test2"
    test = TestClassA()
    print "return value for test1 is " + test.testA(a)
    print "return value for test1 is " + test.testA(a)
    print "return value for test2 is " + test.testA(b)
    print "return value for test1 is "     + test.testA(a)

    c = test.testB(key='name', value='jialei')
    print 'first invoke' + c
    d = test.testB(key='name', value='jialei')
    print 'second invoke' + d
