These instructions explain the steps required to fill in the Financial_Model_Template to be able to execute financial risk analysis on vertical farms considering commonly reported issues, opportunities and failure modes of vertical farms.

The goal of this analysis is to risk-empower your business plan to help your farm become resilient and acquire funding. The spreadsheet is a prototype of the economic risk analysis software and requires information about your business model and farm set-up. This will then be processed through a Python script that will conduct a survival model analysis (first-passage time) which has been commonly used in economics research.

Getting Started: To get started, open up the template Current_Financial_Model and save a copy. It will walk through the process of setting up your model.

Questions?: If you have any questions about the spreadsheet, feel free to email me on sgfbaumo@liv.ac.uk. I'd love to answer any questions.  

---

### Instructions for Spreadsheet

1. Download a copy of this folder and unzip.
2. Open *Current_Financial_Model* and select ‘*Overview*’ sheet (ignore '*Inputs*', this is for the risk analysis script).
3. Focus on editing all Blue cells. You can click and type on them, or sometimes they have an dropdown arrow that you can click to choose options. These are the input parameters required to conduct the analysis. You can approach these points systematically. 
    - [ ]  Currency
    - [ ]  Start date
    - [ ]  Farm Characteristics
    - [ ]  Crop and System Selection - select your crops and systems from a list.
    You can overwrite crop yields and system data easily with the yellow cells. 
    If you like you optionally add information about lights, crops, system to the '*database*' tab.
    - [ ]  Company Info
    - [ ]  Revenue Streams
    - [ ]  Operating Expenses
    - [ ]  Staff Calculations and Head-Count
    - [ ]  Productivity Metrics

Helpful tips are provided by hovering over a cell with a red corner.

4. Take note for any Blue cells that you are unable to provide a precise value for, i.e. you may uncertain of yield, so you want to say the range is 1500-2000kg rather than 1750kg. You can provide estimates at bottom of these instructions in the table Uncertain Parameters.
5. Green cells are based on your growth plans based on Blue cells, but should be overwritten if they are incorrect and a precise value is known.

5. Yellow cells will compute values based on Blue cells, but should be overwritten if they are incorrect and a precise value is known.

6. Select the ‘*CapEx Breakdown*’ Sheet and insert information about capital costs of your farm. Ensure the Total Cost is correct. This will enable more reliable return on investment projections and is necessary for the risk analysis.

- [ ]  Change default yellow cells for CapEx
- [ ]  Make sure Total CapEx in row 37 is correct (you can leave alone if you don't have an estimate)

7. Select the ‘*Risks*’ tab to insert risks and opportunities you would like to consider within the analysis. There are some examples that have been defaults programmed into the system already if you don't want to add any. 

- [ ]  Add any risks you can think of for climate control, growing systems, biosecurity, process and packaging, management, sales and marketing, team risk.
- [ ]  Add any opportunities, i.e. cost savings or deals you think you may have in the future.

8. Save the *Current_Financial_model* as [Name_of_farm]_[scenario no.].xlsx

9. Repeat the above steps and save as a sequential scenario no. for a comparison if desired.

10. You can click the '*Summary*' tab to see summary cash flow and predicted pay back period.

----

### Instructions for Risk Analysis Python Script


11. Create a copy of main_pba.py and save as [farm_name]_pba.py
12. Change line 102 of filename = 'XXX' to the filename of your financial model spreadsheet.
13. You can manually define inputs to include uncertainty from Lines 128-142 through using the pba package (currently in beta testing).
14. Change line 501 of export results' input from results.xlsx to a name you prefer. This will save the quantitative results of the analysis.
15. Toggle risks and opportunities on line 203 from True or False to incorporate into the analysis.
16. Risks and opportunities can be added or adjusted instead of using default values by adapting risk_pba.py code.
17. Run the code to execute analysis.
18. Results are visualised as plots and quantitative data will be exported to the results document you named.
19. Alternatively, email sgfbaumo@liverpool.ac.uk for assistance.

--



Probability Bounds Analysis (pba) Package

Intervals can be specified by using `pba.I(x,y)`

Probability distributions can be specified using `pba.distname(**args)` for all distribution that scipy.stats supports. Using interval arguments return p-boxes

K out of N confidence boxes can be specified using `pba.KN(k,n)`

`+,-,*,/` operations are supported. By default frechet convolutions are used. But independant, perfect and opposite convolutions are also supported, they can be specified using a letter as in:

    A.add(B, method = 'o') # A + B using opposite convolutions
    C.sub(D, method = 'p') # C - D using perfect convolutions
    E.mul(F, method = 'i') # E * F using independence convolutions
    G.div(H, method = 'f') # G / H using frechet convolutions

***
Note:
currently there may be errors in creating p-boxes for certain distribution types because of the way arguments are passed to the distributions in scipy.stats library. If these errors are noticed please email me 
