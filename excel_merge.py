import pandas as pd
import os
import re
import var

# function to ensure text from csv, when merged, can be read (sanitized)
def sanitize_sheet_name(name):
    # Remove invalid characters and shorten to 31 characters
    name = re.sub(r'[\\/*?[\]]', '', name)
    return name[:31]

# function to merge csv files created
def merge_csv():
    with pd.ExcelWriter(var.excel_path, engine='openpyxl') as writer:
        for filename in os.listdir(var.directory):
            if filename.endswith('.csv'):
                file_path = os.path.join(var.directory, filename)
                try:
                    df = pd.read_csv(file_path)

                    sheet_name = sanitize_sheet_name(os.path.splitext(filename)[0])

                    df.to_excel(writer, sheet_name=sheet_name, index=False)
                    
                    # Delete used csv file
                    os.remove(file_path)
                except Exception as e:
                    print(f"Error processing file {filename}: {e}")

    print("Workbook created with sanitized sheet names!")