from numpy.lib.npyio import mafromtxt
import pandas_datareader as pdr
import quandl as ql
import pandas as pd
import numpy as np
import sqlalchemy
from sqlalchemy import create_engine
import mysql.connector
from datetime import datetime, timedelta
from configparser import ConfigParser 
import pyEX
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
cursor.execute("CREATE DATABASE iexcloud")
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

my_cursor = mydb.cursor()


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
tickerSOI = os.path.join(directory, 'MacroDBv2SOI.csv')
#datesList = os.path.join(directory, 'dateslist.csv')

tickers = pd.read_csv(tickerSOI, engine='python')
#days = pd.read_csv(datesList, engine='python')

maintable = pd.DataFrame()

for index,row in tickers.iterrows():

    symbol = row['Ticker']
    #print(symbol)
    tablename = row['Table']

    my_cursor = mydb.cursor()
    query= "SELECT DATE FROM {} ORDER BY DATE DESC LIMIT 1".format(tablename)
    my_cursor.execute(query)
    LastRecord = my_cursor.fetchall()
    LastDate = LastRecord[0][0]
    #print(LastDate)
    #convert the str above to datetime in format below
    #need to add a condition to handle holidays and fridays
    #use days = 3 for friday - skip additional day for holiday
    start = LastDate #+ timedelta(days=1)
    #end = datetime.today()
    df = get_historical_data(symbol, start, token = key, output_format='pandas')
    #print(df)
    df.index.names = ['date']
    df = df.drop(LastDate)
    df = df[['symbol','close','high','low','open','volume']]
    #df = df.drop('volume',1)
    df.to_sql(tablename, engine, if_exists='append')
    print(df)
    maintable = pd.concat([df, maintable])
    #print(maintable)
    maintable.index.names = ['date'] 
    print("Appended " + tablename)

#print(maintable)
maintable.to_csv('pricecheck.csv')










