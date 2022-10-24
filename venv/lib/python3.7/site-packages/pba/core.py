from typing import *
if __name__ is not None and "." in __name__:
    from .interval import *
else:
    from interval import Logical, Interval


def env(x,y):
    if x.__class__.__name__ == 'Pbox':
        return x.env(y)
    elif y.__class__.__name__ == 'Pbox':
        return y.env(x)
    else:
        raise NotImplementedError('At least one argument needs to be a Pbox')

def min(x,y):
    if x.__class__.__name__ == 'Pbox':
        return x.min(y)
    if y.__class__.__name__ == 'Pbox':
        return y.min(x)
    else:
        raise NotImplementedError('At least one argument needs to be a Pbox')

def max(x,y):
    if x.__class__.__name__ == 'Pbox':
        return x.max(y)
    if y.__class__.__name__ == 'Pbox':
        return y.max(x)
    else:
        raise NotImplementedError('At least one argument needs to be a Pbox')

def always(logical: Logical) -> bool:

    if logical.__class__.__name__ != 'Logical':
        return logical
    if logical.left == 1 and logical.right == 1:
        return True
    else:
        return False


def sometimes(logical: Logical) -> bool:

    if logical.__class__.__name__ != 'Logical':
        return logical

    elif logical.left == 1 or logical.right == 1:
        return True
    else:
        return False

def xtimes(logical: Logical) -> bool:
    '''
    exclusive sometimes
    
    Returns true if the logical function is sometimes True but not always true
    If the input is not a Logical class then function will always return false
    '''

    if logical.__class__.__name__ != 'Logical':
        return False

    elif logical.left ^ logical.right:
        return True
    else:
        return False

def sum(l: Union[list,tuple] ,method = 'f'):
    '''
    Allows the sum to be calculated for intervals and p-boxes
    
    Parameters
    ----------
        l : list of pboxes or intervals
        method : pbox addition method to be used
    
    Output
    ------
        sum of interval or pbox objects within l
    
    '''
    s = 0
    for o in l:
        if o.__class__.__name__ == 'Pbox':
            s = o.add(s,method = method)
        else:
            s += o
    return s

def mean(l: Union[list,tuple] ,method = 'f'):
    '''    
    Allows the sum to be calculated for intervals and p-boxes
    
    Parameters
    ----------
        l : list of pboxes or intervals
        method : pbox addition method to be used
    
    Output
    ------
        mean of interval or pbox objects within l
    
    '''
    s = sum(l,method = method)
    
    return s/len(l)

def mul(*args, method = None):
    for i,arg in enumerate(args):
        if i == 0:
            n = arg
        elif n.__class__.__name__ == 'Interval':
            if arg.__class__.__name__ == 'Interval':
                if method is None:
                    n *= arg
                elif method == 'p':
                    n = n.pmul(arg)
                elif method == 'o':
                    n = n.omul(arg)
                else:
                    raise Exception(f"Method {method} unknown for Interval * Interval calculation")
            elif arg.__class__.__name__ == 'Pbox':
                n = arg.mul(n,method = method)
            else:
                n *= arg
        elif n.__class__.__name__ == 'Pbox':
            if method is None:
                n *= arg
            else:
                n = n.mul(arg,method = method)
        else:
            n *= arg
    return n
                