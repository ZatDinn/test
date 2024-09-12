import mysql.connector
import pandas as pd
import dataframe_image as dfi
import var
import datetime
import pytz
from mysql.connector import Error

global tz
tz = pytz.timezone('Asia/Singapore')

def create_connection(host_name, user_name, user_password, db_name):
    """Establish a connection to the MySQL database."""
    try:
        connection = mysql.connector.connect(
            host=host_name,
            user=user_name,
            passwd=user_password,
            database=db_name
        )
        # print("Connection to MySQL DB successful")
        return connection
    except Error as e:
        print(f"The error '{e}' occurred while connecting to the database")
        return None

def fetch_mcamp(tb_name):
    # Fetch the list of mail campaigns from the database
    try:
        connection = create_connection(var.host, var.user, var.password, var.database)
        cursor = connection.cursor()
        query = f"SELECT campaign_id, campaign_name, campaign_data, camp_status FROM {tb_name}"
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
            mcamp_df.loc[i, "Tracker ID"] = b
        return mcamp_df
    except Error as e:
        print(f"The error '{e}' occurred while executing the query")
        return None

def fetch_webt(tb_name):
    # Fetch the list of web trackers from the database
    try:
        connection = create_connection(var.host, var.user, var.password, var.database)
        cursor = connection.cursor()
        query = f"SELECT tracker_id, tracker_name FROM {tb_name}"
        cursor.execute(query)
        data = cursor.fetchall()
        # print(f"Fetched data from table: {tb_name}")
        connection.close()
        return pd.DataFrame(data, columns=["Tracker ID", "Tracker Name"])
    except Error as e:
        print(f"The error '{e}' occurred while executing the query")
        return None

def fetch_user_info(tb_name, mcamp):
    # Fetch the list of users from the database
    try:
        connection = create_connection(var.host, var.user, var.password, var.database)
        cursor = connection.cursor()
        query = f"SELECT id, user_name, user_email, sending_status, send_time, mail_open_times FROM {tb_name} WHERE campaign_id='{mcamp}'"
        cursor.execute(query)
        data = cursor.fetchall()
        # print(f"Fetched data from table: {tb_name}")
        connection.close()
        user_info = pd.DataFrame(data, columns=["ID", "User Name", "Email Address", "Status", "Sent Time", "Mail Open"])
        for i in range(len(user_info["ID"])):
            if user_info.loc[i, "Status"] == 2:
                user_info.loc[i, "Status"] = "Sent"
            else:
                user_info.loc[i, "Status"] = "Not Sent"
            user_info.at[i, "Sent Time"] = datetime.datetime.fromtimestamp(int(user_info.loc[i, "Sent Time"])/1000, tz).strftime('%Y-%m-%d, %H:%M:%S')
            if  user_info.loc[i, "Mail Open"] != None:
                user_info.loc[i, "Mail Open"] = "Yes"
            else:
                user_info.loc[i, "Mail Open"] = "No"
        return user_info
    except Error as e:
        print(f"The error '{e}' occurred while executing the query")
        return None

def fetch_webform_data(tb_name, webt):
    try:
        connection = create_connection(var.host, var.user, var.password, var.database)
        cursor = connection.cursor()
        query = f"SELECT cid, public_ip, browser, platform, ip_info, page, form_field_data FROM {tb_name} WHERE tracker_id='{webt}'"
        cursor.execute(query)
        data = cursor.fetchall()
        # print(f"Fetched data from table: {tb_name}")
        connection.close()
        return pd.DataFrame(data, columns=["Client ID", "Public IP", "Browser", "Platform", "Country", "Page Visit", "Field-usrid2"])
    except Error as e:
        print(f"The error '{e}' occurred while executing the query")
        return None

def fetch_webpage_visit(tb_name, webt, user_id):
    try:
        connection = create_connection(var.host, var.user, var.password, var.database)
        for i in range(len(user_id)):
            cursor = connection.cursor()
            query = f"SELECT id, cid, tracker_id FROM {tb_name} WHERE tracker_id='{webt}'"
        cursor.execute(query)
        data = cursor.fetchall()
        # print(f"Fetched data from table: {tb_name}")
        connection.close()
        return pd.DataFrame(data, columns=["ID", "Client ID", "Tracker ID"])
    except Error as e:
        print(f"The error '{e}' occurred while executing the query")
        return None

def mass_export(user_info, webform_data, filename):
    df1 = pd.DataFrame(user_info)
    df2 = pd.DataFrame(webform_data)
    if len(df2["Client ID"].to_list()) != 0 and set(df2["Client ID"].to_list()).issubset(df1["ID"].to_list()) == True:
        df2_dict = df2.to_dict()
        country = []
        field_usrid2 = []
        field_pass = []
        country_dict = df2_dict["Country"]
        field_dict = df2_dict["Field-usrid2"]
        df2.insert(len(df2.columns), "Field-password", None)
        df2.insert(6, "Form Submission", None)
        df2.insert(7, "P1 Submission", None)
        for i in range(len(df2["Client ID"])):
        # Change from dict to string (country)
            new_country_dict = eval(country_dict[i])
            country.append(new_country_dict["country"])
            df2.at[i, "Country"] = country[i]
                # else:
                #     country.append(None)
            if df2.at[i, "Page Visit"] == 1:
                df2.at[i, "Page Visit"] = "Yes"
            else:
                df2.at[i, "Page Visit"] = "No"
                    
            if user_info["ID"][i] in webform_data["Client ID"].to_list():
                df2.loc[i, "Form Submission"] = True
                df2.loc[i, "P1 Submission"] = True
            else:
                df2.loc[i, "Form Submission"] = False
                df2.loc[i, "P1 Submission"] = False
            # Change from dict to string (Field-usrid2 & Field-password)
            new_field_dict = eval(field_dict[i])
            keys = list(new_field_dict.keys())
            field_usrid2.append(new_field_dict[keys[0]])
            field_pass.append(new_field_dict[keys[1]])
            df2.at[i, "Field-usrid2"] = field_usrid2[i]
            df2.at[i, "Field-password"] = field_pass[i]
        new_df = df1.join(df2.set_index("Client ID"), on="ID")
        new_df.drop("ID", axis=1, inplace=True)
    else:
        new_df = df1.join(pd.DataFrame(
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
            }, index=df1.index
        ))
        new_df.drop("ID", axis=1, inplace=True)

    new_df.to_csv(f"{filename}.csv", index=False)
