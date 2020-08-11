# -*- coding: utf-8 -*-
"""
Created on Wed Jul 29 14:48:58 2020

@author: ferson
"""

# <, etc. now work;  
# & and | work for independent, but not for Frechet because they need min, max
# there are two kinds of min/max, the first for env and imp, but the one we need for logicals is the binary convolutions min and max
# you don't seem to have implemented a general convolution function (add is handled specially)
# init changed slightly, under your eyes

# seems very strange to hard code "200" everywhere
# tails of plots are peculiar colors
# plots connect the dots, rather than step 

# <, <=, >, >=,
# and, or, not
# env
# min, max

import pba

a = pba.norm(0.05,0.01)
b = pba.unif(0.02,0.06)

c = a + b    # both work
d = a.add(b) # both work
d.show(False); 
c.show(); 

c = a.env(b)      # both work           
d = pba.env(a,b)  # both work
d.show(False); 
c.show(); 

c = a.add(b,method='i')
d = a.add(b,method='f')
e = a + b

print(type(c))
x = c.get_x()
x0 = x[0]
x1 = x[1]
y = c.get_y()
y0 = y[0]
y1 = y[1]

print(type(d))
x = d.get_x()
x0 = x[0]
x1 = x[1]
y = d.get_y()
y0 = y[0]
y1 = y[1]

a.show(); b.show(); c.show()

d.show(False); 
c.show(); 

d.show(False); 
e.show(); 

a.show(True)

print('Less than')
c = a < b
print(c)

print('Less than or equal')
c = a <= b
print(c)

print('Greater than')
c = a > b
print(c)

print('Greater than or equal')
c = a >= b
print(c)

print('Frechet And')
c = a & b
print(c)

print('Frechet Or')
c = a | b
print(c)


print('Independent Less than')
c = a.lt(b, method='i')
print(c)

print('Independent Less than or equal')
c = a.le(b, method='i')
print(c)

print('Independent Greater than')
c = a.gt(b, method='i')
print(c)

print('Independent Greater than or equal')
c = a.ge(b, method='i')
print(c)

print('Independent And')
c = a.logicaland(b, method='i')
print(c)

print('Independent Or')
c = a.logicalor(b, method='i')
print(c)

# analogous Risk Calc calculations
#
# a = N(0.05,0.01)
# b = U(0.02,0.06)
# clear; show a in red; show b in blue
#
# a < b
#    [ 0, 0.6666666666667] 
# a <= b
#    [ 0, 0.6666666666667] 
# a > b
#    [ 0.3333333333333, 1] 
# a >= b
#    [ 0.3333333333333, 1] 
#
# a & b
#    ~(range=[0,0.06],  mean=[0,0.04],  var=[0,0.000134]) 
# a | b
#    ~(range=[0.0242417,0.135758],  mean=[0.05,0.09],  var=[0,0.00047]) 
#
# a |<| b
#    [ 0.2525252525252, 0.2828282828283] 
# a |<=| b
# Syntax Problem
# a |>| b
#    [ 0.7171717171717, 0.7474747474748] 
# a |>=| b
# Syntax Problem
#
# a |&| b
#    ~(range=[0.000484834,0.0045455],  mean=0.002,  var=[0.0000005066666,0.0000005066667]) 
# a ||| b
#    ~(range=[0.0437569,0.131213],  mean=[0.08714,0.08886],  var=[0.000185,0.000246]) 


pba.straddles(a)

a = pba.norm(0.05,0.01, steps=20)
b = pba.unif(0.02,0.06, steps=20)

c = a < b
print(c)