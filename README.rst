This is a probability bound analysis library for Python

Intervals can be specified by using ``pba.I(x,y)``

Probability distributions can be specified using
``pba.distname(**args)`` for all distribution that scipy.stats supports.
Using interval arguments return p-boxes

K out of N confidence boxes can be specified using ``pba.KN(k,n)``

``+,-,*,/`` operations are supported. By default frechet convolutions
are used. But independant, perfect and opposite convolutions are also
supported, they can be specified using a letter as in:

::

   A.add(B, method = 'o') # A + B using opposite convolutions
   C.sub(D, method = 'p') # C - D using perfect convolutions
   E.mul(F, method = 'i') # E * F using independence convolutions
   G.div(H, method = 'f') # G / H using frechet convolutions

--------------

Note: currently there may be errors in creating p-boxes for certain
distribution types because of the way arguments are passed to the
distributions in scipy.stats library. If these errors are noticed please
email me
