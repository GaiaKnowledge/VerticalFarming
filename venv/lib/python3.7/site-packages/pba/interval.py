# -*- coding: utf-8 -*-

import numpy as np
import random as r

from .logic import Logical

__all__ = ['Interval','I']

class Interval():
    """
    Interval
    ---------
    An interval is an uncertain number for which only the endpoints are known, for example if :math:`x=[a,b]`
    then this can be interpreted as :math:`x` being between :math:`a` and :math:`b` but with no more information about the value of :math:`x`
    .
    Intervals can be created using::
        pba.I(left,right)
        pba.Interval(left,right)
    Parameters
    ----------
    left : numeric
        Left side of interval
    right : numeric
        Right side of interval
    Attributes
    ----------
    Left : numeric
        Left side of interval
    Right : numeric
        Right side of interval

    """
    def __init__(self,Left = None, Right = None):


        # kill complex nums
        assert not isinstance(Left, np.complex) or not isinstance(Right, np.complex), "Inputs must be real numbers"

        # assume vaccous if no inputs
        if Left is None and Right is None:
            Right = np.inf
            Left = np.inf

        # If only one input assume zero width
        elif Left is None and Right is not None:
            Left = Right
        elif Left is not None and Right is None:
            Right = Left

        # if iterable, find endpoints
        if hasattr(Left, '__iter__') and hasattr(Right, '__iter__'):

            LL = min(Left)
            UL = min(Right)
            LU = max(Left)
            UU = max(Right)

            Left = min(LL,LU)
            Right = max(LU,UU)

        elif hasattr(Left, '__iter__'):

            LL = min(Left)
            LU = max(Left)

            Left = min(LL,LU)


        elif hasattr(Right, '__iter__'):

            UL = min(Right)
            UU = max(Right)

            Right = max(UL,UU)


        if Left > Right:
            LowerUpper = [Left, Right]
            Left = min(LowerUpper)
            Right = max(LowerUpper)

        self.Left = Left
        self.Right = Right

    def __repr__(self): # return
        return "[%g, %g]"%(self.Left,self.Right)

    def __str__(self): # print
        return "[%g, %g]"%(self.Left,self.Right)

    def __iter__(self):
        for bound in [self.Left, self.Right]:
            yield bound

    def __len__(self):
        return 2

    def __add__(self,other):

        if other.__class__.__name__ == 'Interval':
            lo = self.Left + other.Left
            hi = self.Right + other.Right
        elif other.__class__.__name__ == 'Pbox':
            # Perform Pbox addition assuming independance
            return other.add(self, method = 'i')
        else:
            try:
                lo = self.Left + other
                hi  = self.Right + other
            except:
                return NotImplemented

        return Interval(lo,hi)

    def __radd__(self,left):
        return self.__add__(left)

    def __sub__(self, other):

        if other.__class__.__name__ == "Interval":

            lo = self.Left - other.Right
            hi = self.Right - other.Left
        elif other.__class__.__name__ == "Pbox":
            # Perform Pbox subtractnion assuming independance
            return other.rsub(self)
        else:
            try:
                lo = self.Left - other
                hi  = self.Right - other
            except:
                return NotImplemented

        return Interval(lo,hi)

    def __rsub__(self, other):
        if other.__class__.__name__ == "Interval":
            # should be overkill
            lo = other.Right - self.Left
            hi = other.Right - self.Right

        elif other.__class__.__name__ == "Pbox":
            # shoud have be caught by Pbox.__sub__()
            return other.__sub__(self)
        else:
            try:
                lo = other - self.Right
                hi = other - self.Left

            except:
                return NotImplemented

        return Interval(lo,hi)

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
                if other.Left == 0:
                    lo = min(self.lo() / other.hi(), self.hi() / other.hi())
                    hi = np.inf
                elif other.Right == 0:
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

        else:
            try:
                lo = self.lo()/other
                hi = self.hi()/other
            except:

                return NotImplemented

        return Interval(lo,hi)


    def __rtruediv__(self,other):

        try:
            return other * self.recip()
        except:
            return NotImplemented


    def __pow__(self,other):
        if other.__class__.__name__ == "Interval":
            pow1 = self.Left ** other.Left
            pow2 = self.Left ** other.Right
            pow3 = self.Right ** other.Left
            pow4 = self.Right ** other.Right
            powUp = max(pow1,pow2,pow3,pow4)
            powLow = min(pow1,pow2,pow3,pow4)
        elif other.__class__.__name__ in ("int", "float"):
            pow1 = self.Left ** other
            pow2 = self.Right ** other
            powUp = max(pow1,pow2)
            powLow = min(pow1,pow2)
            if (self.Right >= 0) and (self.Left <= 0) and (other % 2 == 0):
                powLow = 0
        return Interval(powLow,powUp)

    def __rpow__(self,left):
        if left.__class__.__name__ == "Interval":
            pow1 = left.Left ** self.Left
            pow2 = left.Left ** self.Right
            pow3 = left.Right ** self.Left
            pow4 = left.Right ** self.Right
            powUp = max(pow1,pow2,pow3,pow4)
            powLow = min(pow1,pow2,pow3,pow4)

        elif left.__class__.__name__ in ("int", "float"):
            pow1 = left ** self.Left
            pow2 = left ** self.Right
            powUp = max(pow1,pow2)
            powLow = min(pow1,pow2)

        return Interval(powLow,powUp)


    def __lt__(self,other):
        # <
        if other.__class__.__name__ == 'Interval':
            if self.Right < other.Left:
                return Logical(1,1)
            elif self.Left > other.Right:
                return Logical(0,0)
            elif self.straddles(other.Left,endpoints = False) or self.straddles(other.Right,endpoints = False):
                return Logical(0,1)
            else:
                return Logical(0,0)
        else:
            try:
                if self.Right < other:
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
            if self.straddles(other.Left) or self.straddles(other.Right):
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
            if self.Right < other.Left:
                return Logical(0,0)
            elif self.Left > other.Right:
                return Logical(1,1)
            elif self.straddles(other.Left,endpoints = False) or self.straddles(other.Right,endpoints = False):
                return Logical(0,1)
            else:
                return Logical(0,0)
        else:
            try:
                if self.Left > other:
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
            if self.straddles(other.Left) or self.straddles(other.Right):
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
            if self.Right <= other.Left:
                return Logical(1,1)
            elif self.Left >= other.Right:
                return Logical(0,0)
            elif self.straddles(other.Left,endpoints = True) or self.straddles(other.Right,endpoints = True):
                return Logical(0,1)
            else:
                return Logical(0,0)
        else:
            try:
                if self.Right <= other:
                    return Logical(1,1)
                elif self.straddles(other,endpoints = True):
                    return Logical(0,1)
                else:
                    return Logical(0,0)
            except Exception as e:
                raise ValueError

    def __ge__(self,other):
        if other.__class__.__name__ == 'Interval':
            if self.Right <= other.Left:
                return Logical(0,0)
            elif self.Left >= other.Right:
                return Logical(1,1)
            elif self.straddles(other.Left,endpoints = True) or self.straddles(other.Right,endpoints = True):
                return Logical(0,1)
            else:
                return Logical(0,0)
        else:
            try:
                if self.Left > other:
                    return Logical(1,1)
                elif self.straddles(other,endpoints = True):
                    return Logical(0,1)
                else:
                    return Logical(0,0)
            except Exception as e:
                raise ValueError

    def __bool__(self):
        print(Logical(self.Left,self.Right))
        try:
            if Logical(self.Left,self.Right):

                return True
            else:
                return False
        except:
            raise ValueError("Truth value of Interval %s is ambiguous" %self)

    def padd(self,other):
        """
        Returns addition using perfect arithmetic
        
        a+b = [a.Left + b.Left, a.Right + b.Right]
        """
        return Interval(self.Left + other.Left, self.Right + other.Right)
  
    def psub(self,other):
        """
        Returns subtraction using perfect arithmetic
        
        a+b = [a.Left - b.Left, a.Right - b.Right]
        """
        return Interval(self.Left - other.Left, self.Right - other.Right)
    
    def oadd(self,other):
        """
        Returns addition using opposite arithmetic
        
        a+b = [a.Left + b.Right, a.Right + b.Left]
        """
        return Interval(self.Left + other.Right, self.Right + other.Left)
  
    def osub(self,other):
        """
        Returns subtraction using opposite arithmetic
        
        a+b = [a.Left - b.Right, a.Right - b.Left]
        """
        return Interval(self.Left - other.Right, self.Right - other.Left)
      
    def left(self):
        """
        Returns the left side of the interval
        """
        return self.Left

    def right(self):
        """
        Returns the right side of the interval
        """
        return self.Right

    lo = left
    hi = right
    
    def width(self):
        """
        Returns the width of the interval
        self.Right - self.Left
        """
        return self.Right - self.Left

    
    def midpoint(self):
        """
        Returns midpoint of interval
        (self.Left+self.Right)/2
        """
        
        return (self.Left+self.Right)/2
    
    # def mean(*args):
    #     LSum = 0
    #     USum = 0
    #     DataLen = len(args)
    #     for x in args:
    #         if x.__class__.__name__ in ("int","float"):
    #             x = Interval(x)
    #         if x.__class__.__name__ in ("list","tuple"):
    #             DataLen = DataLen + (len(x) - 1)
    #             for y in x:
    #                 if y.__class__.__name__ in ("int","float"):
    #                     y = Interval(y)
    #                 LSum = LSum + y.Left
    #                 USum = USum + y.Right
    #         if x.__class__.__name__ == "Interval":
    #             LSum = LSum + x.Left
    #             USum = USum + x.Right
    #         LMean = LSum / DataLen
    #         UMean = USum / DataLen
    #     return Interval(LMean, UMean)

    # def median(*args):
    #     LBounds = []
    #     LSorted = []
    #     UBounds = []
    #     USorted = []

    #     for x in [*args]:
    #         if x.__class__.__name__ in ("int","float"):
    #             x = Interval(x)
    #             LBounds.append(x.Left)
    #             UBounds.append(x.Right)
    #         if x.__class__.__name__ in ("list","tuple"):
    #             for y in x:
    #                 if y.__class__.__name__ in ("int","float"):
    #                     y = Interval(y)
    #                 LBounds.append(y.Left)
    #                 UBounds.append(y.Right)
    #         if x.__class__.__name__ == "Interval":
    #             LBounds.append(x.Left)
    #             UBounds.append(x.Right)
    #     while (len(LBounds) > 0):
    #         MinL = min(LBounds)
    #         LSorted.append(MinL)
    #         LBounds.remove(MinL)
    #     while (len(UBounds) > 0):
    #         MinU = min(UBounds)
    #         USorted.append(MinU)
    #         UBounds.remove(MinU)

    #     if (len(LSorted) % 2) != 0:
    #         LMedian = LSorted[len(LSorted)//2]
    #         UMedian = USorted[len(USorted)//2]
    #     else:
    #         LMedian = (LSorted[len(LSorted)//2] + LSorted[(len(LSorted)//2)-1])/2
    #         UMedian = (USorted[len(USorted)//2] + USorted[(len(USorted)//2)-1])/2
    #     return Interval(LMedian,UMedian)

    # def variance(*args):
    #     dataMean = Interval.mean(*args)
    #     LBounds = []
    #     UBounds = []
    #     LDev = []
    #     UDev = []
    #     DataLen = len(args)
    #     for x in [*args]:
    #         if x.__class__.__name__ in ("int","float"):
    #             x = Interval(x)
    #             LBounds.append(x.Left)
    #             UBounds.append(x.Right)
    #         if x.__class__.__name__ in ("list","tuple"):
    #             DataLen = DataLen + (len(x) - 1)
    #             for y in x:
    #                 if y.__class__.__name__ in ("int","float"):
    #                     y = Interval(y)
    #                 LBounds.append(y.Left)
    #                 UBounds.append(y.Right)

    #     for y in LBounds:
    #         LDev.append(abs(y - dataMean.Left)**2)
    #     for z in UBounds:
    #         UDev.append(abs(z - dataMean.Right)**2)

    #     LSDev = (sum(LDev))/DataLen
    #     USDev = (sum(UDev))/DataLen
    #     return Interval(LSDev, USDev)

    # def mode(*args):
    #     NotImplemented
        
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
            if self.Left <= N and self.Right >= N:
                return True
        else:
            if self.Left < N and self.Right > N:
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
                return I(max([x.Left for x in [self, other]]), min([x.Right for x in [self, other]]))
            else:
                return None
        elif isinstance(other, list):
            if all([self.straddles(o) for o in other]):
                assert all([isinstance(o, Interval) for o in other]), 'All intersected objects must be intervals'
                return I(max([x.Left for x in [self] + other]), min([x.Right for x in [self] + other]))
            else:
                return None
        else:
            if self.straddles(other):
                return other
            else:
                return None

    def exp(self):
        lo = np.exp(self.Left)
        hi = np.exp(self.Right)
        return Interval(lo,hi)
# a = Interval(1,2)
# b = Interval(3,4)
# c = Interval(-2,5)
# d = Interval(-7,-4)

##.sort() function to sort numbers for median
##list1.count(x) function to help with mode


I = Interval
