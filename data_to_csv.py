# This script will take a dict of names and dates, and insert them into an excel spreadsheet
import pandas as pd
import openpyxl


data = [{"name" : "Walter Chang", "date" : "Tuesday, May 17, 2022"}, {"name" : "Michael Moreland", "date" : "Thursday, May 19, 2022"}]
# df = {'first_name' : [], 'last_name' : [], 'date': []}
# for row in data:
#     name = row['name'].split(' ')
#     df['first_name'].append(name[0])
#     df['last_name'].append(name[len(name)-1])
#     df['date'].append(row['date'])
# FILE_NAME = '../demo1.xlsx'
# print(df)

df_with_new_data = pd.DataFrame.from_dict(data, index=False)

# Reading the demo1.xlsx
df_with_existing_data=pd.read_excel("../data/existing_data.xlsx", index=False)
print(df_with_existing_data)

df_with_combined_data=pd.concat([df_with_new_data,df_with_existing_data])

df_with_combined_data=df_with_combined_data.to_excel('../data/combined.xlsx')
