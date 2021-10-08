import pba
from pba_plot import minmaxmean
# x= 0.5
# y = 0.1
# if pba.norm(0.5, 0.1) < 0.5: print(pba.norm(0.5, 0.1) < 0.5)

counter_strict =[]
counter_poss = []

pba.mmms(10, 50, 40, 6.2)

pba.mmms(5,10,7.5, 8)

b= minmaxmean(5, 10, 7.5)
b.show()