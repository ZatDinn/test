from sql_query import *

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

for i in range(len(mcamp_names)):
    print(f"{i+1}.  {mcamp_names[i]}")
    
to_update = input('Which Mail Campaigns do you want updated? (If multiple, separate with comma. e.g. 1, 2, 3. If all, type in all) \n')

for i in range(len(to_update)):
    try:
        if int(to_update[i]) <= len(mcamp_names):
            mcamp_to_update = mcamp_names[int(to_update[i])-1]
        else:
            print(f"Invalid choice: {to_update[i]}")
    except:
        print(f"Invalid input: {to_update[i]}")

user_info = fetch_mcamp_live(mcamp_dict[mcamp_to_update])
cid_list = []
for i in range(len(user_info["Client ID"])):
    cid_list.append(user_info["Client ID"][i])
ws = fetch_webform_submit(mcamp_webt_dict[mcamp_dict[mcamp_to_update]], cid_list)
wv = fetch_webpage_visit(mcamp_webt_dict[mcamp_dict[mcamp_to_update]], cid_list)

visit = 0
form_submissions = 0
for i in range(len(ws["Page Visit"])):
    if ws.at[i, "Page Visit"] == 1:
        visit+=1
for i in range(len(ws["Field-usrid2"])):
    if ws.at[i, "Field-usrid2"] != None:
        form_submissions+=1
        
if len(wv["Client ID"].to_list()) != 0 and set(wv["Client ID"].to_list()).issubset(ws["Client ID"].to_list()) == True:
    wv_dict = wv.to_dict()
    ws_dict = ws.to_dict()
    df = user_info.merge(wv.set_index("Client ID"), on="Client ID")
    df = df.join(pd.DataFrame(
    {
        "Form Submission":"Yes",
        "P1 Submission":"Yes",
    }, index=df.index
    ))
    new_df = df.merge(ws.set_index("Client ID"), on="Client ID")
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
    new_df = user_info.join(pd.DataFrame(
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
    }, index=user_info.index
    ))
print(f"""
Here are the updates for selected mail campaigns.
Selected Mail Campaign: {mcamp_to_update}
Number of Page Visits: {visit}
Number of Form Submissions: {form_submissions}

{new_df}
      """)

