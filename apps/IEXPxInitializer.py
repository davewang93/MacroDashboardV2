import pandas_datareader as pdr
import pandas as pd
import numpy as np
from sqlalchemy import create_engine
import mysql.connector
from datetime import datetime, timedelta
from configparser import ConfigParser 
from iexfinance.stocks import get_historical_data
import os

#this stuff loads the keys
directory = os.path.dirname(os.path.abspath(__file__))
configfile = os.path.join(directory, 'config.ini')
parser = ConfigParser()
parser.read(configfile)

host = parser.get('macrodbv2','host')
user = parser.get('macrodbv2','user')
passwd = parser.get('macrodbv2','passwd')
database = parser.get('macrodbv2','database')

engine = parser.get('engines','macrodbv2')

#production key
secretkey = parser.get('keys','secretkey')
#sandbox key
testkey = parser.get('keys','testkey')

'''


# Create a new DB in mySQL w/ block below
mydb = mysql.connector.connect(
        host = host,
        user = user,
        passwd = passwd,
    )

#create cursor
cursor = mydb.cursor()

#create a db
cursor.execute("CREATE DATABASE macrodbv2")

'''

#connect to specific db w/ both mysql connector and sqlalchemy. sqlalchemy for pushing and mysql for pulling
mydb = mysql.connector.connect(
    host = host,
    user = user,
    passwd = passwd,
    database = database,
)

#connect to db using sqlalchemy
engine = create_engine(engine)

#this is the iexfinance client
#iexcloud-v1 is live
#iexcloud-sandbox is sandbox
#secretkey = live testkey = sandbox
#need to make the switch in the environment variable too
os.environ['IEX_API_VERSION'] = 'iexcloud-v1'
key = secretkey   

#load SOI files and create useful vars
#test file 'DailyPricesListNewAdd.csv'
#live file 'DailyPricesList.csv'
tickerSOI = os.path.join(directory, 'MacroDBv2SOINew.csv')
#datesList = os.path.join(directory, 'dateslist.csv')

tickers = pd.read_csv(tickerSOI, engine='python')
#days = pd.read_csv(datesList, engine='python')

maintable = pd.DataFrame()

#for each ticker in the file, pulls price data for specified date, and pushes to mysql db under associated table name
for index,row in tickers.iterrows():
    #remember to toggle exchange
    start = "5/31/2017"
    end = "9/09/22"
    symbol = row['Ticker']
    tablename = row['Table']
    df = get_historical_data(symbol, start,end, token = key, output_format='pandas')
    df.index.names = ['date']
    df = df[['symbol','close','high','low','open','volume']]
    print("Appended " + tablename)
    df.to_sql(tablename, engine, if_exists='append')














