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

query = "SELECT * FROM broadaeroanddefense"
broadaeroanddefense = pd.read_sql(query, con = v2engine)
broadaeroanddefense= broadaeroanddefense[['date','Price']]
broadaeroanddefense.columns= ['date', 'broadaeroanddefense']
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
query = "SELECT * FROM broadoilandgas"
broadoilandgas = pd.read_sql(query, con = v2engine)
broadoilandgas = broadoilandgas[['date','Price']]
broadoilandgas.columns= ['date', 'broadoilandgas']
query = "SELECT * FROM xwinflationsense"
xwinflationsense = pd.read_sql(query, con = v2engine)
xwinflationsense = xwinflationsense[['date','Price']]
xwinflationsense.columns= ['date', 'xwinflationsense']
query = "SELECT * FROM broadfinancials"
broadfinancials = pd.read_sql(query, con = v2engine)
broadfinancials = broadfinancials[['date','Price']]
broadfinancials.columns= ['date', 'broadfinancials']
query = "SELECT * FROM broadutilities"
broadutilities = pd.read_sql(query, con = v2engine)
broadutilities = broadutilities[['date','Price']]
broadutilities.columns= ['date', 'broadutilities']
query = "SELECT * FROM broadconsumercore"
broadconsumercore = pd.read_sql(query, con = v2engine)
broadconsumercore = broadconsumercore[['date','Price']]
broadconsumercore.columns= ['date', 'broadconsumercore']
query = "SELECT * FROM broadconstruction"
broadconstruction = pd.read_sql(query, con = v2engine)
broadconstruction = broadconstruction[['date','Price']]
broadconstruction.columns= ['date', 'broadconstruction']
query = "SELECT * FROM broadmanu"
broadmanu = pd.read_sql(query, con = v2engine)
broadmanu = broadmanu[['date','Price']]
broadmanu.columns= ['date', 'broadmanu']
query = "SELECT * FROM broadtranspologistics"
broadtranspologistics = pd.read_sql(query, con = v2engine)
broadtranspologistics = broadtranspologistics[['date','Price']]
broadtranspologistics.columns= ['date', 'broadtranspologistics']
query = "SELECT * FROM broadsemi"
broadsemi = pd.read_sql(query, con = v2engine)
broadsemi = broadsemi[['date','Price']]
broadsemi.columns= ['date', 'broadsemi']
query = "SELECT * FROM broadcomms"
broadcomms = pd.read_sql(query, con = v2engine)
broadcomms = broadcomms[['date','Price']]
broadcomms.columns= ['date', 'broadcomms']
query = "SELECT * FROM broadhealthbiotech"
broadhealthbiotech = pd.read_sql(query, con = v2engine)
broadhealthbiotech = broadhealthbiotech[['date','Price']]
broadhealthbiotech.columns= ['date', 'broadhealthbiotech']
query = "SELECT * FROM broadentertainment"
broadentertainment = pd.read_sql(query, con = v2engine)
broadentertainment = broadentertainment[['date','Price']]
broadentertainment.columns= ['date', 'broadentertainment']
query = "SELECT * FROM broadconsumeredge"
broadconsumeredge = pd.read_sql(query, con = v2engine)
broadconsumeredge = broadconsumeredge[['date','Price']]
broadconsumeredge.columns= ['date', 'broadconsumeredge']

#print(ethe)


custom_indices = (broadaeroanddefense,broadreits,stapleagri,
broadmetals,broadoilandgas,xwinflationsense,
broadfinancials,broadutilities,broadconsumercore,
broadconstruction,broadmanu,broadtranspologistics,
broadsemi,broadcomms,broadhealthbiotech,
broadentertainment,broadconsumeredge)

for i in custom_indices:
    i['date'] = pd.to_datetime(i['date']).dt.strftime('%m-%d-%y')
    i.set_index('date', inplace=True)


df = pd.concat(custom_indices, axis=1, join = 'inner')

df = df.reset_index() 

df['date'] = pd.to_datetime(df['date'],errors='coerce')

date = df['date'].max() 

df = df.apply(pd.to_numeric)

df = df.set_index('date')

print(date)

#print(df.dtypes)

df.to_csv('custom_indices2.csv')

df = df.corr()

df.to_csv('intermediate2.csv')

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

df.to_sql('correlationcustoms', v2engine, if_exists='append')