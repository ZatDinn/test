# SniperPhish Mass Export & Update

## Description
This is a simple Python (ver. 3.12.3) script that connects to the SniperPhish database to return updates and semi-automatically mass exports mail campaign data based on pre-built SniperPhish export feature.

The program utilizes the following Python packages:
1. mysql-connector-python (Python MySQL connector package)
2. pandas (Python data analytics and table image generator package)
3. datetime and pytz (Python datetime, UNIX timestamp, and GMT converter package)
4. os (Python file manipulation package)

## Installation
To install the required libraries, run the following command in your terminal:
```
pip install python-telegram-bot
pip install pandas
pip install dataframe_image
pip install mysql-connector-python
pip install pytz
pip install openpyxl
pip install matplotlib
```
## Usage
To run the mass export feature:
'''
python3 main.py
'''

To run the update feature:
'''
python3 update.py
'''