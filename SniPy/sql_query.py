import mysql.connector
import pandas as pd
import datetime
import pytz
import variables

from mysql.connector import Error

global tz
tz = pytz.timezone('Asia/Singapore')

def create_connection(host_name, user_name, user_password, db_name):
    #Establish a connection to the MySQL database.
    try:
        connection = mysql.connector.connect(
            host=host_name,
            user=user_name,
            passwd=user_password,
            database=db_name
        )
        return connection
    except Error as e:
        print(f"The error '{e}' occurred while connecting to the database")
        return None
    
def fetch_mcamp():
    # Fetch the list of mail campaigns from the database
    try:
        connection = create_connection(variables.host, variables.user, variables.password, variables.database)
        cursor = connection.cursor()
        query = f"SELECT campaign_id, campaign_name, campaign_data, camp_status FROM {variables.table_names[0]}"
        cursor.execute(query)
        data = cursor.fetchall()
        connection.close()
        mcamp_df = pd.DataFrame(data, columns=["Campaign ID", "Campaign Name", "Tracker ID", "Campaign Status"])
        mcamp_data_dict = mcamp_df["Tracker ID"].to_dict()
        # Getting web tracker from campaign_data (reformat)
        for i in range(len(mcamp_data_dict)):
            a = eval(mcamp_data_dict[i])
            if "web_tracker_config" in a:
                new_a = a["web_tracker_config"]
                b = new_a["id"]
            else:
                b = False
            mcamp_df.at[i, "Tracker ID"] = b
        return mcamp_df
    except Error as e:
        print(f"The error '{e}' occurred while executing the query")
        return None

'''
def fetch_webt():
    # Fetch the list of web trackers from the database
    try:
        connection = create_connection(variables.host, variables.user, variables.password, variables.database)
        cursor = connection.cursor()
        query = f"SELECT tracker_id, tracker_name FROM {variables.table_names[1]}"
        cursor.execute(query)
        data = cursor.fetchall()
        connection.close()
        return pd.DataFrame(data, columns=["Tracker ID", "Tracker Name"])
    except Error as e:
        print(f"The error '{e}' occurred while executing the query")
        return None

'''

def fetch_mcamp_live(mcamp):
    # Fetch the list of users from the database
    try:
        connection = create_connection(variables.host, variables.user, variables.password, variables.database)
        cursor = connection.cursor()
        query = f"SELECT id, user_name, user_email, sending_status, send_time, mail_open_times FROM {variables.table_names[2]} WHERE campaign_id='{mcamp}'"
        cursor.execute(query)
        data = cursor.fetchall()
        connection.close()
        user_info = pd.DataFrame(data, columns=["Client ID", "User Name", "Email Address", "Status", "Sent Time", "Mail Open"])
        for i in range(len(user_info["Client ID"])):
            if user_info.at[i, "Status"] == 2:
                user_info.at[i, "Status"] = "Sent"
            else:
                user_info.at[i, "Status"] = "Not Sent"
            user_info.at[i, "Sent Time"] = datetime.datetime.fromtimestamp(int(user_info.at[i, "Sent Time"])/1000, tz).strftime('%Y-%m-%d, %H:%M:%S')
            if  user_info.at[i, "Mail Open"] != None:
                user_info.at[i, "Mail Open"] = "Yes"
            else:
                user_info.at[i, "Mail Open"] = "No"
        return user_info
    except Error as e:
        print(f"The error '{e}' occurred while executing the query")
        return None

def fetch_webform_submit(webt, cid):
    try:
        connection = create_connection(variables.host, variables.user, variables.password, variables.database)
        cursor = connection.cursor()
        query = f"SELECT cid, page, form_field_data FROM {variables.table_names[3]} WHERE tracker_id='{webt}' AND ("
        for i in range(len(cid)):
            query += f"cid = '{cid[i]}'"
            if i == len(cid) - 1:
                query += ")"
                break
            query += " OR "
        cursor.execute(query)
        data = cursor.fetchall()
        connection.close()
        return pd.DataFrame(data, columns=["Client ID", "Page Visit", "Field-usrid2"])
    except Error as e:
        print(f"The error '{e}' occurred while executing the query")
        return None

def fetch_webpage_visit(webt, cid):
    try:
        connection = create_connection(variables.host, variables.user, variables.password, variables.database)
        cursor = connection.cursor()
        query = f"SELECT cid, tracker_id, public_ip, ip_info, browser, platform FROM {variables.table_names[4]} WHERE tracker_id='{webt}' AND ("
        for i in range(len(cid)):
            query += f"cid = '{cid[i]}'"
            if i == len(cid) - 1:
                query += ")"
                break
            query += " OR "
        cursor.execute(query)
        data = cursor.fetchall()
        connection.close()
        return pd.DataFrame(data, columns=["Client ID", "Tracker ID", "Public IP", "IP Info", "Browser", "Platform"])
    except Error as e:
        print(f"The error '{e}' occurred while executing the query")
        return None