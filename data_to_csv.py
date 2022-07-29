# This script will take a dict of names and dates, and insert them into an excel spreadsheet
import pandas as pd
import os

class ExcelWriter:
    
    def writeToExcel(self, data, filename, path = ''):
        
        df_with_new_data = pd.DataFrame.from_dict(data, index=False)

        df_with_new_data.to_excel(os.path.join(path, filename))
