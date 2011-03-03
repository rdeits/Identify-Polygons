class Foo(object):
    def __init__(self):
        self.x = [1,2]
    @property
    def x(self):
        print "got x"
        return self._x
    @x.setter
    def x(self,value):
        print "setting x"
        self._x = value

foo = Foo()
foo.x[0] = 5
print foo.x

