from datetime import datetime
from pathlib import Path

# Connection variables
host = 'localhost'
user = 'root'
password = None
database = 'sniperphish'

# SQL table names
table_names = [
    "tb_core_mailcamp_list",
    "tb_core_web_tracker_list",
    "tb_data_mailcamp_live",
    "tb_data_webform_submit",
    "tb_data_webpage_visit"
]

# Excel File name
current_date = datetime.now().strftime("%Y-%m-%d")
excel_path = f"Mass_Export_{current_date}.xlsx"
directory = Path.cwd()

#telegram bot token
token = '7204375664:AAGO9Rwoz2OHXQfqinsttQPY0vzxvBdwGvQ'