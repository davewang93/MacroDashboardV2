from re import sub
from numpy.core.einsumfunc import _einsum_path_dispatcher
import pandas as pd
from sqlalchemy import create_engine
import mysql.connector
from configparser import ConfigParser 
import os
import plotly.express as px
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.graph_objects as go
from datetime import timedelta

app = dash.Dash()

#this stuff loads the config file
directory = os.path.dirname(os.path.abspath(__file__))
configfile = os.path.join(directory, 'config.ini')
parser = ConfigParser()
parser.read(configfile)

#read credentials
fxhost = parser.get('pricedb','host')
fxuser = parser.get('pricedb','user')
fxpasswd = parser.get('pricedb','passwd')
fxdatabase = parser.get('pricedb','database')
fxengine = parser.get('engines','pricedbengine')

v2host = parser.get('macrodbv2','host')
v2user = parser.get('macrodbv2','user')
v2passwd = parser.get('macrodbv2','passwd')
v2database = parser.get('macrodbv2','database')
v2engine = parser.get('engines','macrodbv2')

v1host = parser.get('macrodashboard','host')
v1user = parser.get('macrodashboard','user')
v1passwd = parser.get('macrodashboard','passwd')
v1database = parser.get('macrodashboard','database')
v1engine = parser.get('engines','macrodbengine')

#connect to specific db w/ both mysql connector and sqlalchemy. sqlalchemy for pushing and mysql for pulling
fxdb = mysql.connector.connect(
    host = fxhost,
    user = fxuser,
    passwd = fxpasswd,
    database = fxdatabase,
)
#connect to db using sqlalchemy
fxengine = create_engine(fxengine)
fx_cursor = fxdb.cursor(buffered=True , dictionary=True)

v1db = mysql.connector.connect(
    host = v1host,
    user = v1user,
    passwd = v1passwd,
    database = v1database,
)
#connect to db using sqlalchemy
v1engine = create_engine(v1engine)
#create sql.connector cursor, often called "self"
v1_cursor = v1db.cursor()

v2db = mysql.connector.connect(
    host = v2host,
    user = v2user,
    passwd = v2passwd,
    database = v2database,
)
#connect to db using sqlalchemy
v2engine = create_engine(v2engine)
v2_cursor = v2db.cursor()

query = "SELECT * FROM audusd"
audusd = pd.read_sql(query, con = fxengine)
audusd =audusd[['time','mid.c']]
audusd.columns= ['date', 'audusd']
query = "SELECT * FROM eurusd"
eurusd = pd.read_sql(query, con = fxengine)
eurusd= eurusd[['time','mid.c']]
eurusd.columns= ['date', 'eurusd']
query = "SELECT * FROM gbpusd"
gbpusd = pd.read_sql(query, con = fxengine)
gbpusd= gbpusd[['time','mid.c']]
gbpusd.columns= ['date', 'gbpusd']
query = "SELECT * FROM usdchf"
usdchf = pd.read_sql(query, con = fxengine)
usdchf= usdchf[['time','mid.c']]
usdchf.columns= ['date', 'usdchf']
query = "SELECT * FROM usdcad"
usdcad = pd.read_sql(query, con = fxengine)
usdcad= usdcad[['time','mid.c']]
usdcad.columns= ['date', 'usdcad']
query = "SELECT * FROM usdjpy"
usdjpy = pd.read_sql(query, con = fxengine)
usdjpy= usdjpy[['time','mid.c']]
usdjpy.columns= ['date', 'usdjpy']
#print(usdjpy,gbpusd)


query = "SELECT * FROM opeccrude"
opeccrude = pd.read_sql(query, con = v1engine)
opeccrude.columns= ['date', 'opeccrude']
query = "SELECT * FROM 10yrtreasbenchmark"
tenyrtreasbenchmark = pd.read_sql(query, con = v1engine)
tenyrtreasbenchmark = tenyrtreasbenchmark.reset_index(drop=True) 
tenyrtreasbenchmark =tenyrtreasbenchmark[['Date','Value']]
tenyrtreasbenchmark.columns= ['date', 'tenyrtreasbenchmark']
query = "SELECT * FROM aaayieldidx"
aaayieldidx = pd.read_sql(query, con = v1engine)
aaayieldidx.columns= ['date', 'aaayieldidx']
query = "SELECT * FROM 10yrbrkevninf"
tenyrbrkevninf = pd.read_sql(query, con = v1engine)
tenyrbrkevninf = tenyrbrkevninf.reset_index(drop=True)
tenyrbrkevninf =tenyrbrkevninf[['Date','Value']]
tenyrbrkevninf.columns= ['date', 'tenyrbrkevninf']
#print(tenyrbrkevninf,usfedfundsrate)

#print(broadaeroanddefense.head())
query = "SELECT * FROM broadreits"
broadreits = pd.read_sql(query, con = v2engine)
broadreits= broadreits[['date','Price']]
broadreits.columns= ['date', 'broadreits']
query = "SELECT * FROM stapleagri"
stapleagri = pd.read_sql(query, con = v2engine)
stapleagri= stapleagri[['date','Price']]
stapleagri.columns= ['date', 'stapleagri']
query = "SELECT * FROM broadmetals"
broadmetals = pd.read_sql(query, con = v2engine)
broadmetals= broadmetals[['date','Price']]
broadmetals.columns= ['date', 'broadmetals']
query = "SELECT * FROM gld"
gld = pd.read_sql(query, con = v2engine)
gld = gld[['date','close']]
gld.columns= ['date', 'gld']
query = "SELECT * FROM broadoilandgas"
broadoilandgas = pd.read_sql(query, con = v2engine)
broadoilandgas = broadoilandgas[['date','Price']]
broadoilandgas.columns= ['date', 'broadoilandgas']
query = "SELECT * FROM broadfinancials"
broadfinancials = pd.read_sql(query, con = v2engine)
broadfinancials = broadfinancials[['date','Price']]
broadfinancials.columns= ['date', 'broadfinancials']
query = "SELECT * FROM broadconsumercore"
broadconsumercore = pd.read_sql(query, con = v2engine)
broadconsumercore = broadconsumercore[['date','Price']]
broadconsumercore.columns= ['date', 'broadconsumercore']
query = "SELECT * FROM voo"
voo = pd.read_sql(query, con = v2engine)
us = voo[['date','close']]
us.columns= ['date', 'us']
query = "SELECT * FROM mchi"
mchi = pd.read_sql(query, con = v2engine)
chn = mchi[['date','close']]
chn.columns= ['date', 'chn']
query = "SELECT * FROM ewj"
ewj = pd.read_sql(query, con = v2engine)
jpn = ewj[['date','close']]
jpn.columns= ['date', 'jpn']
query = "SELECT * FROM ewc"
ewc = pd.read_sql(query, con = v2engine)
can = ewc[['date','close']]
can.columns= ['date', 'can']
query = "SELECT * FROM ewu"
ewu = pd.read_sql(query, con = v2engine)
uk = ewu[['date','close']]
uk.columns= ['date', 'uk']
query = "SELECT * FROM ewg"
ewg = pd.read_sql(query, con = v2engine)
deu = ewg[['date','close']]
deu.columns= ['date', 'deu']
query = "SELECT * FROM ewa"
ewa = pd.read_sql(query, con = v2engine)
aus = ewa[['date','close']]
aus.columns= ['date', 'aus']
query = "SELECT * FROM ewq"
ewq = pd.read_sql(query, con = v2engine)
fr = ewq[['date','close']]
fr.columns= ['date', 'fr']
query = "SELECT * FROM gbtc"
gbtc = pd.read_sql(query, con = v2engine)
gbtc = gbtc[['date','close']]
gbtc.columns= ['date', 'gbtc']
query = "SELECT * FROM ethe"
ethe = pd.read_sql(query, con = v2engine)
ethe = ethe[['date','close']]
ethe.columns= ['date', 'ethe']
#print(ethe)

fx_list = (audusd,eurusd,gbpusd,
usdchf,usdcad,usdjpy,)

for i in fx_list:
     #i["date"] = pd.to_datetime(i["date"]).dt.strftime('%m-%d-%y')
     #i.set_index('date', inplace=True)
    i['date'] = pd.DatetimeIndex(i['date']) + pd.DateOffset(1)
    i['date'] = pd.to_datetime(i['date']).dt.strftime('%m-%d-%y')
     #var = i[['date']]
    i.set_index('date', inplace=True)
     #print(var)
     #print(var.dtypes)
     #pd.DatetimeIndex(i.date) +pd.DateOffset(1)
     #i['date'] = i[['date']] + timedelta(days=1)
     #print(i[['date']])
     #i['date'] = i['date'] + timedelta(days=1)
     #i.set_index('date', inplace=True)

'''
#fx_list = fx_list['date'] + timedelta(days=1)

df = pd.concat(fx_list, axis=1, join='inner')

df.to_csv('fxtest.csv')

#print(df)
'''
custom_indices = (broadreits,stapleagri,broadmetals,
broadoilandgas,broadfinancials,
broadconsumercore)

for i in custom_indices:
    i['date'] = pd.to_datetime(i['date']).dt.strftime('%m-%d-%y')
    i.set_index('date', inplace=True)

single_iex = (opeccrude,
aaayieldidx, tenyrtreasbenchmark,tenyrbrkevninf,ethe,gbtc)

for i in single_iex:
    #i = i.reset_index(drop=True) 
    i['date'] = pd.to_datetime(i['date']).dt.strftime('%m-%d-%y')
    i.set_index('date', inplace=True)
    #print(i.index)
    #print(i.columns)
    #var = i[['date']]
    #print(var)
    #print(var.dtypes)
    #print(i)

equity_indices = (us,chn,uk,deu,fr,aus,can,jpn)

for i in equity_indices:
    #i = i.reset_index(drop=True) 
    #print(i)
    #print(i.columns)
    #print(i.index)
    i['date'] = pd.to_datetime(i['date']).dt.strftime('%m-%d-%y')
    i.set_index('date', inplace=True)
    #print(i.index)
    #print(i.columns)
    #var = i[['date']]
    #print(var)
    #print(var.dtypes)  
    #print(i)

#df = pd.concat(equity_indices, axis=1)

#print(df)


custom_indices = fx_list + custom_indices + single_iex + equity_indices

df = pd.concat(custom_indices, axis=1, join = 'inner')

df = df.reset_index() 

df['date'] = pd.to_datetime(df['date'],errors='coerce')

date = df['date'].max() 

df = df.apply(pd.to_numeric)

df = df.set_index('date')

print(date)

#print(df.dtypes)

#df.to_csv('custom_indices.csv')

df = df.corr()

#df.to_csv('intermediate.csv')

df = df.stack().reset_index()

df.columns = ['a','b','c']

df = df[df.c != 1]

df['transpose'] = df['a'] + '/'+ df['b']

df = df.drop(['a','b'], 1)

df = df.drop_duplicates(subset =['c'])

df = df[['transpose','c']]

df['date'] = date

#df = df.set_index('date')

#df.reset_index().T

df = df.pivot(index ='date', columns='transpose',values = 'c')
#print(df.columns)

#df.to_csv('testcorr.csv', index=True)

df.to_sql('correlationall', v2engine, if_exists='append')

