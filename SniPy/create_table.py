import pandas as pd
from sql_query import *

def fetch_data(selected_mcamp_names, selected_mcamp_id, selected_mcamp_tracker):
    
    cid_list = []
    mcamp_live_list = []
    for i in range(len(selected_mcamp_id)):
        mcamp_live = fetch_mcamp_live(selected_mcamp_id[i])
        cid_list.append(mcamp_live["Client ID"])
        mcamp_live_list.append(mcamp_live)
    
    ws_list = []
    wv_list = []

    for i in range(len(selected_mcamp_id)):
        ws_list.append(fetch_webform_submit(selected_mcamp_tracker[i],  cid_list[i]))
        wv_list.append(fetch_webpage_visit(selected_mcamp_tracker[i],  cid_list[i]))
    return cid_list, ws_list, wv_list, mcamp_live_list, selected_mcamp_names


def mcamp_table(cidlist, wslist, wvlist, mcamp_data, mcamp_name):
    for i in range(len(cidlist)):
        filename = mcamp_name[i]
        if len(wvlist[i]["Client ID"].to_list()) != 0 and set(wvlist[i]["Client ID"].to_list()).issubset(wslist[i]["Client ID"].to_list()) == True:
            
            wv_dict = wvlist[i].to_dict()
            ws_dict = wslist[i].to_dict()
            df = mcamp_data[i].merge(wvlist[i].set_index("Client ID"), on="Client ID")
            df = df.join(pd.DataFrame(
                {
                    "Form Submission":"Yes",
                    "P1 Submission":"Yes",
                }, index=df.index
            ))
            new_df = df.merge(wslist[i].set_index("Client ID"), on="Client ID")
            new_df = new_df.join(pd.DataFrame(
                {
                    "Field-password":None
                }, index=new_df.index
            ))
            new_df.drop("Client ID", axis=1, inplace=True)
            new_df.drop("Tracker ID", axis=1, inplace=True)
            new_df.rename(columns={"IP Info":"Country"}, inplace=True)
            for j in range(len(wv_dict["IP Info"])):
                ip_info = eval(wv_dict["IP Info"][j])
                new_df.at[j, "Country"] = ip_info["country"]
                if new_df.at[j, "Page Visit"] == 1:
                    new_df.at[j, "Page Visit"] = "Yes"
                else:
                    new_df.at[j, "Page Visit"] = "No"
                field_usrid2 = eval(ws_dict["Field-usrid2"][j])
                new_df.at[j, "Field-usrid2"] = field_usrid2["usrid2"]
                new_df.at[j, "Field-password"] = field_usrid2["password"]
            
            cols = new_df.columns.to_list()
            col_move = cols.pop(11)
            cols.insert(9, col_move)
            new_df = new_df[cols]
        else:
            new_df = mcamp_data[i].join(pd.DataFrame(
            {
                "Public IP":None,
                "Browser":None,
                "Platform":None,
                "Country":None,
                "Page Visit":"No",
                "Form Submission":"No",
                "P1 Submission":"No",
                "Field-usrid2":None,
                "Form-password":None,
            }, index=mcamp_data[i].index
            ))
            new_df.drop("Client ID", axis=1, inplace=True)
            
        new_df.to_csv(f"{filename}.csv", index=False)