from sql_query import *
from create_table import *
from excel_merge import *

if __name__ == '__main__':
    mcamp_names = []
    mcamp_id = []
    mcamp_tracker_id = []
    mcamp = fetch_mcamp()
    mcamp = mcamp[mcamp["Campaign Status"]>=2]
    for i in range(len(mcamp)):
        if mcamp.loc[i, "Campaign Status"] >= 2:
            mcamp_names.append(mcamp.at[i, "Campaign Name"])
            mcamp_id.append(mcamp.at[i, "Campaign ID"])
            mcamp_tracker_id.append(mcamp.at[i, "Tracker ID"])
        else:
            continue
    mcamp_dict = dict(zip(mcamp_names, mcamp_id))
    mcamp_webt_dict = dict(zip(mcamp_id, mcamp_tracker_id))

    start_val = 'N'
    while start_val.upper() != 'Y':
        if start_val.upper() == 'N':
            for i in range(len(mcamp_names)):
                print(f"{i+1}.  {mcamp_names[i]}")
            
            to_export = input('Which Mail Campaigns do you want exported? (If multiple, separate with comma. e.g. 1, 2, 3. If all, type in all) \n')
            mcamp_to_export = []
            if to_export.upper() == "ALL":
                mcamp_to_export = mcamp_names
            else:
                to_export = list(to_export.split(','))
                for i in range(len(to_export)):
                    try:
                        if int(to_export[i]) <= len(mcamp_names):
                            mcamp_to_export.append(mcamp_names[int(to_export[i])-1])
                        else:
                            print(f"Invalid choice: {to_export[i]}")
                    except:
                        print(f"Invalid input: {to_export[i]}")
            if mcamp_to_export != []:
                for i in mcamp_to_export:
                    print(i)
                start_val = input('Export listed Mail Campaigns? (Y/N): ')
        else:
            print("Invalid input")
            start_val = input("Export listed Mail Campaigns? (Y/N):  \n")
    id_to_export = []
    webt_id_to_export = []
    for i in mcamp_to_export:
        id_to_export.append(mcamp_dict[i])
        webt_id_to_export.append(mcamp_webt_dict[mcamp_dict[i]])
    
    table_data = fetch_data(mcamp_to_export, id_to_export, webt_id_to_export)
    mcamp_table(table_data[0], table_data[1], table_data[2], table_data[3], table_data[4])
    merge_csv()