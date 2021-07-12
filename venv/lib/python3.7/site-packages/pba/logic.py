# functions in this file act as adverbs for logic

class Logical:
    def __init__(self, left = 0,right = 1):

        if left  < 0 and left  > 1: raise TypeError
        if right < 0 and right > 1: raise TypeError

        if left < right:
            self.Left = left
            self.Right = right
        else:
            self.Left = left
            self.Right = right

    def __bool__(self):

        if self.Left == 0 and self.Right == 0:
            return False
        else:
            return True

    def __repr__(self):

        if self.Left == 0 and self.Right == 0:
            return 'False'
        elif self.Left == 1 and self.Right == 1:
            return 'True'
        else:
            return "[%g, %g]"%(self.Left,self.Right)

    __str__ = __repr__

def always(logical):
    assert logical.__class__.__name__ == 'Logical'

    if logical.Left == logical.Right == 1:
        return True
    else:
        return False

def sometimes(logical):
    assert logical.__class__.__name__ == 'Logical'

    if logical:
        # using Logical.__bool__
        return True
    else:
        return False
