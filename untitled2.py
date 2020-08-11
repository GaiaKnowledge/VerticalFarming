# -*- coding: utf-8 -*-
"""
Created on Fri Jul 31 03:23:30 2020

@author: ferson
"""

import tkinter as tk
from tkinter import filedialog
import pandas as pd

root = tk.Tk()

canvas1 = tk.Canvas(root, width=300, height=300, bg='lightsteelblue')
canvas1.pack()


def getExcel():
    global df

    import_file_path = filedialog.askopenfilename()
    df = pd.read_excel(import_file_path)
    print(df)



browseButton_Excel = tk.Button(text='Import Excel File', command=getExcel, bg='green', fg='white',
                               font=('helvetica', 12, 'bold'))
canvas1.create_window(150, 150, window=browseButton_Excel)

root.mainloop()


item_number = df['part number']
quantity = df['quantity']

uniques = []
amounts = []

for number in item_number:

    if number not in uniques:
        print('adding', number)
        #print(item_number.index(number))
        print(quantity[number])
        uniques = uniques + [number]
#        amounts = amounts.append(quantity(item_number.index(number)))
        amounts = amounts.append(quantity[number])
    elif number in uniques:
        g = amounts(amounts.index(number)) + amounts(uniques.find(number))


print(uniques)
print(amounts)
