from data_export import *
from excel_merge import *

def export():
    mcamp = fetch_mcamp(var.table_names[0])
    mcamp_id_list = mcamp["Campaign ID"].to_list()
    mcamp_name_list = mcamp["Campaign Name"].to_list()
    webt = fetch_webt(var.table_names[1])
    webt_id_list = webt["Tracker ID"].to_list()
    webt_name_list = webt["Tracker Name"].to_list()
    user_info = []
    webform_data = []
    for mcamp_id in mcamp_id_list:
        user_info.append(fetch_user_info(var.table_names[2], mcamp_id))
    for webt_id in webt_id_list:
        webform_data.append(fetch_webform_data(var.table_names[3], webt_id))
    for i in range(len(user_info)):
        for j in range(len(webform_data)):
            mass_export(user_info[i], webform_data[j], f"{mcamp_name_list[i]} & {webt_name_list[j]}")
    merge_csv()

if __name__ == "__main__":
    export()
    """
    mcamp = fetch_mcamp(var.table_names[0])
    mcamp_id_list = mcamp["Campaign ID"].to_list()
    mcamp_name_list = mcamp["Campaign Name"].to_list()
    webt = fetch_webt(var.table_names[1])
    webt_id_list = webt["Tracker ID"].to_list()
    webt_name_list = webt["Tracker Name"].to_list()
    user_info = []
    webform_data = []
    for mcamp_id in mcamp_id_list:
        user_info.append(fetch_user_info(var.table_names[2], mcamp_id))
    for webt_id in webt_id_list:
        webform_data.append(fetch_webform_data(var.table_names[3], webt_id))
    for i in range(len(user_info)):
        for j in range(len(webform_data)):
            mass_export(user_info[i], webform_data[j], f"{mcamp_name_list[i]} & {webt_name_list[j]}")
    merge_csv()
    """
    