import openpyxl
import formulas

fpath, dir_output = 'Model_onepage.xlsx', 'output'
xl_model = formulas.ExcelModel().loads(fpath).finish()
xl_model.calculate()
Solution(...)
xl_model.write(dirpath=dir_output)
{'EXCEL.XLSX': {Book: <openpyxl.workbook.workbook.Workbook ...>}}

circular=True

# To plot the dependency graph that depict relationships between Excel cells:

>>> dsp = xl_model.dsp
>>> dsp.plot(view=False)  # Set view=True to plot in the default browser.
SiteMap([(ExcelModel, SiteMap(...))])

# >>> xl_model.calculate(
# ...     inputs={
# ...         "'[EXCEL.XLSX]DATA'!A2": 3,  # To overwrite the default value.
# ...         "'[EXCEL.XLSX]DATA'!B3": 1  # To impose a value to B3 cell.
# ...     },
# ...     outputs=[
# ...        "'[EXCEL.XLSX]DATA'!C2", "'[EXCEL.XLSX]DATA'!C4"
# ...     ] # To define the outputs that you want to calculate.
# ... )
# Solution([("'[EXCEL.XLSX]DATA'!A2", <Ranges>('[EXCEL.XLSX]DATA'!A2)=[[3]]),
#           ("'[EXCEL.XLSX]DATA'!A3", <Ranges>('[EXCEL.XLSX]DATA'!A3)=[[6]]),
#           ("'[EXCEL.XLSX]DATA'!B3", <Ranges>('[EXCEL.XLSX]DATA'!B3)=[[1]]),
#           ("'[EXCEL.XLSX]DATA'!D2", <Ranges>('[EXCEL.XLSX]DATA'!D2)=[[1]]),
#           ("'[EXCEL.XLSX]DATA'!B2", <Ranges>('[EXCEL.XLSX]DATA'!B2)=[[9.0]]),
#           ("'[EXCEL.XLSX]DATA'!D3", <Ranges>('[EXCEL.XLSX]DATA'!D3)=[[2.0]]),
#           ("'[EXCEL.XLSX]DATA'!C2", <Ranges>('[EXCEL.XLSX]DATA'!C2)=[[10.0]]),
#           ("'[EXCEL.XLSX]DATA'!D4", <Ranges>('[EXCEL.XLSX]DATA'!D4)=[[3.0]]),
#           ("'[EXCEL.XLSX]DATA'!C4", <Ranges>('[EXCEL.XLSX]DATA'!C4)=[[4.0]])])









# import os
# os.getcwd()
#
# import pandas as pd
# file = 'Financialmodel.xlsx'
# data = pd.ExcelFile(file)
# print(data.sheet_names) #this returns the all the sheets in the excel file
# ['Sheet1']
#
# df = data.parse('Sheet1')
# df.info
# df.head(10)

