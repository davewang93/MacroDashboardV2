import pandas as pd 
import numpy as np
import glob
import os
from sqlalchemy import create_engine
import mysql.connector
from datetime import datetime, timedelta
from configparser import ConfigParser 
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

mydb = mysql.connector.connect(
    host = host,
    user = user,
    passwd = passwd,
    database = database,
)

#connect to db using sqlalchemy
engine = create_engine(engine)

my_cursor = mydb.cursor()

path = os.path.join(directory, 'correlations.csv')
#datesList = os.path.join(directory, 'dateslist.csv')

sheet = pd.read_csv(path, engine='python')

tickers = sheet['Tickers']
columns = sheet['Column']
columns = columns.iloc[::-1]

path2 = os.path.join(directory, 'correlations2.csv')
#datesList = os.path.join(directory, 'dateslist.csv')

sheet2 = pd.read_csv(path2, engine='python')

tickers2 = sheet2['Tickers']
columns2 = sheet2['Column']
columns2 = columns2.iloc[::-1]

def corr_table(days,tickers,columns):

    maintable = pd.DataFrame()

    for i in tickers:
        query= "SELECT * FROM {} ORDER BY Date DESC LIMIT {}".format(i,days)
        df = pd.read_sql(query, con = engine)
        df = df[['date','close']]
        df['date'] =pd.to_datetime(df.date)
        df = df.sort_values(by='date')
        df = df.set_index('date')
        df['close'] = pd.to_numeric(df['close'])
        df = df[~df.index.duplicated(keep='first')]
        maintable = pd.concat([df,maintable], axis = 1)
        #print(maintable)

    maintable.columns = columns
    maintable = maintable.pct_change()
    maintable.to_csv(r'D:\OneDrive\David\src\MacroDashboardV2\apps\correlations\{}check.csv'.format(days))
    maintable = maintable.corr().stack().rename_axis(('a', 'b')).reset_index(name='corr')
    mask_dups = (maintable[['a', 'b']].apply(frozenset, axis=1).duplicated()) | (maintable['a']==maintable['b']) 
    maintable = maintable[~mask_dups].reset_index().drop(columns='index')
    print(maintable)
    return maintable


df = corr_table(5,tickers,columns)
df.to_csv(r'D:\OneDrive\David\src\MacroDashboardV2\apps\correlations\{}day.csv'.format(5))
df = corr_table(21,tickers,columns)
df.to_csv(r'D:\OneDrive\David\src\MacroDashboardV2\apps\correlations\{}day.csv'.format(21))
df = corr_table(63,tickers,columns)
df.to_csv(r'D:\OneDrive\David\src\MacroDashboardV2\apps\correlations\{}day.csv'.format(63))
df = corr_table(126,tickers,columns)
df.to_csv(r'D:\OneDrive\David\src\MacroDashboardV2\apps\correlations\{}day.csv'.format(126))
df = corr_table(252,tickers,columns)
df.to_csv(r'D:\OneDrive\David\src\MacroDashboardV2\apps\correlations\{}day.csv'.format(252))
df = corr_table(756,tickers,columns)
df.to_csv(r'D:\OneDrive\David\src\MacroDashboardV2\apps\correlations\{}day.csv'.format(756))

df = corr_table(5,tickers2,columns2)
df.to_csv(r'D:\OneDrive\David\src\MacroDashboardV2\apps\correlations\{}day.csv'.format('mini5'))
df = corr_table(21,tickers2,columns2)
df.to_csv(r'D:\OneDrive\David\src\MacroDashboardV2\apps\correlations\{}day.csv'.format('mini21'))
df = corr_table(63,tickers2,columns2)
df.to_csv(r'D:\OneDrive\David\src\MacroDashboardV2\apps\correlations\{}day.csv'.format('mini63'))
df = corr_table(126,tickers2,columns2)
df.to_csv(r'D:\OneDrive\David\src\MacroDashboardV2\apps\correlations\{}day.csv'.format('mini126'))
df = corr_table(252,tickers2,columns2)
df.to_csv(r'D:\OneDrive\David\src\MacroDashboardV2\apps\correlations\{}day.csv'.format('mini252'))
df = corr_table(756,tickers2,columns2)
df.to_csv(r'D:\OneDrive\David\src\MacroDashboardV2\apps\correlations\{}day.csv'.format('mini756'))
