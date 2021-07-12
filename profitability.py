import matplotlib.pyplot as plt
import numpy as np
plt.clf()
plt.cla()

plt.rcdefaults()
fig, ax = plt.subplots()

# Example data
reports = ('#6 VF Japan (2014)', 'VF #5 (2017)', '#6 VF Japan (2018)', 'VF #17 (2019)')
#'#5 Container VF (2017)','#17 Container VF (2019)', '#5 GH (2017)', '#17 GH (2019)')
performance = [25, 27, 50, 47]# 50, 43, 67, 50]
break_even = [25+25, 0, 0, 22+47] # 0, 14+43, 0, 26+50]

y_pos = np.arange(len(performance))
error = [[0,0,0,0],(0,0,0, 16)]
#error = [[0,0,0,0,0,0,0,0],(0,0,0, 16, 0, 14, 0, 11)]
error1 = (0,0,0, 16)# 0, 14, 0, 11)


ax.barh(y_pos, break_even, align='center', color='g', label='Break-even')
ax.barh(y_pos, performance, align='center', color='c', label='Profitable')
plt.errorbar(performance, reports, xerr=error1, yerr=None,xlolims=True, label='Error bar', color='r', linestyle='')

ax.set_yticks(y_pos)
ax.set_yticklabels(reports)
ax.invert_yaxis()  # labels read top-to-bottom
ax.set_ylabel('Analysis')
ax.set_xlabel('Percentage (%)')
ax.set_title('Profitability of Vertical Farms')
ax.legend(loc='upper right', frameon=False)
#plt.tight_layout()
plt.grid(axis='x', linewidth=0.25)

plt.annotate('N=165', (2,0.15)) # Japan 2014
plt.annotate('N=56', (2,1.1)) # SIFR 2017
plt.annotate('N=215', (2,2.1)) # Japan 2018
plt.annotate('N=223', (2,3.1)) # CEA Census 2019
plt.annotate('N=10', (2,4.05)) # Container VF 2017
plt.annotate('N=33', (2,5.1)) # Container VF CEA 2019
plt.annotate('N=70', (2,6.05)) # GH SIFR 2017
plt.annotate('N=167', (2,7.1)) # GH CEA Census  2019


plt.show()