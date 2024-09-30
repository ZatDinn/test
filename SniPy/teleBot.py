import telebot
import dataframe_image as dfi
import os
from sql_query import *

def start_data():
    global mcamp_dict, mcamp_webt_dict
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

def create_mcamp_inline_buttons():
    markup = telebot.types.InlineKeyboardMarkup()
    for key, value in mcamp_dict.items():
        button = telebot.types.InlineKeyboardButton(key, callback_data=value)
        markup.add(button)
    return markup

user_responses = []

bot = telebot.TeleBot(variables.token, parse_mode=None)
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Hello! Use /update to get update on SniperPhish data.")

@bot.message_handler(commands=['update'])
def send_inline_buttons(message):
    start_data()
    markup = create_mcamp_inline_buttons()
    bot.send_message(message.chat.id, "Choose a Mail Campaign:", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data in mcamp_dict.values())
def handle_callback(call):
    user_responses.append(call.data)
    user_info = fetch_mcamp_live(call.data)
    cid_list = []
    for i in range(len(user_info["Client ID"])):
        cid_list.append(user_info["Client ID"][i])
    ws = fetch_webform_submit(mcamp_webt_dict[call.data], cid_list)
    wv = fetch_webpage_visit(mcamp_webt_dict[call.data], cid_list)
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
    dfi.export(new_df, "data.png", table_conversion='matplotlib')
    msg = f"""
Here are the updates for selected mail campaigns.
Selected Mail Campaign: {next((k for k, v in mcamp_dict.items() if v == call.data), None)}
Number of Page Visits: {visit}
Number of Form Submissions: {form_submissions}
        """
    bot.edit_message_text(text=msg, message_id=call.message.message_id, chat_id=call.message.chat.id)
    bot.send_photo(call.message.chat.id, photo=open(r"C:\Users\izati\Desktop\sniperphish\SniPy\data.png", 'rb'))
    os.remove(r"C:\Users\izati\Desktop\sniperphish\SniPy\data.png")
    
bot.infinity_polling()