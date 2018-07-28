# import pandas as pd
# import numpy as np

# # Define the diff function to show the changes in each field
# def report_diff(x):
#     return x[0] if x[0] == x[1] else '{} ---> {}'.format(*x)

# # We want to be able to easily tell which rows have changes
# def has_change(row):
#     if "--->" in row.to_string():
#         return "Y"
#     else:
#         return "N"

# # Read in both excel files
# df1 = pd.read_excel('TestReportLayout.xls', 'Complete Assessment', na_values=['NA'])
# df2 = pd.read_excel('report2.xls', 'Complete Assessment', na_values=['NA'])

# # Make sure we order by account number so the comparisons work


# # Create a panel of the two dataframes
# diff_panel = pd.Panel(dict(df1=df1,df2=df2))

# #Apply the diff function
# diff_output = diff_panel.apply(report_diff, axis=0)

# # Flag all the changes
# diff_output['has_change'] = diff_output.apply(has_change, axis=1)

# #Save the changes to excel but only include the columns we care about
# diff_output[(diff_output.has_change == 'Y')].to_excel('my-diff-1.xlsx',index=False)

# from itertools import zip_longest
# import xlrd

# rb1 = xlrd.open_workbook('TestReportLayout.xls')
# rb2 = xlrd.open_workbook('report2.xls')

# sheet1 = rb1.sheet_by_index(0)
# sheet2 = rb2.sheet_by_index(0)

# for rownum in range(max(sheet1.nrows, sheet2.nrows)):
#     if rownum < sheet1.nrows:
#         row_rb1 = sheet1.row_values(rownum)
#         row_rb2 = sheet2.row_values(rownum)

#         for colnum, (c1, c2) in enumerate(zip_longest(row_rb1, row_rb2)):
#             if c1 != c2:
#                 print("Row {} Col {} - {} != {}".format(rownum+1, colnum+1, c1, c2))
#     else:
#         print("Row {} missing".format(rownum+1))


"""
NEW ONE
"""

# import pandas as pd

# df1 = pd.read_excel('Actual_File_1.xls')
# df2 = pd.read_excel('TestReportLayout.xls')

# difference = df1[df1!=df2]
# print(difference)


"""
another one
"""
# import pandas as pd

# filename1 = 'Actual_File_1.xls'
# filename2 = 'Actual_File_2.xls'

# df1 = pd.read_excel(filename1, index_col=0)
# df2 = pd.read_excel(filename2, index_col=0)

# df_merged = pd.merge(df1, df2, left_index=True, right_index=True, how='outer', sort=False, indicator=True)

# id_new = df_merged.index[df_merged['_merge'] == 'right_only'] 
# id_deleted = df_merged.index[df_merged['_merge'] == 'left_only'] 
# id_changed_data1 = df_merged.index[(df_merged['_merge'] == 'both') & (df_merged['Data1_x'] != df_merged['Data1_y'])]
# id_changed_data3 = df_merged.index[(df_merged['_merge'] == 'both') & (df_merged['Data3_x'] != df_merged['Data3_y'])]

# print(id_changed_data3)
"""
another new method
"""

# with open('old.csv', 'r') as t1:
#     old_csv = t1.readlines()
# with open('new.csv', 'r') as t2:
#     new_csv = t2.readlines()

# with open('update.csv', 'w') as out_file:
#     line_in_new = 0
#     line_in_old = 0
#     while line_in_new < len(new_csv) and line_in_old < len(old_csv):
#         if old_csv[line_in_old] != new_csv[line_in_new]:
#             out_file.write(new_csv[line_in_new])
#         else:
#             line_in_old += 1
#         line_in_new += 1

import xlrd
import pandas as pd

file1 = pd.read_excel("Actual_File_1.xls")
file2 = pd.read_excel("report2.xls")

for f in file1:
    if f in file2:
        print("Same")
    else:
        print(f)