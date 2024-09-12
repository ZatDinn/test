from main import *
from data_export import *
from excel_merge import merge_csv

# function to get mail campaign info from sql
def get_mcamp_info():
    global mcamp, mcamp_names, mcamp_id, mcamp_tracker_id
    mcamp = fetch_mcamp(var.table_names[0])
    mcamp_names = []
    mcamp_id = []
    mcamp_tracker_id = []
    mcamp = mcamp[mcamp["Campaign Status"]!=0]
    for i in range(len(mcamp)):
        if mcamp.loc[i, "Campaign Status"] != 0:
            mcamp_names.append(mcamp.at[i, "Campaign Name"])
            mcamp_id.append(mcamp.at[i, "Campaign ID"])
            mcamp_tracker_id.append(mcamp.at[i, "Tracker ID"])
        else:
            continue

get_mcamp_info()

# display mail campaigns
for i in range(len(mcamp_names)):
    print(f"{i+1}. {mcamp_names[i]}")

# while loop to loop as long as criteria is not met
start_val = "N"
while start_val.upper() != "Y":
    if start_val.upper() == "N":
        val = input("Select which to export (if multiple, separate with comma e.g. 1,2,3): \n")
        val = list(val.split(","))
        to_export = []
        for i in range(len(val)):
            try:
                if  int(val[i]) <= len(mcamp_names):
                    to_export.append(int(val[i]))
                else:
                    print(f"Invalid choice: {val[i]}")
            except:
                print(f"Invalid input: {val[i]}")
        print(to_export)
        if to_export != []:
            for i in to_export:
                print(f"{mcamp_names[i-1]}")
            start_val = input("Are you sure you want to export the selected campaigns? (Y/N): \n")
    else:
        print("Invalid input")
        start_val = input("Are you sure you want to export the selected campaigns? (Y/N): \n")

# exporting to .xlsx file
try:
    user_info = []
    webform_data = []
    mcamp_id_list = []
    webt_id_list = []
    for i in to_export:
        mcamp_id_list.append(mcamp_id[i-1])
        webt_id_list.append(mcamp_tracker_id[i-1])
    for mcamp_id in mcamp_id_list:
        user_info.append(fetch_user_info(var.table_names[2], mcamp_id))
    for webt_id in webt_id_list:
        webform_data.append(fetch_webform_data(var.table_names[3], webt_id))
    for i in range(len(user_info)):
        mass_export(user_info[i], webform_data[i], f"{mcamp_names[i]}")
    merge_csv()
    print("Export Successful!")
except:
    print("Export Failed!")