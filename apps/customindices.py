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

path = r'D:\OneDrive\David\src\MacroDashboardV2\apps\CustomIndexSOIs'
csv_files = glob.glob(os.path.join(path, "*.csv"))

datetable = pd.DataFrame()

for f in csv_files:

    tickers = pd.read_csv(f, header = None).values.tolist()
    tickers = [var for sublist in tickers for var in sublist]
    fname = f.split("\\")[-1]
    fname = os.path.splitext(fname)[0]
    print(tickers)
    transtbl = pd.DataFrame()

    for i in tickers:
        query= "SELECT * FROM {}".format(i)
        df = pd.read_sql(query, con = engine)
        df = df[['date','close']]
        df = df.set_index('date')
        df['close'] = pd.to_numeric(df['close'])
        df.rename(columns={'close':i}, inplace= True)
        df = df[~df.index.duplicated(keep='first')]
        transtbl = pd.concat([df,transtbl], axis = 1)
        
        query= "SELECT * FROM {} ORDER BY date DESC LIMIT 1;".format(i)
        df2 = pd.read_sql(query, con = engine)
        datetable =  pd.concat([df2,datetable])
        #print(df2)
        #print(transtbl)

    #datetable =  pd.concat([datetableinner,datetable])
    transtbl = transtbl.replace(0, np.nan)
    transtbl = np.log10(transtbl)
    transtbl['Price'] = transtbl.mean(axis=1)
    #transtbl = transtbl[['Price']]
    transtbl = transtbl.dropna()
    transtbl.to_sql(fname, engine, if_exists='replace')

    suffix = '.csv'
    base_filename = fname
    dir = r'D:\OneDrive\David\src\MacroDashboardV2\apps\datecheck'
    path= os.path.join(dir, base_filename + suffix)
    datetable.to_csv(path)

    print(fname)
      