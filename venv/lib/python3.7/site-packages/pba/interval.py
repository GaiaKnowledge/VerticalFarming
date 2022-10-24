# -*- coding: utf-8 -*-

import numpy as np
import random as r


__all__ = ['Interval','I','Logical']

class Interval:
    """
    An interval is an uncertain number for which only the endpoints are known, for example if :math:`x=[a,b]`
    then this can be interpreted as :math:`x` being between :math:`a` and :math:`b` but with no more information about the value of :math:`x`.
    
    Intervals can be created using::
        pba.I(left,right)
        pba.Interval(left,right)
        
    Parameters
    ----------
    left : numeric
        left side of interval
    right : numeric
        right side of interval
        
    Attributes
    ----------
    left : numeric
        left side of interval
    right : numeric
        right side of interval

    """
    def __init__(self,left = None, right = None):


        # kill complex nums
        assert not isinstance(left, np.complex) or not isinstance(right, np.complex), "Inputs must be real numbers"

        # assume vaccous if no inputs
        if left is None and right is None:
            right = np.inf
            left = -np.inf

        # If only one input assume zero width
        elif left is None and right is not None:
            left = right
        elif left is not None and right is None:
            right = left

        # if iterable, find endpoints
        if hasattr(left, '__iter__') and hasattr(right, '__iter__'):

            LL = min(left)
            UL = min(right)
            LU = max(left)
            UU = max(right)

            left = min(LL,LU)
            right = max(LU,UU)

        elif hasattr(left, '__iter__'):

            LL = min(left)
            LU = max(left)

            left = min(LL,LU)


        elif hasattr(right, '__iter__'):

            UL = min(right)
            UU = max(right)

            right = max(UL,UU)


        if left > right:
            LowerUpper = [left, right]
            left = min(LowerUpper)
            right = max(LowerUpper)

        self.left = left
        self.right = right

    def __repr__(self) -> str: # return
        return "Interval [%g, %g]"%(self.left,self.right)

    def __str__(self) -> str: # print
        return "Interval [%g, %g]"%(self.left,self.right)

    def __format__(self, format_spec: str) -> str:
        try:
            return f'[{format(self.left, format_spec)},{format(self.right, format_spec)}]'
        except:
            raise ValueError(f'{format_spec} format specifier not understood for Interval object')
        
    def __iter__(self):
        for bound in [self.left, self.right]:
            yield bound

    def __len__(self):
        return 2

    def __add__(self,other):

        if other.__class__.__name__ == 'Interval':
            lo = self.left + other.left
            hi = self.right + other.right
        elif other.__class__.__name__ == 'Pbox':
            # Perform Pbox addition assuming independance
            return other.add(self, method = 'i')
        else:
            try:
                lo = self.left + other
                hi  = self.right + other
            except:
                return NotImplemented

        return Interval(lo,hi)

    def __radd__(self,left):
        return self.__add__(left)

    def __sub__(self, other):

        if other.__class__.__name__ == "Interval":

            lo = self.left - other.right
            hi = self.right - other.left
        elif other.__class__.__name__ == "Pbox":
            # Perform Pbox subtractnion assuming independance
            return other.rsub(self)
        else:
            try:
                lo = self.left - other
                hi  = self.right - other
            except:
                return NotImplemented

        return Interval(lo,hi)

    def __rsub__(self, other):
        if other.__class__.__name__ == "Interval":
            # should be overkill
            lo = other.right - self.left
            hi = other.right - self.right

        elif other.__class__.__name__ == "Pbox":
            # shoud have be caught by Pbox.__sub__()
            return other.__sub__(self)
        else:
            try:
                lo = other - self.right
                hi = other - self.left

            except:
                return NotImplemented

        return Interval(lo,hi)

    def __neg__(self):
        return Interval(-self.right, -self.left)
    
    def __mul__(self,other):
        if other.__class__.__name__ == "Interval":

            b1 = self.lo() * other.lo()
            b2 = self.lo() * other.hi()
            b3 = self.hi() * other.lo()
            b4 = self.hi() * other.hi()

            lo = min(b1,b2,b3,b4)
            hi = max(b1,b2,b3,b4)

        elif other.__class__.__name__ == "Pbox":

            return other.mul(self)

        else:

            try:

                lo = self.lo() * other
                hi = self.hi() * other

            except:

                return NotImplemented

        return Interval(lo,hi)

    def __rmul__(self,other):
        return self * other

    def __truediv__(self,other):

        if other.__class__.__name__ == "Interval":

            if other.straddles_zero():
                if other.left == 0:
                    lo = min(self.lo() / other.hi(), self.hi() / other.hi())
                    hi = np.inf
                elif other.right == 0:
                    lo = -np.inf
                    hi = max(self.lo() / other.lo(), self.hi() / other.lo())
                else:
                    # Cant divide by zero
                    raise ZeroDivisionError()
            else:
                b1 = self.lo() / other.lo()
                b2 = self.lo() / other.hi()
                b3 = self.hi() / other.lo()
                b4 = self.hi() / other.hi()

                lo = min(b1,b2,b3,b4)
                hi = max(b1,b2,b3,b4)
        elif other.__class__.__name__ == "Pbox":

            return other.__rtruediv__(self)
        
        else:
            try:
                lo = self.lo()/other
                hi = self.hi()/other
            except:

                return NotImplemented

        return Interval(lo,hi)


    def __rtruediv__(self,other):
        
        if self.straddles_zero():
            
            raise ZeroDivisionError()
        
        try:
            return other * self.recip()
        except:
            return NotImplemented


    def __pow__(self,other):
        if other.__class__.__name__ == "Interval":
            pow1 = self.left ** other.left
            pow2 = self.left ** other.right
            pow3 = self.right ** other.left
            pow4 = self.right ** other.right
            powUp = max(pow1,pow2,pow3,pow4)
            powLow = min(pow1,pow2,pow3,pow4)
        elif other.__class__.__name__ in ("int", "float"):
            pow1 = self.left ** other
            pow2 = self.right ** other
            powUp = max(pow1,pow2)
            powLow = min(pow1,pow2)
            if (self.right >= 0) and (self.left <= 0) and (other % 2 == 0):
                powLow = 0
        return Interval(powLow,powUp)

    def __rpow__(self,left):
        if left.__class__.__name__ == "Interval":
            pow1 = left.left ** self.left
            pow2 = left.left ** self.right
            pow3 = left.right ** self.left
            pow4 = left.right ** self.right
            powUp = max(pow1,pow2,pow3,pow4)
            powLow = min(pow1,pow2,pow3,pow4)

        elif left.__class__.__name__ in ("int", "float"):
            pow1 = left ** self.left
            pow2 = left ** self.right
            powUp = max(pow1,pow2)
            powLow = min(pow1,pow2)

        return Interval(powLow,powUp)


    def __lt__(self,other):
        # <
        if other.__class__.__name__ == 'Interval':
            if self.right < other.left:
                return Logical(1,1)
            elif self.left > other.right:
                return Logical(0,0)
            elif self.straddles(other.left,endpoints = False) or self.straddles(other.right,endpoints = False):
                return Logical(0,1)
            else:
                return Logical(0,0)
        else:
            try:
                if self.right < other:
                    return Logical(1,1)
                elif self.straddles(other,endpoints = False):
                    return Logical(0,1)
                else:
                    return Logical(0,0)
            except Exception as e:
                raise ValueError

    def __eq__(self,other):
        # ==
        if other.__class__.__name__ == 'Interval':
            if self.straddles(other.left) or self.straddles(other.right):
                return Logical(0,1)
            else:
                return Logical(0,0)
        elif other is None:
            try:
                self is None
            except:
                raise ValueError
        else:
            try:
                if self.straddles(other):
                    return Logical(0,1)
                else:
                    return Logical(0,0)
            except:
                raise ValueError


    def __gt__(self,other):
        # >
        if other.__class__.__name__ == 'Interval':
            if self.right < other.left:
                return Logical(0,0)
            elif self.left > other.right:
                return Logical(1,1)
            elif self.straddles(other.left,endpoints = False) or self.straddles(other.right,endpoints = False):
                return Logical(0,1)
            else:
                return Logical(0,0)
        else:
            try:
                if self.left > other:
                    return Logical(1,1)
                elif self.straddles(other,endpoints = False):
                    return Logical(0,1)
                else:
                    return Logical(0,0)
            except Exception as e:
                raise ValueError

    def __ne__(self,other):
        # !=
        if other.__class__.__name__ == 'Interval':
            if self.straddles(other.left) or self.straddles(other.right):
                return Logical(0,1)
            else:
                return Logical(1,1)
        else:
            try:
                if self.straddles(other):
                    return Logical(0,1)
                else:
                    return Logical(1,1)
            except:
                try:
                    return not self is other
                except:
                    raise ValueError

    def __le__(self,other):
        # <=
        if other.__class__.__name__ == 'Interval':
            if self.right <= other.left:
                return Logical(1,1)
            elif self.left >= other.right:
                return Logical(0,0)
            elif self.straddles(other.left,endpoints = True) or self.straddles(other.right,endpoints = True):
                return Logical(0,1)
            else:
                return Logical(0,0)
        else:
            try:
                if self.right <= other:
                    return Logical(1,1)
                elif self.straddles(other,endpoints = True):
                    return Logical(0,1)
                else:
                    return Logical(0,0)
            except Exception as e:
                raise ValueError

    def __ge__(self,other):
        if other.__class__.__name__ == 'Interval':
            if self.right <= other.left:
                return Logical(0,0)
            elif self.left >= other.right:
                return Logical(1,1)
            elif self.straddles(other.left,endpoints = True) or self.straddles(other.right,endpoints = True):
                return Logical(0,1)
            else:
                return Logical(0,0)
        else:
            try:
                if self.left > other:
                    return Logical(1,1)
                elif self.straddles(other,endpoints = True):
                    return Logical(0,1)
                else:
                    return Logical(0,0)
            except Exception as e:
                raise ValueError

    def __bool__(self):

        try:
            if self.to_logical():
                return True
            else:
                return False
        except:
            raise ValueError("Truth value of Interval %s is ambiguous" %self)
        
    def __abs__(self):
        if self.straddles_zero():
            return Interval(0, max(abs(self.left),abs(self.right)))
        else:
            return Interval(abs(self.left),abs(self.right))

    def padd(self,other):
        """
        Returns addition using perfect arithmetic
        
        a+b = [a.left + b.left, a.right + b.right]
        """
        return Interval(self.left + other.left, self.right + other.right)
  
    def psub(self,other):
        """
        Returns subtraction using perfect arithmetic
        
        a+b = [a.left - b.left, a.right - b.right]
        """
        return Interval(self.left - other.left, self.right - other.right)

    def pmul(self,other):
        """
        Returns multiplication using opposite arithmetic
        
        a*b = [a.left * b.left, a.right * b.right]
        """
        return Interval(self.left * other.left, self.right * other.right)

    def pdiv(self,other):
        """
        Returns division using opposite arithmetic
        
        a/b = [a.left / b.left, a.right / b.right]
        """
        return Interval(self.left / other.left, self.right / other.right)    
    
    def oadd(self,other):
        """
        Returns addition using opposite arithmetic
        
        a+b = [a.left + b.right, a.right + b.left]
        """
        return Interval(self.left + other.right, self.right + other.left)
  
    def osub(self,other):
        """
        Returns subtraction using opposite arithmetic
        
        a+b = [a.left - b.right, a.right - b.left]
        """
        return Interval(self.left - other.right, self.right - other.left)
    
    def omul(self,other):
        """
        Returns multiplication using opposite arithmetic
        
        a*b = [a.left * b.right, a.right * b.left]
        """
        return Interval(self.left * other.right, self.right * other.left)

    def odiv(self,other):
        """
        Returns division using opposite arithmetic
        
        a/b = [a.left / b.right, a.right / b.left]
        """
        return Interval(self.left / other.right, self.right / other.left)      
    
    def equiv(self,other):
        """
        Checks whether two intervals are equivalent. 
        True if self.left == other.right and self.right == other.right
        """
        return (self.left == other.left and self.right == other.right)
    
    def lo(self):
        """
        Returns the left side of the interval
        """
        return self.left

    def hi(self):
        """
        Returns the right side of the interval
        """
        return self.right
    
    def width(self):
        """
        Returns the width of the interval
        self.right - self.left
        """
        return self.right - self.left

    
    def midpoint(self):
        """
        Returns midpoint of interval
        (self.left+self.right)/2
        """
        
        return (self.left+self.right)/2
    
    def to_logical(self):
        '''
        Turns the interval into a logical interval, this is done by chacking the truth value of the ends of the interval
        '''
        if self.left:
            left = True
        else:
            left = False
        
        if self.right:
            right = True
        else:
            right = False
        
        return Logical(left,right)
    
        
    def straddles(self,N, endpoints = True):
        """
        Parameters
        ----------
        N : numeric
            Number to check
        endpoints : bool
            Whether to include the endpoints within the check

        Returns
        -------
        True
            If :math:`\\mathrm{left} \\leq N \\leq \mathrm{right}` (Assuming `endpoints=True`)
        False
            Otherwise
        """
        if endpoints:
            if self.left <= N and self.right >= N:
                return True
        else:
            if self.left < N and self.right > N:
                return True

        return False

    def straddles_zero(self,endpoints = True):
        """
        Checks whether :math:`0` is within the interval
        """
        return self.straddles(0,endpoints)

    def recip(self):
        """
        Calculates the reciprocle of the interval.
        If :math:`0 \\in [a,b]` it returns a division by zero error

        """
        if self.straddles_zero():
            # Cant divide by zero
            raise ZeroDivisionError()

        elif 1/self.hi() < 1/self.lo():
            return Interval(1/self.hi(), 1/self.lo())
        else:
            return Interval(1/self.lo(), 1/self.hi())

    def intersection(self, other):
        '''
        Calculates the intersection between two intervals
        '''
        if isinstance(other, Interval):
            if self.straddles(other):
                return I(max([x.left for x in [self, other]]), min([x.right for x in [self, other]]))
            else:
                return None
        elif isinstance(other, list):
            if all([self.straddles(o) for o in other]):
                assert all([isinstance(o, Interval) for o in other]), 'All intersected objects must be intervals'
                return I(max([x.left for x in [self] + other]), min([x.right for x in [self] + other]))
            else:
                return None
        else:
            if self.straddles(other):
                return other
            else:
                return None

    def exp(self):
        lo = np.exp(self.left)
        hi = np.exp(self.right)
        return Interval(lo,hi)
    
    def log(self):
        lo = np.log(self.left)
        hi = np.log(self.right)
        return Interval(lo,hi)
    
    def sqrt(self):
        if self.left >= 0:
            return Interval(np.sqrt(self.left),np.sqrt(self.right))
        else:
            print("RuntimeWarning: invalid value encountered in sqrt")
            return Interval(np.nan,np.sqrt(self.right))
        
    def sin(self):
        return Interval(np.sin(self.left),np.sin(self.right))
    def cos(self):
        return Interval(np.cos(self.left),np.cos(self.right))
    def tan(self):
        return Interval(np.tan(self.left),np.tan(self.right))
    
    def sample(self, seed = None) -> float:
        '''
        Returns a random value from within the interval        
        '''
        
        if seed is not None:
            r.seed(seed)
        return self.left + r.random()*self.width()
    
# Alias
I = Interval

class Logical(Interval):
    '''
    Imprecise Boolean object
    
    Parameters
    ----------
    left : bool
        left side of interval
    right : bool
        right side of interval
    Attributes
    ----------
    left : bool
        left side of interval
    right : bool
        right side of interval
        
    '''
    def __init__(self, left: bool ,right: bool = None):

        super().__init__(left, right)

    def __bool__(self):

        if self.left == 0 and self.right == 0:
            return False
        if self.left == 1 and self.right == 1:
            return True
        else:
            print('WARNING: Truth value of Logical is ambiguous, use pba.sometime or pba.always')
            return True

    def __repr__(self):

        if self.left == 0 and self.right == 0:
            return 'False'
        elif self.left == 1 and self.right == 1:
            return 'True'
        else:
            return "[%g, %g]"%(self.left,self.right)

    __str__ = __repr__