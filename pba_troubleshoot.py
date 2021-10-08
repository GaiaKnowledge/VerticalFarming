import pba
import pandas as pd

a = pba.Pbox(pba.I(50, 180), mean_left=79, mean_right=155, var_left=0.0, var_right=249)

b = pba.Pbox(pba.I(-40, 50), mean_left=-17, mean_right=22, var_left=181, var_right=256)
b += pba.Pbox([900, 1200])*5
b -= pba.Pbox(pba.I(300,500))
b *= pba.Pbox(pba.I(-9000, 2800), mean_left=--600, mean_right=900, var_left=0, var_right=2208)
b += pba.beta(500,250)
b /= pba.Pbox(pba.I(90,100))

print(a)
print(b)

print(a+b)