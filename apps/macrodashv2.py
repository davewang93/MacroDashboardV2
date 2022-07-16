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
audusd= audusd[['time','mid.c']]
query = "SELECT * FROM eurusd"
eurusd = pd.read_sql(query, con = fxengine)
eurusd= eurusd[['time','mid.c']]
query = "SELECT * FROM gbpusd"
gbpusd = pd.read_sql(query, con = fxengine)
gbpusd= gbpusd[['time','mid.c']]
query = "SELECT * FROM usdchf"
usdchf = pd.read_sql(query, con = fxengine)
usdchf= usdchf[['time','mid.c']]
query = "SELECT * FROM usdcad"
usdcad = pd.read_sql(query, con = fxengine)
usdcad= usdcad[['time','mid.c']]
query = "SELECT * FROM usdjpy"
usdjpy = pd.read_sql(query, con = fxengine)
usdjpy= usdjpy[['time','mid.c']]
#print(usdjpy,gbpusd)

#Date, Value
query = "SELECT * FROM indeedus"
indeedus = pd.read_sql(query, con = v1engine)
query = "SELECT * FROM indeednewus"
indeednewus = pd.read_sql(query, con = v1engine)
query = "SELECT * FROM opeccrude"
opeccrude = pd.read_sql(query, con = v1engine)
query = "SELECT * FROM usfedfundsrate"
usfedfundsrate = pd.read_sql(query, con = v1engine)
query = "SELECT * FROM discountrate"
discountrate = pd.read_sql(query, con = v1engine)
query = "SELECT * FROM usgovtyieldcurve"
usgovtyieldcurve = pd.read_sql(query, con = v1engine)
query = "SELECT * FROM 10yrtreasbenchmark"
tenyrtreasbenchmark = pd.read_sql(query, con = v1engine)
query = "SELECT * FROM ustwoten"
ustwoten = pd.read_sql(query, con = v1engine)
query = "SELECT * FROM aaayieldidx"
aaayieldidx = pd.read_sql(query, con = v1engine)
query = "SELECT * FROM bbbyieldidx"
bbbyieldidx = pd.read_sql(query, con = v1engine)
query = "SELECT * FROM cccyieldidx"
cccyieldidx = pd.read_sql(query, con = v1engine)
query = "SELECT * FROM 30yrmortgage"
thirtyyrmortgage = pd.read_sql(query, con = v1engine)
query = "SELECT * FROM 5yrtips"
fiveyrtips = pd.read_sql(query, con = v1engine)
query = "SELECT * FROM 10yrtips"
tenyrtips = pd.read_sql(query, con = v1engine)
query = "SELECT * FROM 5yrbrkevninf"
fiveyrbrkevninf = pd.read_sql(query, con = v1engine)
query = "SELECT * FROM 10yrbrkevninf"
tenyrbrkevninf = pd.read_sql(query, con = v1engine)
#print(tenyrbrkevninf,usfedfundsrate)

query = "SELECT * FROM broadaeroanddefense"
broadaeroanddefense = pd.read_sql(query, con = v2engine)
broadaeroanddefense= broadaeroanddefense[['date','Price']]
#print(broadaeroanddefense.head())
query = "SELECT * FROM selectedglobaldefense"
selectedglobaldefense = pd.read_sql(query, con = v2engine)
selectedglobaldefense= selectedglobaldefense[['date','Price']]
query = "SELECT * FROM selectedglobalstaffing"
selectedglobalstaffing = pd.read_sql(query, con = v2engine)
selectedglobalstaffing= selectedglobalstaffing[['date','Price']]
query = "SELECT * FROM broadreits"
broadreits = pd.read_sql(query, con = v2engine)
broadreits= broadreits[['date','Price']]
query = "SELECT * FROM selectedglobalrealestate"
selectedglobalrealestate = pd.read_sql(query, con = v2engine)
selectedglobalrealestate= selectedglobalrealestate[['date','Price']]
query = "SELECT * FROM dba"
dba = pd.read_sql(query, con = v2engine)
dba= dba[['date','close']]
query = "SELECT * FROM stapleagri"
stapleagri = pd.read_sql(query, con = v2engine)
stapleagri= stapleagri[['date','Price']]
query = "SELECT * FROM corn"
corn = pd.read_sql(query, con = v2engine)
corn= corn[['date','close']]
query = "SELECT * FROM weat"
weat = pd.read_sql(query, con = v2engine)
weat= weat[['date','close']]
query = "SELECT * FROM broadmetals"
broadmetals = pd.read_sql(query, con = v2engine)
broadmetals= broadmetals[['date','Price']]
query = "SELECT * FROM selectedmetals"
selectedmetals = pd.read_sql(query, con = v2engine)
selectedmetals = selectedmetals[['date','Price']]
query = "SELECT * FROM gld"
gld = pd.read_sql(query, con = v2engine)
gld = gld[['date','close']]
query = "SELECT * FROM dbb"
dbb = pd.read_sql(query, con = v2engine)
dbb = dbb[['date','close']]
query = "SELECT * FROM broadlumber"
broadlumber = pd.read_sql(query, con = v2engine)
broadlumber = broadlumber[['date','Price']]
query = "SELECT * FROM selectedgloballumber"
selectedgloballumber = pd.read_sql(query, con = v2engine)
selectedgloballumber = selectedgloballumber[['date','Price']]
query = "SELECT * FROM broadoilandgas"
broadoilandgas = pd.read_sql(query, con = v2engine)
broadoilandgas = broadoilandgas[['date','Price']]
query = "SELECT * FROM selectedglobaloilandgas"
selectedglobaloilandgas = pd.read_sql(query, con = v2engine)
selectedglobaloilandgas = selectedglobaloilandgas[['date','Price']]
query = "SELECT * FROM bno"
bno = pd.read_sql(query, con = v2engine)
bno = bno[['date','close']]
query = "SELECT * FROM ung"
ung = pd.read_sql(query, con = v2engine)
ung = ung[['date','close']]
query = "SELECT * FROM broadcleanenergy"
broadcleanenergy = pd.read_sql(query, con = v2engine)
broadcleanenergy = broadcleanenergy[['date','Price']]
query = "SELECT * FROM selectedglobalcleanenergy"
selectedglobalcleanenergy = pd.read_sql(query, con = v2engine)
selectedglobalcleanenergy = selectedglobalcleanenergy[['date','Price']]
query = "SELECT * FROM xwinflationsense"
xwinflationsense = pd.read_sql(query, con = v2engine)
xwinflationsense = xwinflationsense[['date','Price']]
query = "SELECT * FROM broadfinancials"
broadfinancials = pd.read_sql(query, con = v2engine)
broadfinancials = broadfinancials[['date','Price']]
query = "SELECT * FROM selectedglobalfinancials"
selectedglobalfinancials = pd.read_sql(query, con = v2engine)
selectedglobalfinancials = selectedglobalfinancials[['date','Price']]
query = "SELECT * FROM broadutilities"
broadutilities = pd.read_sql(query, con = v2engine)
broadutilities = broadutilities[['date','Price']]
query = "SELECT * FROM selectedglobalutilities"
selectedglobalutilities = pd.read_sql(query, con = v2engine)
selectedglobalutilities = selectedglobalutilities[['date','Price']]
query = "SELECT * FROM broadconsumercore"
broadconsumercore = pd.read_sql(query, con = v2engine)
broadconsumercore = broadconsumercore[['date','Price']]
query = "SELECT * FROM selectedglobalconsumercore"
selectedglobalconsumercore = pd.read_sql(query, con = v2engine)
selectedglobalconsumercore = selectedglobalconsumercore[['date','Price']]
query = "SELECT * FROM broadconstruction"
broadconstruction = pd.read_sql(query, con = v2engine)
broadconstruction = broadconstruction[['date','Price']]
query = "SELECT * FROM selectedglobalconstruction"
selectedglobalconstruction = pd.read_sql(query, con = v2engine)
selectedglobalconstruction = selectedglobalconstruction[['date','Price']]
query = "SELECT * FROM broadmanu"
broadmanu = pd.read_sql(query, con = v2engine)
broadmanu = broadmanu[['date','Price']]
query = "SELECT * FROM selectedglobalmanu"
selectedglobalmanu = pd.read_sql(query, con = v2engine)
selectedglobalmanu = selectedglobalmanu[['date','Price']]
query = "SELECT * FROM broadtranspologistics"
broadtranspologistics = pd.read_sql(query, con = v2engine)
broadtranspologistics = broadtranspologistics[['date','Price']]
query = "SELECT * FROM selectedglobaltranslogi"
selectedglobaltranslogi = pd.read_sql(query, con = v2engine)
selectedglobaltranslogi = selectedglobaltranslogi[['date','Price']]
query = "SELECT * FROM broadsemi"
broadsemi = pd.read_sql(query, con = v2engine)
broadsemi = broadsemi[['date','Price']]
query = "SELECT * FROM selectedglobalsemi"
selectedglobalsemi = pd.read_sql(query, con = v2engine)
selectedglobalsemi = selectedglobalsemi[['date','Price']]
query = "SELECT * FROM broadcomms"
broadcomms = pd.read_sql(query, con = v2engine)
broadcomms = broadcomms[['date','Price']]
query = "SELECT * FROM selectedglobalcomms"
selectedglobalcomms = pd.read_sql(query, con = v2engine)
selectedglobalcomms = selectedglobalcomms[['date','Price']]
query = "SELECT * FROM broadhealthbiotech"
broadhealthbiotech = pd.read_sql(query, con = v2engine)
broadhealthbiotech = broadhealthbiotech[['date','Price']]
query = "SELECT * FROM selectedglobalbiohealth"
selectedglobalbiohealth = pd.read_sql(query, con = v2engine)
selectedglobalbiohealth = selectedglobalbiohealth[['date','Price']]
query = "SELECT * FROM broadentertainment"
broadentertainment = pd.read_sql(query, con = v2engine)
broadentertainment = broadentertainment[['date','Price']]
query = "SELECT * FROM selectedglobalentertainment"
selectedglobalentertainment = pd.read_sql(query, con = v2engine)
selectedglobalentertainment = selectedglobalentertainment[['date','Price']]
query = "SELECT * FROM broadconsumeredge"
broadconsumeredge = pd.read_sql(query, con = v2engine)
broadconsumeredge = broadconsumeredge[['date','Price']]
query = "SELECT * FROM selectedglobalconsumeredge"
selectedglobalconsumeredge = pd.read_sql(query, con = v2engine)
selectedglobalconsumeredge = selectedglobalconsumeredge[['date','Price']]
query = "SELECT * FROM voo"
voo = pd.read_sql(query, con = v2engine)
voo = voo[['date','close']]
query = "SELECT * FROM mchi"
mchi = pd.read_sql(query, con = v2engine)
mchi = mchi[['date','close']]
query = "SELECT * FROM ewj"
ewj = pd.read_sql(query, con = v2engine)
ewj = ewj[['date','close']]
query = "SELECT * FROM ewc"
ewc = pd.read_sql(query, con = v2engine)
ewc = ewc[['date','close']]
query = "SELECT * FROM ewu"
ewu = pd.read_sql(query, con = v2engine)
ewu = ewu[['date','close']]
query = "SELECT * FROM ewg"
ewg = pd.read_sql(query, con = v2engine)
ewg = ewg[['date','close']]
query = "SELECT * FROM ewa"
ewa = pd.read_sql(query, con = v2engine)
ewa = ewa[['date','close']]
query = "SELECT * FROM ewq"
ewq = pd.read_sql(query, con = v2engine)
ewq = ewq[['date','close']]
query = "SELECT * FROM xwglobalequitysense"
xwglobalequitysense = pd.read_sql(query, con = v2engine)
xwglobalequitysense = xwglobalequitysense[['date','Price']]
query = "SELECT * FROM gbtc"
gbtc = pd.read_sql(query, con = v2engine)
gbtc = gbtc[['date','close']]
query = "SELECT * FROM ethe"
ethe = pd.read_sql(query, con = v2engine)
ethe = ethe[['date','close']]

#print(selectedglobalconsumeredge,broadhealthbiotech)

voo = px.line(voo, x='date', y='close', title='VG S&P 500')
voo.update_xaxes(
    title = 'Date Range',
    rangeslider_visible=True,
    rangeselector=dict(
        bgcolor = '#F89880',
        activecolor = '#FF4433',
        buttons=list([
            dict(count=1, label="1m", step="month", stepmode="backward"),
            dict(count=6, label="6m", step="month", stepmode="backward"),
            dict(count=1, label="YTD", step="year", stepmode="todate"),
            dict(count=1, label="1y", step="year", stepmode="backward"),
            dict(step="all")      
            ])
    )
)
voo.update_yaxes(title = '')
voo.update_traces(line_color='#FF4500')
voo.update_layout(
    plot_bgcolor='#1f2833',
    paper_bgcolor='#1f2833',
    font_color = 'white')

mchi = px.line(mchi, x='date', y='close', title='iShares China')
mchi.update_xaxes(
    title = 'Date Range',
    rangeslider_visible=True,
    rangeselector=dict(
        bgcolor = '#F89880',
        activecolor = '#FF4433',
        buttons=list([
            dict(count=1, label="1m", step="month", stepmode="backward"),
            dict(count=6, label="6m", step="month", stepmode="backward"),
            dict(count=1, label="YTD", step="year", stepmode="todate"),
            dict(count=1, label="1y", step="year", stepmode="backward"),
            dict(step="all")      
            ])
    )
)
mchi.update_yaxes(title = '')
mchi.update_traces(line_color='#FF4500')
mchi.update_layout(
    plot_bgcolor='#1f2833',
    paper_bgcolor='#1f2833',
    font_color = 'white')

ewj = px.line(ewj, x='date', y='close', title='iShares Japan')
ewj.update_xaxes(
    title = 'Date Range',
    rangeslider_visible=True,
    rangeselector=dict(
        bgcolor = '#F89880',
        activecolor = '#FF4433',
        buttons=list([
            dict(count=1, label="1m", step="month", stepmode="backward"),
            dict(count=6, label="6m", step="month", stepmode="backward"),
            dict(count=1, label="YTD", step="year", stepmode="todate"),
            dict(count=1, label="1y", step="year", stepmode="backward"),
            dict(step="all")      
            ])
    )
)
ewj.update_yaxes(title = '')
ewj.update_traces(line_color='#FF4500')
ewj.update_layout(
    plot_bgcolor='#1f2833',
    paper_bgcolor='#1f2833',
    font_color = 'white')

ewg = px.line(ewg, x='date', y='close', title='iShares Germany')
ewg.update_xaxes(
    title = 'Date Range',
    rangeslider_visible=True,
    rangeselector=dict(
        bgcolor = '#F89880',
        activecolor = '#FF4433',
        buttons=list([
            dict(count=1, label="1m", step="month", stepmode="backward"),
            dict(count=6, label="6m", step="month", stepmode="backward"),
            dict(count=1, label="YTD", step="year", stepmode="todate"),
            dict(count=1, label="1y", step="year", stepmode="backward"),
            dict(step="all")      
            ])
    )
)
ewg.update_yaxes(title = '')
ewg.update_traces(line_color='#FF4500')
ewg.update_layout(
    plot_bgcolor='#1f2833',
    paper_bgcolor='#1f2833',
    font_color = 'white')

ewu = px.line(ewu, x='date', y='close', title='iShares United Kingdom')
ewu.update_xaxes(
    title = 'Date Range',
    rangeslider_visible=True,
    rangeselector=dict(
        bgcolor = '#F89880',
        activecolor = '#FF4433',
        buttons=list([
            dict(count=1, label="1m", step="month", stepmode="backward"),
            dict(count=6, label="6m", step="month", stepmode="backward"),
            dict(count=1, label="YTD", step="year", stepmode="todate"),
            dict(count=1, label="1y", step="year", stepmode="backward"),
            dict(step="all")      
            ])
    )
)
ewu.update_yaxes(title = '')
ewu.update_traces(line_color='#FF4500')
ewu.update_layout(
    plot_bgcolor='#1f2833',
    paper_bgcolor='#1f2833',
    font_color = 'white')

ewq = px.line(ewq, x='date', y='close', title='iShares France')
ewq.update_xaxes(
    title = 'Date Range',
    rangeslider_visible=True,
    rangeselector=dict(
        bgcolor = '#F89880',
        activecolor = '#FF4433',
        buttons=list([
            dict(count=1, label="1m", step="month", stepmode="backward"),
            dict(count=6, label="6m", step="month", stepmode="backward"),
            dict(count=1, label="YTD", step="year", stepmode="todate"),
            dict(count=1, label="1y", step="year", stepmode="backward"),
            dict(step="all")      
            ])
    )
)
ewq.update_yaxes(title = '')
ewq.update_traces(line_color='#FF4500')
ewq.update_layout(
    plot_bgcolor='#1f2833',
    paper_bgcolor='#1f2833',
    font_color = 'white')

ewc = px.line(ewc, x='date', y='close', title='iShares Canada')
ewc.update_xaxes(
    title = 'Date Range',
    rangeslider_visible=True,
    rangeselector=dict(
        bgcolor = '#F89880',
        activecolor = '#FF4433',
        buttons=list([
            dict(count=1, label="1m", step="month", stepmode="backward"),
            dict(count=6, label="6m", step="month", stepmode="backward"),
            dict(count=1, label="YTD", step="year", stepmode="todate"),
            dict(count=1, label="1y", step="year", stepmode="backward"),
            dict(step="all")      
            ])
    )
)
ewc.update_yaxes(title = '')
ewc.update_traces(line_color='#FF4500')
ewc.update_layout(
    plot_bgcolor='#1f2833',
    paper_bgcolor='#1f2833',
    font_color = 'white')

ewa = px.line(ewa, x='date', y='close', title='iShares Australia')
ewa.update_xaxes(
    title = 'Date Range',
    rangeslider_visible=True,
    rangeselector=dict(
        bgcolor = '#F89880',
        activecolor = '#FF4433',
        buttons=list([
            dict(count=1, label="1m", step="month", stepmode="backward"),
            dict(count=6, label="6m", step="month", stepmode="backward"),
            dict(count=1, label="YTD", step="year", stepmode="todate"),
            dict(count=1, label="1y", step="year", stepmode="backward"),
            dict(step="all")      
            ])
    )
)
ewa.update_yaxes(title = '')
ewa.update_traces(line_color='#FF4500')
ewa.update_layout(
    plot_bgcolor='#1f2833',
    paper_bgcolor='#1f2833',
    font_color = 'white')

xwglobalequitysense = px.line(xwglobalequitysense, x='date', y='Price', title='XW Global Equity Sense')
xwglobalequitysense.update_xaxes(
    title = 'Date Range',
    rangeslider_visible=True,
    rangeselector=dict(
        bgcolor = '#F89880',
        activecolor = '#FF4433',
        buttons=list([
            dict(count=1, label="1m", step="month", stepmode="backward"),
            dict(count=6, label="6m", step="month", stepmode="backward"),
            dict(count=1, label="YTD", step="year", stepmode="todate"),
            dict(count=1, label="1y", step="year", stepmode="backward"),
            dict(step="all")      
            ])
    )
)
xwglobalequitysense.update_yaxes(title = '')
xwglobalequitysense.update_traces(line_color='#FF4500')
xwglobalequitysense.update_layout(
    plot_bgcolor='#1f2833',
    paper_bgcolor='#1f2833',
    font_color = 'white')

indeedus = px.line(indeedus, x='Date', y='Value', title='Job Postings on Indeed - US')
indeedus.update_xaxes(
    title = 'Date Range',
    rangeslider_visible=True,
    rangeselector=dict(
        bgcolor = '#F89880',
        activecolor = '#FF4433',
        buttons=list([
            dict(count=1, label="1m", step="month", stepmode="backward"),
            dict(count=6, label="6m", step="month", stepmode="backward"),
            dict(count=1, label="YTD", step="year", stepmode="todate"),
            dict(count=1, label="1y", step="year", stepmode="backward"),
            dict(step="all")      
            ])
    )
)
indeedus.update_yaxes(title = '')
indeedus.update_traces(line_color='#FF4500')
indeedus.update_layout(
    plot_bgcolor='#1f2833',
    paper_bgcolor='#1f2833',
    font_color = 'white')

indeednewus = px.line(indeednewus, x='Date', y='Value', title='New Job Postings on Indeed - US')
indeednewus.update_xaxes(
    title = 'Date Range',
    rangeslider_visible=True,
    rangeselector=dict(
        bgcolor = '#F89880',
        activecolor = '#FF4433',
        buttons=list([
            dict(count=1, label="1m", step="month", stepmode="backward"),
            dict(count=6, label="6m", step="month", stepmode="backward"),
            dict(count=1, label="YTD", step="year", stepmode="todate"),
            dict(count=1, label="1y", step="year", stepmode="backward"),
            dict(step="all")      
            ])
    )
)
indeednewus.update_yaxes(title = '')
indeednewus.update_traces(line_color='#FF4500')
indeednewus.update_layout(
    plot_bgcolor='#1f2833',
    paper_bgcolor='#1f2833',
    font_color = 'white')

selectedglobalstaffing = px.line(selectedglobalstaffing, x='date', y='Price', title='Selected Global Staffing')
selectedglobalstaffing.update_xaxes(
    title = 'Date Range',
    rangeslider_visible=True,
    rangeselector=dict(
        bgcolor = '#F89880',
        activecolor = '#FF4433',
        buttons=list([
            dict(count=1, label="1m", step="month", stepmode="backward"),
            dict(count=6, label="6m", step="month", stepmode="backward"),
            dict(count=1, label="YTD", step="year", stepmode="todate"),
            dict(count=1, label="1y", step="year", stepmode="backward"),
            dict(step="all")      
            ])
    )
)
selectedglobalstaffing.update_yaxes(title = '')
selectedglobalstaffing.update_traces(line_color='#FF4500')
selectedglobalstaffing.update_layout(
    plot_bgcolor='#1f2833',
    paper_bgcolor='#1f2833',
    font_color = 'white')

broadreits = px.line(broadreits, x='date', y='Price', title='Broad REITs')
broadreits.update_xaxes(
    title = 'Date Range',
    rangeslider_visible=True,
    rangeselector=dict(
        bgcolor = '#F89880',
        activecolor = '#FF4433',
        buttons=list([
            dict(count=1, label="1m", step="month", stepmode="backward"),
            dict(count=6, label="6m", step="month", stepmode="backward"),
            dict(count=1, label="YTD", step="year", stepmode="todate"),
            dict(count=1, label="1y", step="year", stepmode="backward"),
            dict(step="all")      
            ])
    )
)
broadreits.update_yaxes(title = '')
broadreits.update_traces(line_color='#FF4500')
broadreits.update_layout(
    plot_bgcolor='#1f2833',
    paper_bgcolor='#1f2833',
    font_color = 'white')

selectedglobalrealestate = px.line(selectedglobalrealestate, x='date', y='Price', title='Selected Global Real Estate')
selectedglobalrealestate.update_xaxes(
    title = 'Date Range',
    rangeslider_visible=True,
    rangeselector=dict(
        bgcolor = '#F89880',
        activecolor = '#FF4433',
        buttons=list([
            dict(count=1, label="1m", step="month", stepmode="backward"),
            dict(count=6, label="6m", step="month", stepmode="backward"),
            dict(count=1, label="YTD", step="year", stepmode="todate"),
            dict(count=1, label="1y", step="year", stepmode="backward"),
            dict(step="all")      
            ])
    )
)
selectedglobalrealestate.update_yaxes(title = '')
selectedglobalrealestate.update_traces(line_color='#FF4500')
selectedglobalrealestate.update_layout(
    plot_bgcolor='#1f2833',
    paper_bgcolor='#1f2833',
    font_color = 'white')

broadaeroanddefenseplot = px.line(broadaeroanddefense, x='date', y='Price', title='Broad Aerospace and Defense')
broadaeroanddefenseplot.update_xaxes(
    title = 'Date Range',
    rangeslider_visible=True,
    rangeselector=dict(
        bgcolor = '#F89880',
        activecolor = '#FF4433',
        buttons=list([
            dict(count=1, label="1m", step="month", stepmode="backward"),
            dict(count=6, label="6m", step="month", stepmode="backward"),
            dict(count=1, label="YTD", step="year", stepmode="todate"),
            dict(count=1, label="1y", step="year", stepmode="backward"),
            dict(step="all")      
            ])
    )
)
broadaeroanddefenseplot.update_yaxes(title = '')
broadaeroanddefenseplot.update_traces(line_color='#FF4500')
broadaeroanddefenseplot.update_layout(
    plot_bgcolor='#1f2833',
    paper_bgcolor='#1f2833',
    font_color = 'white')

selectedglobaldefense = px.line(selectedglobaldefense, x='date', y='Price', title='Selected Global Defense')
selectedglobaldefense.update_xaxes(
    title = 'Date Range',
    rangeslider_visible=True,
    rangeselector=dict(
        bgcolor = '#F89880',
        activecolor = '#FF4433',
        buttons=list([
            dict(count=1, label="1m", step="month", stepmode="backward"),
            dict(count=6, label="6m", step="month", stepmode="backward"),
            dict(count=1, label="YTD", step="year", stepmode="todate"),
            dict(count=1, label="1y", step="year", stepmode="backward"),
            dict(step="all")      
            ])
    )
)
selectedglobaldefense.update_yaxes(title = '')
selectedglobaldefense.update_traces(line_color='#FF4500')
selectedglobaldefense.update_layout(
    plot_bgcolor='#1f2833',
    paper_bgcolor='#1f2833',
    font_color = 'white')

stapleagri = px.line(stapleagri, x='date', y='Price', title='Staple Agriculture')
stapleagri.update_xaxes(
    title = 'Date Range',
    rangeslider_visible=True,
    rangeselector=dict(
        bgcolor = '#F89880',
        activecolor = '#FF4433',
        buttons=list([
            dict(count=1, label="1m", step="month", stepmode="backward"),
            dict(count=6, label="6m", step="month", stepmode="backward"),
            dict(count=1, label="YTD", step="year", stepmode="todate"),
            dict(count=1, label="1y", step="year", stepmode="backward"),
            dict(step="all")      
            ])
    )
)
stapleagri.update_yaxes(title = '')
stapleagri.update_traces(line_color='#FF4500')
stapleagri.update_layout(
    plot_bgcolor='#1f2833',
    paper_bgcolor='#1f2833',
    font_color = 'white')

corn = px.line(corn, x='date', y='close', title='Teucrium Corn Fund')
corn.update_xaxes(
    title = 'Date Range',
    rangeslider_visible=True,
    rangeselector=dict(
        bgcolor = '#F89880',
        activecolor = '#FF4433',
        buttons=list([
            dict(count=1, label="1m", step="month", stepmode="backward"),
            dict(count=6, label="6m", step="month", stepmode="backward"),
            dict(count=1, label="YTD", step="year", stepmode="todate"),
            dict(count=1, label="1y", step="year", stepmode="backward"),
            dict(step="all")      
            ])
    )
)
corn.update_yaxes(title = '')
corn.update_traces(line_color='#FF4500')
corn.update_layout(
    plot_bgcolor='#1f2833',
    paper_bgcolor='#1f2833',
    font_color = 'white')

weat = px.line(weat, x='date', y='close', title='Teucrium Wheat Fund')
weat.update_xaxes(
    title = 'Date Range',
    rangeslider_visible=True,
    rangeselector=dict(
        bgcolor = '#F89880',
        activecolor = '#FF4433',
        buttons=list([
            dict(count=1, label="1m", step="month", stepmode="backward"),
            dict(count=6, label="6m", step="month", stepmode="backward"),
            dict(count=1, label="YTD", step="year", stepmode="todate"),
            dict(count=1, label="1y", step="year", stepmode="backward"),
            dict(step="all")      
            ])
    )
)
weat.update_yaxes(title = '')
weat.update_traces(line_color='#FF4500')
weat.update_layout(
    plot_bgcolor='#1f2833',
    paper_bgcolor='#1f2833',
    font_color = 'white')

broadmetals = px.line(broadmetals, x='date', y='Price', title='Broad Metals')
broadmetals.update_xaxes(
    title = 'Date Range',
    rangeslider_visible=True,
    rangeselector=dict(
        bgcolor = '#F89880',
        activecolor = '#FF4433',
        buttons=list([
            dict(count=1, label="1m", step="month", stepmode="backward"),
            dict(count=6, label="6m", step="month", stepmode="backward"),
            dict(count=1, label="YTD", step="year", stepmode="todate"),
            dict(count=1, label="1y", step="year", stepmode="backward"),
            dict(step="all")      
            ])
    )
)
broadmetals.update_yaxes(title = '')
broadmetals.update_traces(line_color='#FF4500')
broadmetals.update_layout(
    plot_bgcolor='#1f2833',
    paper_bgcolor='#1f2833',
    font_color = 'white')

selectedmetals = px.line(selectedmetals, x='date', y='Price', title='Selected Global Metals')
selectedmetals.update_xaxes(
    title = 'Date Range',
    rangeslider_visible=True,
    rangeselector=dict(
        bgcolor = '#F89880',
        activecolor = '#FF4433',
        buttons=list([
            dict(count=1, label="1m", step="month", stepmode="backward"),
            dict(count=6, label="6m", step="month", stepmode="backward"),
            dict(count=1, label="YTD", step="year", stepmode="todate"),
            dict(count=1, label="1y", step="year", stepmode="backward"),
            dict(step="all")      
            ])
    )
)
selectedmetals.update_yaxes(title = '')
selectedmetals.update_traces(line_color='#FF4500')
selectedmetals.update_layout(
    plot_bgcolor='#1f2833',
    paper_bgcolor='#1f2833',
    font_color = 'white')

broadlumber = px.line(broadlumber, x='date', y='Price', title='Broad Lumber')
broadlumber.update_xaxes(
    title = 'Date Range',
    rangeslider_visible=True,
    rangeselector=dict(
        bgcolor = '#F89880',
        activecolor = '#FF4433',
        buttons=list([
            dict(count=1, label="1m", step="month", stepmode="backward"),
            dict(count=6, label="6m", step="month", stepmode="backward"),
            dict(count=1, label="YTD", step="year", stepmode="todate"),
            dict(count=1, label="1y", step="year", stepmode="backward"),
            dict(step="all")      
            ])
    )
)
broadlumber.update_yaxes(title = '')
broadlumber.update_traces(line_color='#FF4500')
broadlumber.update_layout(
    plot_bgcolor='#1f2833',
    paper_bgcolor='#1f2833',
    font_color = 'white')

selectedgloballumber = px.line(selectedgloballumber, x='date', y='Price', title='Selected Global Lumber')
selectedgloballumber.update_xaxes(
    title = 'Date Range',
    rangeslider_visible=True,
    rangeselector=dict(
        bgcolor = '#F89880',
        activecolor = '#FF4433',
        buttons=list([
            dict(count=1, label="1m", step="month", stepmode="backward"),
            dict(count=6, label="6m", step="month", stepmode="backward"),
            dict(count=1, label="YTD", step="year", stepmode="todate"),
            dict(count=1, label="1y", step="year", stepmode="backward"),
            dict(step="all")      
            ])
    )
)
selectedgloballumber.update_yaxes(title = '')
selectedgloballumber.update_traces(line_color='#FF4500')
selectedgloballumber.update_layout(
    plot_bgcolor='#1f2833',
    paper_bgcolor='#1f2833',
    font_color = 'white')

broadoilandgas = px.line(broadoilandgas, x='date', y='Price', title='Broad Oil & Gas')
broadoilandgas.update_xaxes(
    title = 'Date Range',
    rangeslider_visible=True,
    rangeselector=dict(
        bgcolor = '#F89880',
        activecolor = '#FF4433',
        buttons=list([
            dict(count=1, label="1m", step="month", stepmode="backward"),
            dict(count=6, label="6m", step="month", stepmode="backward"),
            dict(count=1, label="YTD", step="year", stepmode="todate"),
            dict(count=1, label="1y", step="year", stepmode="backward"),
            dict(step="all")      
            ])
    )
)
broadoilandgas.update_yaxes(title = '')
broadoilandgas.update_traces(line_color='#FF4500')
broadoilandgas.update_layout(
    plot_bgcolor='#1f2833',
    paper_bgcolor='#1f2833',
    font_color = 'white')

selectedglobaloilandgas = px.line(selectedglobaloilandgas, x='date', y='Price', title='Selected Global Oil & Gas')
selectedglobaloilandgas.update_xaxes(
    title = 'Date Range',
    rangeslider_visible=True,
    rangeselector=dict(
        bgcolor = '#F89880',
        activecolor = '#FF4433',
        buttons=list([
            dict(count=1, label="1m", step="month", stepmode="backward"),
            dict(count=6, label="6m", step="month", stepmode="backward"),
            dict(count=1, label="YTD", step="year", stepmode="todate"),
            dict(count=1, label="1y", step="year", stepmode="backward"),
            dict(step="all")      
            ])
    )
)
selectedglobaloilandgas.update_yaxes(title = '')
selectedglobaloilandgas.update_traces(line_color='#FF4500')
selectedglobaloilandgas.update_layout(
    plot_bgcolor='#1f2833',
    paper_bgcolor='#1f2833',
    font_color = 'white')

opeccrude = px.line(opeccrude, x='Date', y='Value', title='Opec Crude')
opeccrude.update_xaxes(
    title = 'Date Range',
    rangeslider_visible=True,
    rangeselector=dict(
        bgcolor = '#F89880',
        activecolor = '#FF4433',
        buttons=list([
            dict(count=1, label="1m", step="month", stepmode="backward"),
            dict(count=6, label="6m", step="month", stepmode="backward"),
            dict(count=1, label="YTD", step="year", stepmode="todate"),
            dict(count=1, label="1y", step="year", stepmode="backward"),
            dict(step="all")      
            ])
    )
)
opeccrude.update_yaxes(title = '')
opeccrude.update_traces(line_color='#FF4500')
opeccrude.update_layout(
    plot_bgcolor='#1f2833',
    paper_bgcolor='#1f2833',
    font_color = 'white')

bno = px.line(bno, x='date', y='close', title='United States Brent Oil Fund')
bno.update_xaxes(
    title = 'Date Range',
    rangeslider_visible=True,
    rangeselector=dict(
        bgcolor = '#F89880',
        activecolor = '#FF4433',
        buttons=list([
            dict(count=1, label="1m", step="month", stepmode="backward"),
            dict(count=6, label="6m", step="month", stepmode="backward"),
            dict(count=1, label="YTD", step="year", stepmode="todate"),
            dict(count=1, label="1y", step="year", stepmode="backward"),
            dict(step="all")      
            ])
    )
)
bno.update_yaxes(title = '')
bno.update_traces(line_color='#FF4500')
bno.update_layout(
    plot_bgcolor='#1f2833',
    paper_bgcolor='#1f2833',
    font_color = 'white')

ung = px.line(ung, x='date', y='close', title='United States Natural Gas Fund')
ung.update_xaxes(
    title = 'Date Range',
    rangeslider_visible=True,
    rangeselector=dict(
        bgcolor = '#F89880',
        activecolor = '#FF4433',
        buttons=list([
            dict(count=1, label="1m", step="month", stepmode="backward"),
            dict(count=6, label="6m", step="month", stepmode="backward"),
            dict(count=1, label="YTD", step="year", stepmode="todate"),
            dict(count=1, label="1y", step="year", stepmode="backward"),
            dict(step="all")      
            ])
    )
)
ung.update_yaxes(title = '')
ung.update_traces(line_color='#FF4500')
ung.update_layout(
    plot_bgcolor='#1f2833',
    paper_bgcolor='#1f2833',
    font_color = 'white')

broadcleanenergy = px.line(broadcleanenergy, x='date', y='Price', title='Broad Clean Energy')
broadcleanenergy.update_xaxes(
    title = 'Date Range',
    rangeslider_visible=True,
    rangeselector=dict(
        bgcolor = '#F89880',
        activecolor = '#FF4433',
        buttons=list([
            dict(count=1, label="1m", step="month", stepmode="backward"),
            dict(count=6, label="6m", step="month", stepmode="backward"),
            dict(count=1, label="YTD", step="year", stepmode="todate"),
            dict(count=1, label="1y", step="year", stepmode="backward"),
            dict(step="all")      
            ])
    )
)
broadcleanenergy.update_yaxes(title = '')
broadcleanenergy.update_traces(line_color='#FF4500')
broadcleanenergy.update_layout(
    plot_bgcolor='#1f2833',
    paper_bgcolor='#1f2833',
    font_color = 'white')

selectedglobalcleanenergy = px.line(selectedglobalcleanenergy, x='date', y='Price', title='Selected Global Clean Energy')
selectedglobalcleanenergy.update_xaxes(
    title = 'Date Range',
    rangeslider_visible=True,
    rangeselector=dict(
        bgcolor = '#F89880',
        activecolor = '#FF4433',
        buttons=list([
            dict(count=1, label="1m", step="month", stepmode="backward"),
            dict(count=6, label="6m", step="month", stepmode="backward"),
            dict(count=1, label="YTD", step="year", stepmode="todate"),
            dict(count=1, label="1y", step="year", stepmode="backward"),
            dict(step="all")      
            ])
    )
)
selectedglobalcleanenergy.update_yaxes(title = '')
selectedglobalcleanenergy.update_traces(line_color='#FF4500')
selectedglobalcleanenergy.update_layout(
    plot_bgcolor='#1f2833',
    paper_bgcolor='#1f2833',
    font_color = 'white')

audusd = px.line(audusd, x='time', y='mid.c', title='AUDUSD')
audusd.update_xaxes(
    title = 'Date Range',
    rangeslider_visible=True,
    rangeselector=dict(
        bgcolor = '#F89880',
        activecolor = '#FF4433',
        buttons=list([
            dict(count=1, label="1m", step="month", stepmode="backward"),
            dict(count=6, label="6m", step="month", stepmode="backward"),
            dict(count=1, label="YTD", step="year", stepmode="todate"),
            dict(count=1, label="1y", step="year", stepmode="backward"),
            dict(step="all")      
            ])
    )
)
audusd.update_yaxes(title = '')
audusd.update_traces(line_color='#FF4500')
audusd.update_layout(
    plot_bgcolor='#1f2833',
    paper_bgcolor='#1f2833',
    font_color = 'white')

eurusd = px.line(eurusd, x='time', y='mid.c', title='EURUSD')
eurusd.update_xaxes(
    title = 'Date Range',
    rangeslider_visible=True,
    rangeselector=dict(
        bgcolor = '#F89880',
        activecolor = '#FF4433',
        buttons=list([
            dict(count=1, label="1m", step="month", stepmode="backward"),
            dict(count=6, label="6m", step="month", stepmode="backward"),
            dict(count=1, label="YTD", step="year", stepmode="todate"),
            dict(count=1, label="1y", step="year", stepmode="backward"),
            dict(step="all")      
            ])
    )
)
eurusd.update_yaxes(title = '')
eurusd.update_traces(line_color='#FF4500')
eurusd.update_layout(
    plot_bgcolor='#1f2833',
    paper_bgcolor='#1f2833',
    font_color = 'white')

gbpusd = px.line(gbpusd, x='time', y='mid.c', title='GBPUSD')
gbpusd.update_xaxes(
    title = 'Date Range',
    rangeslider_visible=True,
    rangeselector=dict(
        bgcolor = '#F89880',
        activecolor = '#FF4433',
        buttons=list([
            dict(count=1, label="1m", step="month", stepmode="backward"),
            dict(count=6, label="6m", step="month", stepmode="backward"),
            dict(count=1, label="YTD", step="year", stepmode="todate"),
            dict(count=1, label="1y", step="year", stepmode="backward"),
            dict(step="all")      
            ])
    )
)
gbpusd.update_yaxes(title = '')
gbpusd.update_traces(line_color='#FF4500')
gbpusd.update_layout(
    plot_bgcolor='#1f2833',
    paper_bgcolor='#1f2833',
    font_color = 'white')

usdchf = px.line(usdchf, x='time', y='mid.c', title='USDCHF')
usdchf.update_xaxes(
    title = 'Date Range',
    rangeslider_visible=True,
    rangeselector=dict(
        bgcolor = '#F89880',
        activecolor = '#FF4433',
        buttons=list([
            dict(count=1, label="1m", step="month", stepmode="backward"),
            dict(count=6, label="6m", step="month", stepmode="backward"),
            dict(count=1, label="YTD", step="year", stepmode="todate"),
            dict(count=1, label="1y", step="year", stepmode="backward"),
            dict(step="all")      
            ])
    )
)
usdchf.update_yaxes(title = '')
usdchf.update_traces(line_color='#FF4500')
usdchf.update_layout(
    plot_bgcolor='#1f2833',
    paper_bgcolor='#1f2833',
    font_color = 'white')

usdcad = px.line(usdcad, x='time', y='mid.c', title='USDCAD')
usdcad.update_xaxes(
    title = 'Date Range',
    rangeslider_visible=True,
    rangeselector=dict(
        bgcolor = '#F89880',
        activecolor = '#FF4433',
        buttons=list([
            dict(count=1, label="1m", step="month", stepmode="backward"),
            dict(count=6, label="6m", step="month", stepmode="backward"),
            dict(count=1, label="YTD", step="year", stepmode="todate"),
            dict(count=1, label="1y", step="year", stepmode="backward"),
            dict(step="all")      
            ])
    )
)
usdcad.update_yaxes(title = '')
usdcad.update_traces(line_color='#FF4500')
usdcad.update_layout(
    plot_bgcolor='#1f2833',
    paper_bgcolor='#1f2833',
    font_color = 'white')

usdjpy = px.line(usdjpy, x='time', y='mid.c', title='USDJPY')
usdjpy.update_xaxes(
    title = 'Date Range',
    rangeslider_visible=True,
    rangeselector=dict(
        bgcolor = '#F89880',
        activecolor = '#FF4433',
        buttons=list([
            dict(count=1, label="1m", step="month", stepmode="backward"),
            dict(count=6, label="6m", step="month", stepmode="backward"),
            dict(count=1, label="YTD", step="year", stepmode="todate"),
            dict(count=1, label="1y", step="year", stepmode="backward"),
            dict(step="all")      
            ])
    )
)
usdjpy.update_yaxes(title = '')
usdjpy.update_traces(line_color='#FF4500')
usdjpy.update_layout(
    plot_bgcolor='#1f2833',
    paper_bgcolor='#1f2833',
    font_color = 'white')

usfedfundsrate = px.line(usfedfundsrate, x='Date', y='Value', title='US Fed Funds Rate')
usfedfundsrate.update_xaxes(
    title = 'Date Range',
    rangeslider_visible=True,
    rangeselector=dict(
        bgcolor = '#F89880',
        activecolor = '#FF4433',
        buttons=list([
            dict(count=1, label="1m", step="month", stepmode="backward"),
            dict(count=6, label="6m", step="month", stepmode="backward"),
            dict(count=1, label="YTD", step="year", stepmode="todate"),
            dict(count=1, label="1y", step="year", stepmode="backward"),
            dict(step="all")      
            ])
    )
)
usfedfundsrate.update_yaxes(title = '')
usfedfundsrate.update_traces(line_color='#FF4500')
usfedfundsrate.update_layout(
    plot_bgcolor='#1f2833',
    paper_bgcolor='#1f2833',
    font_color = 'white')

discountrate = px.line(discountrate, x='Date', y='Value', title='US Discount Rate')
discountrate.update_xaxes(
    title = 'Date Range',
    rangeslider_visible=True,
    rangeselector=dict(
        bgcolor = '#F89880',
        activecolor = '#FF4433',
        buttons=list([
            dict(count=1, label="1m", step="month", stepmode="backward"),
            dict(count=6, label="6m", step="month", stepmode="backward"),
            dict(count=1, label="YTD", step="year", stepmode="todate"),
            dict(count=1, label="1y", step="year", stepmode="backward"),
            dict(step="all")      
            ])
    )
)
discountrate.update_yaxes(title = '')
discountrate.update_traces(line_color='#FF4500')
discountrate.update_layout(
    plot_bgcolor='#1f2833',
    paper_bgcolor='#1f2833',
    font_color = 'white')

tenyrtreasbenchmark = px.line(tenyrtreasbenchmark, x='Date', y='Value', title='10 Yr US Treasury')
tenyrtreasbenchmark.update_xaxes(
    title = 'Date Range',
    rangeslider_visible=True,
    rangeselector=dict(
        bgcolor = '#F89880',
        activecolor = '#FF4433',
        buttons=list([
            dict(count=1, label="1m", step="month", stepmode="backward"),
            dict(count=6, label="6m", step="month", stepmode="backward"),
            dict(count=1, label="YTD", step="year", stepmode="todate"),
            dict(count=1, label="1y", step="year", stepmode="backward"),
            dict(step="all")      
            ])
    )
)
tenyrtreasbenchmark.update_yaxes(title = '')
tenyrtreasbenchmark.update_traces(line_color='#FF4500')
tenyrtreasbenchmark.update_layout(
    plot_bgcolor='#1f2833',
    paper_bgcolor='#1f2833',
    font_color = 'white')

ustwoten = px.line(ustwoten, x='Date', y='Value', title='US 2-10 Treasury Spread')
ustwoten.update_xaxes(
    title = 'Date Range',
    rangeslider_visible=True,
    rangeselector=dict(
        bgcolor = '#F89880',
        activecolor = '#FF4433',
        buttons=list([
            dict(count=1, label="1m", step="month", stepmode="backward"),
            dict(count=6, label="6m", step="month", stepmode="backward"),
            dict(count=1, label="YTD", step="year", stepmode="todate"),
            dict(count=1, label="1y", step="year", stepmode="backward"),
            dict(step="all")      
            ])
    )
)
ustwoten.update_yaxes(title = '')
ustwoten.update_traces(line_color='#FF4500')
ustwoten.update_layout(
    plot_bgcolor='#1f2833',
    paper_bgcolor='#1f2833',
    font_color = 'white')

thirtyyrmortgage = px.line(thirtyyrmortgage, x='Date', y='Value', title='30 Yr Mortgage Rate')
thirtyyrmortgage.update_xaxes(
    title = 'Date Range',
    rangeslider_visible=True,
    rangeselector=dict(
        bgcolor = '#F89880',
        activecolor = '#FF4433',
        buttons=list([
            dict(count=1, label="1m", step="month", stepmode="backward"),
            dict(count=6, label="6m", step="month", stepmode="backward"),
            dict(count=1, label="YTD", step="year", stepmode="todate"),
            dict(count=1, label="1y", step="year", stepmode="backward"),
            dict(step="all")      
            ])
    )
)
thirtyyrmortgage.update_yaxes(title = '')
thirtyyrmortgage.update_traces(line_color='#FF4500')
thirtyyrmortgage.update_layout(
    plot_bgcolor='#1f2833',
    paper_bgcolor='#1f2833',
    font_color = 'white')

aaayieldidx = px.line(aaayieldidx, x='DATE', y='BAMLC0A1CAAAEY', title='AAA Corporate Bond Yield Index')
aaayieldidx.update_xaxes(
    title = 'Date Range',
    rangeslider_visible=True,
    rangeselector=dict(
        bgcolor = '#F89880',
        activecolor = '#FF4433',
        buttons=list([
            dict(count=1, label="1m", step="month", stepmode="backward"),
            dict(count=6, label="6m", step="month", stepmode="backward"),
            dict(count=1, label="YTD", step="year", stepmode="todate"),
            dict(count=1, label="1y", step="year", stepmode="backward"),
            dict(step="all")      
            ])
    )
)
aaayieldidx.update_yaxes(title = '')
aaayieldidx.update_traces(line_color='#FF4500')
aaayieldidx.update_layout(
    plot_bgcolor='#1f2833',
    paper_bgcolor='#1f2833',
    font_color = 'white')

bbbyieldidx = px.line(bbbyieldidx, x='DATE', y='BAMLC0A4CBBBEY', title='BBB Corporate Bond Yield Index')
bbbyieldidx.update_xaxes(
    title = 'Date Range',
    rangeslider_visible=True,
    rangeselector=dict(
        bgcolor = '#F89880',
        activecolor = '#FF4433',
        buttons=list([
            dict(count=1, label="1m", step="month", stepmode="backward"),
            dict(count=6, label="6m", step="month", stepmode="backward"),
            dict(count=1, label="YTD", step="year", stepmode="todate"),
            dict(count=1, label="1y", step="year", stepmode="backward"),
            dict(step="all")      
            ])
    )
)
bbbyieldidx.update_yaxes(title = '')
bbbyieldidx.update_traces(line_color='#FF4500')
bbbyieldidx.update_layout(
    plot_bgcolor='#1f2833',
    paper_bgcolor='#1f2833',
    font_color = 'white')

cccyieldidx = px.line(cccyieldidx, x='DATE', y='BAMLH0A3HYCEY', title='CCC Corporate Bond Yield Index')
cccyieldidx.update_xaxes(
    title = 'Date Range',
    rangeslider_visible=True,
    rangeselector=dict(
        bgcolor = '#F89880',
        activecolor = '#FF4433',
        buttons=list([
            dict(count=1, label="1m", step="month", stepmode="backward"),
            dict(count=6, label="6m", step="month", stepmode="backward"),
            dict(count=1, label="YTD", step="year", stepmode="todate"),
            dict(count=1, label="1y", step="year", stepmode="backward"),
            dict(step="all")      
            ])
    )
)
cccyieldidx.update_yaxes(title = '')
cccyieldidx.update_traces(line_color='#FF4500')
cccyieldidx.update_layout(
    plot_bgcolor='#1f2833',
    paper_bgcolor='#1f2833',
    font_color = 'white')

fiveyrtips = px.line(fiveyrtips, x='Date', y='Value', title='5 Year TIPs')
fiveyrtips.update_xaxes(
    title = 'Date Range',
    rangeslider_visible=True,
    rangeselector=dict(
        bgcolor = '#F89880',
        activecolor = '#FF4433',
        buttons=list([
            dict(count=1, label="1m", step="month", stepmode="backward"),
            dict(count=6, label="6m", step="month", stepmode="backward"),
            dict(count=1, label="YTD", step="year", stepmode="todate"),
            dict(count=1, label="1y", step="year", stepmode="backward"),
            dict(step="all")      
            ])
    )
)
fiveyrtips.update_yaxes(title = '')
fiveyrtips.update_traces(line_color='#FF4500')
fiveyrtips.update_layout(
    plot_bgcolor='#1f2833',
    paper_bgcolor='#1f2833',
    font_color = 'white')


tenyrtips = px.line(tenyrtips, x='Date', y='Value', title='10 Year TIPs')
tenyrtips.update_xaxes(
    title = 'Date Range',
    rangeslider_visible=True,
    rangeselector=dict(
        bgcolor = '#F89880',
        activecolor = '#FF4433',
        buttons=list([
            dict(count=1, label="1m", step="month", stepmode="backward"),
            dict(count=6, label="6m", step="month", stepmode="backward"),
            dict(count=1, label="YTD", step="year", stepmode="todate"),
            dict(count=1, label="1y", step="year", stepmode="backward"),
            dict(step="all")      
            ])
    )
)
tenyrtips.update_yaxes(title = '')
tenyrtips.update_traces(line_color='#FF4500')
tenyrtips.update_layout(
    plot_bgcolor='#1f2833',
    paper_bgcolor='#1f2833',
    font_color = 'white')

fiveyrbrkevninf = px.line(fiveyrbrkevninf, x='Date', y='Value', title='5 Yr BEI')
fiveyrbrkevninf.update_xaxes(
    title = 'Date Range',
    rangeslider_visible=True,
    rangeselector=dict(
        bgcolor = '#F89880',
        activecolor = '#FF4433',
        buttons=list([
            dict(count=1, label="1m", step="month", stepmode="backward"),
            dict(count=6, label="6m", step="month", stepmode="backward"),
            dict(count=1, label="YTD", step="year", stepmode="todate"),
            dict(count=1, label="1y", step="year", stepmode="backward"),
            dict(step="all")      
            ])
    )
)
fiveyrbrkevninf.update_yaxes(title = '')
fiveyrbrkevninf.update_traces(line_color='#FF4500')
fiveyrbrkevninf.update_layout(
    plot_bgcolor='#1f2833',
    paper_bgcolor='#1f2833',
    font_color = 'white')

tenyrbrkevninf = px.line(tenyrbrkevninf, x='Date', y='Value', title='10 Yr BEI')
tenyrbrkevninf.update_xaxes(
    title = 'Date Range',
    rangeslider_visible=True,
    rangeselector=dict(
        bgcolor = '#F89880',
        activecolor = '#FF4433',
        buttons=list([
            dict(count=1, label="1m", step="month", stepmode="backward"),
            dict(count=6, label="6m", step="month", stepmode="backward"),
            dict(count=1, label="YTD", step="year", stepmode="todate"),
            dict(count=1, label="1y", step="year", stepmode="backward"),
            dict(step="all")      
            ])
    )
)
tenyrbrkevninf.update_yaxes(title = '')
tenyrbrkevninf.update_traces(line_color='#FF4500')
tenyrbrkevninf.update_layout(
    plot_bgcolor='#1f2833',
    paper_bgcolor='#1f2833',
    font_color = 'white')

xwinflationsense = px.line(xwinflationsense, x='date', y='Price', title='XW Inflation Sense')
xwinflationsense.update_xaxes(
    title = 'Date Range',
    rangeslider_visible=True,
    rangeselector=dict(
        bgcolor = '#F89880',
        activecolor = '#FF4433',
        buttons=list([
            dict(count=1, label="1m", step="month", stepmode="backward"),
            dict(count=6, label="6m", step="month", stepmode="backward"),
            dict(count=1, label="YTD", step="year", stepmode="todate"),
            dict(count=1, label="1y", step="year", stepmode="backward"),
            dict(step="all")      
            ])
    )
)
xwinflationsense.update_yaxes(title = '')
xwinflationsense.update_traces(line_color='#FF4500')
xwinflationsense.update_layout(
    plot_bgcolor='#1f2833',
    paper_bgcolor='#1f2833',
    font_color = 'white')

broadfinancials = px.line(broadfinancials, x='date', y='Price', title='Broad Financials')
broadfinancials.update_xaxes(
    title = 'Date Range',
    rangeslider_visible=True,
    rangeselector=dict(
        bgcolor = '#F89880',
        activecolor = '#FF4433',
        buttons=list([
            dict(count=1, label="1m", step="month", stepmode="backward"),
            dict(count=6, label="6m", step="month", stepmode="backward"),
            dict(count=1, label="YTD", step="year", stepmode="todate"),
            dict(count=1, label="1y", step="year", stepmode="backward"),
            dict(step="all")      
            ])
    )
)
broadfinancials.update_yaxes(title = '')
broadfinancials.update_traces(line_color='#FF4500')
broadfinancials.update_layout(
    plot_bgcolor='#1f2833',
    paper_bgcolor='#1f2833',
    font_color = 'white')

selectedglobalfinancials = px.line(selectedglobalfinancials, x='date', y='Price', title='Selected Global Financials')
selectedglobalfinancials.update_xaxes(
    title = 'Date Range',
    rangeslider_visible=True,
    rangeselector=dict(
        bgcolor = '#F89880',
        activecolor = '#FF4433',
        buttons=list([
            dict(count=1, label="1m", step="month", stepmode="backward"),
            dict(count=6, label="6m", step="month", stepmode="backward"),
            dict(count=1, label="YTD", step="year", stepmode="todate"),
            dict(count=1, label="1y", step="year", stepmode="backward"),
            dict(step="all")      
            ])
    )
)
selectedglobalfinancials.update_yaxes(title = '')
selectedglobalfinancials.update_traces(line_color='#FF4500')
selectedglobalfinancials.update_layout(
    plot_bgcolor='#1f2833',
    paper_bgcolor='#1f2833',
    font_color = 'white')

broadutilities = px.line(broadutilities, x='date', y='Price', title='Broad Utilities')
broadutilities.update_xaxes(
    title = 'Date Range',
    rangeslider_visible=True,
    rangeselector=dict(
        bgcolor = '#F89880',
        activecolor = '#FF4433',
        buttons=list([
            dict(count=1, label="1m", step="month", stepmode="backward"),
            dict(count=6, label="6m", step="month", stepmode="backward"),
            dict(count=1, label="YTD", step="year", stepmode="todate"),
            dict(count=1, label="1y", step="year", stepmode="backward"),
            dict(step="all")      
            ])
    )
)
broadutilities.update_yaxes(title = '')
broadutilities.update_traces(line_color='#FF4500')
broadutilities.update_layout(
    plot_bgcolor='#1f2833',
    paper_bgcolor='#1f2833',
    font_color = 'white')

selectedglobalutilities = px.line(selectedglobalutilities, x='date', y='Price', title='Selected Global Utilities')
selectedglobalutilities.update_xaxes(
    title = 'Date Range',
    rangeslider_visible=True,
    rangeselector=dict(
        bgcolor = '#F89880',
        activecolor = '#FF4433',
        buttons=list([
            dict(count=1, label="1m", step="month", stepmode="backward"),
            dict(count=6, label="6m", step="month", stepmode="backward"),
            dict(count=1, label="YTD", step="year", stepmode="todate"),
            dict(count=1, label="1y", step="year", stepmode="backward"),
            dict(step="all")      
            ])
    )
)
selectedglobalutilities.update_yaxes(title = '')
selectedglobalutilities.update_traces(line_color='#FF4500')
selectedglobalutilities.update_layout(
    plot_bgcolor='#1f2833',
    paper_bgcolor='#1f2833',
    font_color = 'white')

broadconsumercore = px.line(broadconsumercore, x='date', y='Price', title='Broad Consumer Core')
broadconsumercore.update_xaxes(
    title = 'Date Range',
    rangeslider_visible=True,
    rangeselector=dict(
        bgcolor = '#F89880',
        activecolor = '#FF4433',
        buttons=list([
            dict(count=1, label="1m", step="month", stepmode="backward"),
            dict(count=6, label="6m", step="month", stepmode="backward"),
            dict(count=1, label="YTD", step="year", stepmode="todate"),
            dict(count=1, label="1y", step="year", stepmode="backward"),
            dict(step="all")      
            ])
    )
)
broadconsumercore.update_yaxes(title = '')
broadconsumercore.update_traces(line_color='#FF4500')
broadconsumercore.update_layout(
    plot_bgcolor='#1f2833',
    paper_bgcolor='#1f2833',
    font_color = 'white')

selectedglobalconsumercore = px.line(selectedglobalconsumercore, x='date', y='Price', title='Selected Global Consumer Core')
selectedglobalconsumercore.update_xaxes(
    title = 'Date Range',
    rangeslider_visible=True,
    rangeselector=dict(
        bgcolor = '#F89880',
        activecolor = '#FF4433',
        buttons=list([
            dict(count=1, label="1m", step="month", stepmode="backward"),
            dict(count=6, label="6m", step="month", stepmode="backward"),
            dict(count=1, label="YTD", step="year", stepmode="todate"),
            dict(count=1, label="1y", step="year", stepmode="backward"),
            dict(step="all")      
            ])
    )
)
selectedglobalconsumercore.update_yaxes(title = '')
selectedglobalconsumercore.update_traces(line_color='#FF4500')
selectedglobalconsumercore.update_layout(
    plot_bgcolor='#1f2833',
    paper_bgcolor='#1f2833',
    font_color = 'white')

broadconstruction = px.line(broadconstruction, x='date', y='Price', title='Broad Construction')
broadconstruction.update_xaxes(
    title = 'Date Range',
    rangeslider_visible=True,
    rangeselector=dict(
        bgcolor = '#F89880',
        activecolor = '#FF4433',
        buttons=list([
            dict(count=1, label="1m", step="month", stepmode="backward"),
            dict(count=6, label="6m", step="month", stepmode="backward"),
            dict(count=1, label="YTD", step="year", stepmode="todate"),
            dict(count=1, label="1y", step="year", stepmode="backward"),
            dict(step="all")      
            ])
    )
)
broadconstruction.update_yaxes(title = '')
broadconstruction.update_traces(line_color='#FF4500')
broadconstruction.update_layout(
    plot_bgcolor='#1f2833',
    paper_bgcolor='#1f2833',
    font_color = 'white')

selectedglobalconstruction = px.line(selectedglobalconstruction, x='date', y='Price', title='Selected Global Construction')
selectedglobalconstruction.update_xaxes(
    title = 'Date Range',
    rangeslider_visible=True,
    rangeselector=dict(
        bgcolor = '#F89880',
        activecolor = '#FF4433',
        buttons=list([
            dict(count=1, label="1m", step="month", stepmode="backward"),
            dict(count=6, label="6m", step="month", stepmode="backward"),
            dict(count=1, label="YTD", step="year", stepmode="todate"),
            dict(count=1, label="1y", step="year", stepmode="backward"),
            dict(step="all")      
            ])
    )
)
selectedglobalconstruction.update_yaxes(title = '')
selectedglobalconstruction.update_traces(line_color='#FF4500')
selectedglobalconstruction.update_layout(
    plot_bgcolor='#1f2833',
    paper_bgcolor='#1f2833',
    font_color = 'white')

broadmanu = px.line(broadmanu, x='date', y='Price', title='Broad Manufacturers')
broadmanu.update_xaxes(
    title = 'Date Range',
    rangeslider_visible=True,
    rangeselector=dict(
        bgcolor = '#F89880',
        activecolor = '#FF4433',
        buttons=list([
            dict(count=1, label="1m", step="month", stepmode="backward"),
            dict(count=6, label="6m", step="month", stepmode="backward"),
            dict(count=1, label="YTD", step="year", stepmode="todate"),
            dict(count=1, label="1y", step="year", stepmode="backward"),
            dict(step="all")      
            ])
    )
)
broadmanu.update_yaxes(title = '')
broadmanu.update_traces(line_color='#FF4500')
broadmanu.update_layout(
    plot_bgcolor='#1f2833',
    paper_bgcolor='#1f2833',
    font_color = 'white')

selectedglobalmanu = px.line(selectedglobalmanu, x='date', y='Price', title='Selected Global Manufacturers')
selectedglobalmanu.update_xaxes(
    title = 'Date Range',
    rangeslider_visible=True,
    rangeselector=dict(
        bgcolor = '#F89880',
        activecolor = '#FF4433',
        buttons=list([
            dict(count=1, label="1m", step="month", stepmode="backward"),
            dict(count=6, label="6m", step="month", stepmode="backward"),
            dict(count=1, label="YTD", step="year", stepmode="todate"),
            dict(count=1, label="1y", step="year", stepmode="backward"),
            dict(step="all")      
            ])
    )
)
selectedglobalmanu.update_yaxes(title = '')
selectedglobalmanu.update_traces(line_color='#FF4500')
selectedglobalmanu.update_layout(
    plot_bgcolor='#1f2833',
    paper_bgcolor='#1f2833',
    font_color = 'white')

broadtranspologistics = px.line(broadtranspologistics, x='date', y='Price', title='Broad Transportation/Logistics')
broadtranspologistics.update_xaxes(
    title = 'Date Range',
    rangeslider_visible=True,
    rangeselector=dict(
        bgcolor = '#F89880',
        activecolor = '#FF4433',
        buttons=list([
            dict(count=1, label="1m", step="month", stepmode="backward"),
            dict(count=6, label="6m", step="month", stepmode="backward"),
            dict(count=1, label="YTD", step="year", stepmode="todate"),
            dict(count=1, label="1y", step="year", stepmode="backward"),
            dict(step="all")      
            ])
    )
)
broadtranspologistics.update_yaxes(title = '')
broadtranspologistics.update_traces(line_color='#FF4500')
broadtranspologistics.update_layout(
    plot_bgcolor='#1f2833',
    paper_bgcolor='#1f2833',
    font_color = 'white')

selectedglobaltranslogi = px.line(selectedglobaltranslogi, x='date', y='Price', title='Selected Global Transportation/Logistics')
selectedglobaltranslogi.update_xaxes(
    title = 'Date Range',
    rangeslider_visible=True,
    rangeselector=dict(
        bgcolor = '#F89880',
        activecolor = '#FF4433',
        buttons=list([
            dict(count=1, label="1m", step="month", stepmode="backward"),
            dict(count=6, label="6m", step="month", stepmode="backward"),
            dict(count=1, label="YTD", step="year", stepmode="todate"),
            dict(count=1, label="1y", step="year", stepmode="backward"),
            dict(step="all")      
            ])
    )
)
selectedglobaltranslogi.update_yaxes(title = '')
selectedglobaltranslogi.update_traces(line_color='#FF4500')
selectedglobaltranslogi.update_layout(
    plot_bgcolor='#1f2833',
    paper_bgcolor='#1f2833',
    font_color = 'white')

broadsemi = px.line(broadsemi, x='date', y='Price', title='Broad Semiconductors')
broadsemi.update_xaxes(
    title = 'Date Range',
    rangeslider_visible=True,
    rangeselector=dict(
        bgcolor = '#F89880',
        activecolor = '#FF4433',
        buttons=list([
            dict(count=1, label="1m", step="month", stepmode="backward"),
            dict(count=6, label="6m", step="month", stepmode="backward"),
            dict(count=1, label="YTD", step="year", stepmode="todate"),
            dict(count=1, label="1y", step="year", stepmode="backward"),
            dict(step="all")      
            ])
    )
)
broadsemi.update_yaxes(title = '')
broadsemi.update_traces(line_color='#FF4500')
broadsemi.update_layout(
    plot_bgcolor='#1f2833',
    paper_bgcolor='#1f2833',
    font_color = 'white')

selectedglobalsemi = px.line(selectedglobalsemi, x='date', y='Price', title='Selected Global Semiconductors')
selectedglobalsemi.update_xaxes(
    title = 'Date Range',
    rangeslider_visible=True,
    rangeselector=dict(
        bgcolor = '#F89880',
        activecolor = '#FF4433',
        buttons=list([
            dict(count=1, label="1m", step="month", stepmode="backward"),
            dict(count=6, label="6m", step="month", stepmode="backward"),
            dict(count=1, label="YTD", step="year", stepmode="todate"),
            dict(count=1, label="1y", step="year", stepmode="backward"),
            dict(step="all")      
            ])
    )
)
selectedglobalsemi.update_yaxes(title = '')
selectedglobalsemi.update_traces(line_color='#FF4500')
selectedglobalsemi.update_layout(
    plot_bgcolor='#1f2833',
    paper_bgcolor='#1f2833',
    font_color = 'white')

broadcomms = px.line(broadcomms, x='date', y='Price', title='Broad Communications')
broadcomms.update_xaxes(
    title = 'Date Range',
    rangeslider_visible=True,
    rangeselector=dict(
        bgcolor = '#F89880',
        activecolor = '#FF4433',
        buttons=list([
            dict(count=1, label="1m", step="month", stepmode="backward"),
            dict(count=6, label="6m", step="month", stepmode="backward"),
            dict(count=1, label="YTD", step="year", stepmode="todate"),
            dict(count=1, label="1y", step="year", stepmode="backward"),
            dict(step="all")      
            ])
    )
)
broadcomms.update_yaxes(title = '')
broadcomms.update_traces(line_color='#FF4500')
broadcomms.update_layout(
    plot_bgcolor='#1f2833',
    paper_bgcolor='#1f2833',
    font_color = 'white')

selectedglobalcomms = px.line(selectedglobalcomms, x='date', y='Price', title='Selected Global Communications')
selectedglobalcomms.update_xaxes(
    title = 'Date Range',
    rangeslider_visible=True,
    rangeselector=dict(
        bgcolor = '#F89880',
        activecolor = '#FF4433',
        buttons=list([
            dict(count=1, label="1m", step="month", stepmode="backward"),
            dict(count=6, label="6m", step="month", stepmode="backward"),
            dict(count=1, label="YTD", step="year", stepmode="todate"),
            dict(count=1, label="1y", step="year", stepmode="backward"),
            dict(step="all")      
            ])
    )
)
selectedglobalcomms.update_yaxes(title = '')
selectedglobalcomms.update_traces(line_color='#FF4500')
selectedglobalcomms.update_layout(
    plot_bgcolor='#1f2833',
    paper_bgcolor='#1f2833',
    font_color = 'white')

broadhealthbiotech = px.line(broadhealthbiotech, x='date', y='Price', title='Broad Health & Biotech')
broadhealthbiotech.update_xaxes(
    title = 'Date Range',
    rangeslider_visible=True,
    rangeselector=dict(
        bgcolor = '#F89880',
        activecolor = '#FF4433',
        buttons=list([
            dict(count=1, label="1m", step="month", stepmode="backward"),
            dict(count=6, label="6m", step="month", stepmode="backward"),
            dict(count=1, label="YTD", step="year", stepmode="todate"),
            dict(count=1, label="1y", step="year", stepmode="backward"),
            dict(step="all")      
            ])
    )
)
broadhealthbiotech.update_yaxes(title = '')
broadhealthbiotech.update_traces(line_color='#FF4500')
broadhealthbiotech.update_layout(
    plot_bgcolor='#1f2833',
    paper_bgcolor='#1f2833',
    font_color = 'white')

selectedglobalbiohealth = px.line(selectedglobalbiohealth, x='date', y='Price', title='Selected Global Health & Biotech')
selectedglobalbiohealth.update_xaxes(
    title = 'Date Range',
    rangeslider_visible=True,
    rangeselector=dict(
        bgcolor = '#F89880',
        activecolor = '#FF4433',
        buttons=list([
            dict(count=1, label="1m", step="month", stepmode="backward"),
            dict(count=6, label="6m", step="month", stepmode="backward"),
            dict(count=1, label="YTD", step="year", stepmode="todate"),
            dict(count=1, label="1y", step="year", stepmode="backward"),
            dict(step="all")      
            ])
    )
)
selectedglobalbiohealth.update_yaxes(title = '')
selectedglobalbiohealth.update_traces(line_color='#FF4500')
selectedglobalbiohealth.update_layout(
    plot_bgcolor='#1f2833',
    paper_bgcolor='#1f2833',
    font_color = 'white')

broadentertainment = px.line(broadentertainment, x='date', y='Price', title='Broad Entertainment')
broadentertainment.update_xaxes(
    title = 'Date Range',
    rangeslider_visible=True,
    rangeselector=dict(
        bgcolor = '#F89880',
        activecolor = '#FF4433',
        buttons=list([
            dict(count=1, label="1m", step="month", stepmode="backward"),
            dict(count=6, label="6m", step="month", stepmode="backward"),
            dict(count=1, label="YTD", step="year", stepmode="todate"),
            dict(count=1, label="1y", step="year", stepmode="backward"),
            dict(step="all")      
            ])
    )
)
broadentertainment.update_yaxes(title = '')
broadentertainment.update_traces(line_color='#FF4500')
broadentertainment.update_layout(
    plot_bgcolor='#1f2833',
    paper_bgcolor='#1f2833',
    font_color = 'white')

selectedglobalentertainment = px.line(selectedglobalentertainment, x='date', y='Price', title='Selected Global Entertainment')
selectedglobalentertainment.update_xaxes(
    title = 'Date Range',
    rangeslider_visible=True,
    rangeselector=dict(
        bgcolor = '#F89880',
        activecolor = '#FF4433',
        buttons=list([
            dict(count=1, label="1m", step="month", stepmode="backward"),
            dict(count=6, label="6m", step="month", stepmode="backward"),
            dict(count=1, label="YTD", step="year", stepmode="todate"),
            dict(count=1, label="1y", step="year", stepmode="backward"),
            dict(step="all")      
            ])
    )
)
selectedglobalentertainment.update_yaxes(title = '')
selectedglobalentertainment.update_traces(line_color='#FF4500')
selectedglobalentertainment.update_layout(
    plot_bgcolor='#1f2833',
    paper_bgcolor='#1f2833',
    font_color = 'white')

broadconsumeredge = px.line(broadconsumeredge, x='date', y='Price', title='Broad Consumer Edge')
broadconsumeredge.update_xaxes(
    title = 'Date Range',
    rangeslider_visible=True,
    rangeselector=dict(
        bgcolor = '#F89880',
        activecolor = '#FF4433',
        buttons=list([
            dict(count=1, label="1m", step="month", stepmode="backward"),
            dict(count=6, label="6m", step="month", stepmode="backward"),
            dict(count=1, label="YTD", step="year", stepmode="todate"),
            dict(count=1, label="1y", step="year", stepmode="backward"),
            dict(step="all")      
            ])
    )
)
broadconsumeredge.update_yaxes(title = '')
broadconsumeredge.update_traces(line_color='#FF4500')
broadconsumeredge.update_layout(
    plot_bgcolor='#1f2833',
    paper_bgcolor='#1f2833',
    font_color = 'white')

selectedglobalconsumeredge = px.line(selectedglobalconsumeredge, x='date', y='Price', title='Selected Global Consumer Edge')
selectedglobalconsumeredge.update_xaxes(
    title = 'Date Range',
    rangeslider_visible=True,
    rangeselector=dict(
        bgcolor = '#F89880',
        activecolor = '#FF4433',
        buttons=list([
            dict(count=1, label="1m", step="month", stepmode="backward"),
            dict(count=6, label="6m", step="month", stepmode="backward"),
            dict(count=1, label="YTD", step="year", stepmode="todate"),
            dict(count=1, label="1y", step="year", stepmode="backward"),
            dict(step="all")      
            ])
    )
)
selectedglobalconsumeredge.update_yaxes(title = '')
selectedglobalconsumeredge.update_traces(line_color='#FF4500')
selectedglobalconsumeredge.update_layout(
    plot_bgcolor='#1f2833',
    paper_bgcolor='#1f2833',
    font_color = 'white')

gld = px.line(gld, x='date', y='close', title='SPDR Gold')
gld.update_xaxes(
    title = 'Date Range',
    rangeslider_visible=True,
    rangeselector=dict(
        bgcolor = '#F89880',
        activecolor = '#FF4433',
        buttons=list([
            dict(count=1, label="1m", step="month", stepmode="backward"),
            dict(count=6, label="6m", step="month", stepmode="backward"),
            dict(count=1, label="YTD", step="year", stepmode="todate"),
            dict(count=1, label="1y", step="year", stepmode="backward"),
            dict(step="all")      
            ])
    )
)
gld.update_yaxes(title = '')
gld.update_traces(line_color='#FF4500')
gld.update_layout(
    plot_bgcolor='#1f2833',
    paper_bgcolor='#1f2833',
    font_color = 'white')

dbb = px.line(dbb, x='date', y='close', title='Invesco Base Metals')
dbb.update_xaxes(
    title = 'Date Range',
    rangeslider_visible=True,
    rangeselector=dict(
        bgcolor = '#F89880',
        activecolor = '#FF4433',
        buttons=list([
            dict(count=1, label="1m", step="month", stepmode="backward"),
            dict(count=6, label="6m", step="month", stepmode="backward"),
            dict(count=1, label="YTD", step="year", stepmode="todate"),
            dict(count=1, label="1y", step="year", stepmode="backward"),
            dict(step="all")      
            ])
    )
)
dbb.update_yaxes(title = '')
dbb.update_traces(line_color='#FF4500')
dbb.update_layout(
    plot_bgcolor='#1f2833',
    paper_bgcolor='#1f2833',
    font_color = 'white')

gbtc = px.line(gbtc, x='date', y='close', title='Grayscale Bitcoin Trust')
gbtc.update_xaxes(
    title = 'Date Range',
    rangeslider_visible=True,
    rangeselector=dict(
        bgcolor = '#F89880',
        activecolor = '#FF4433',
        buttons=list([
            dict(count=1, label="1m", step="month", stepmode="backward"),
            dict(count=6, label="6m", step="month", stepmode="backward"),
            dict(count=1, label="YTD", step="year", stepmode="todate"),
            dict(count=1, label="1y", step="year", stepmode="backward"),
            dict(step="all")      
            ])
    )
)
gbtc.update_yaxes(title = '')
gbtc.update_traces(line_color='#FF4500')
gbtc.update_layout(
    plot_bgcolor='#1f2833',
    paper_bgcolor='#1f2833',
    font_color = 'white')

ethe = px.line(ethe, x='date', y='close', title='Grayscale Ethereum Trust')
ethe.update_xaxes(
    title = 'Date Range',
    rangeslider_visible=True,
    rangeselector=dict(
        bgcolor = '#F89880',
        activecolor = '#FF4433',
        buttons=list([
            dict(count=1, label="1m", step="month", stepmode="backward"),
            dict(count=6, label="6m", step="month", stepmode="backward"),
            dict(count=1, label="YTD", step="year", stepmode="todate"),
            dict(count=1, label="1y", step="year", stepmode="backward"),
            dict(step="all")      
            ])
    )
)
ethe.update_yaxes(title = '')
ethe.update_traces(line_color='#FF4500')
ethe.update_layout(
    plot_bgcolor='#1f2833',
    paper_bgcolor='#1f2833',
    font_color = 'white')

app.layout = html.Div([ #big block\

    html.H1(children='MACRO DASH v2'),

    html.Div(className = 'globalequity', children=[
        html.H2(children='Global Equity'),

        html.Div([ #small block upper most

        dcc.Graph(
            id='xwglobalequitysense',
            figure=xwglobalequitysense),
        ],
        className = 'longformgraph',
        style={
            'width': '70.8%', 
            'margin-left' : '15rem',
            'margin-bottom' : '5px',
            'display' : 'inline-block',
            }
        ),

        html.Div([ #small block upper most

        dcc.Graph(
            id='voo',
            figure=voo
        ),

        ]
        ,className = 'twobytwoleft',
        style={
            'width': '35%', 
            'margin-left' : '15rem',
            'margin-right' : '7.5px',
            'margin-bottom' : '5px',
            'margin-top' : '5px',
            'display' : 'inline-block',
        }
        ),

        html.Div([ #small block upper most

        dcc.Graph(
            id='mchi',
            figure=mchi
        ),

        ]
        ,className = 'twobytworight',
        style={
            'width': '35%', 
            'display' : 'inline-block',
            'margin-left' : '7.5px',
            'margin-top' : '5px',
            'margin-bottom' : '5px',
            }
        ),

        html.Div([ #small block upper most

        dcc.Graph(
            id='ewj',
            figure=ewj
        ),

        ]
        ,className = 'twobytwoleft',
        style={
            'width': '35%', 
            'margin-left' : '15rem',
            'margin-right' : '7.5px',
            'margin-bottom' : '5px',
            'margin-top' : '5px',
            'display' : 'inline-block',
        }
        ),

        html.Div([ #small block upper most

        dcc.Graph(
            id='ewg',
            figure=ewg
        ),
        ]
        ,className = 'twobytworight',
        style={
            'width': '35%', 
            'display' : 'inline-block',
            'margin-left' : '7.5px',
            'margin-top' : '5px',
            'margin-bottom' : '5px',
            }
        ),
                
        html.Div([ #small block upper most

        dcc.Graph(
            id='ewu',
            figure=ewu),
        ]
        ,className = 'twobytwoleft',
        style={
            'width': '35%', 
            'margin-left' : '15rem',
            'margin-right' : '7.5px',
            'margin-bottom' : '5px',
            'margin-top' : '5px',
            'display' : 'inline-block',
        }
        ),

        html.Div([ #small block upper most

        dcc.Graph(
            id='ewq',
            figure=ewq),
        ]
        ,className = 'twobytworight',
        style={
            'width': '35%', 
            'display' : 'inline-block',
            'margin-left' : '7.5px',
            'margin-top' : '5px',
            'margin-bottom' : '5px',
            }
        ),

        html.Div([ #small block upper most

        dcc.Graph(
            id='ewc',
            figure=ewc
        ),

        ]
        ,className = 'twobytwoleft',
        style={
            'width': '35%', 
            'margin-left' : '15rem',
            'margin-right' : '7.5px',
            'margin-bottom' : '5px',
            'margin-top' : '5px',
            'display' : 'inline-block',
        }
        ),

        html.Div([ #small block upper most

        dcc.Graph(
            id='ewa',
            figure=ewa
        ),

        ]
        ,className = 'twobytworight',
        style={
            'width': '35%', 
            'display' : 'inline-block',
            'margin-left' : '7.5px',
            'margin-top' : '5px',
            'margin-bottom' : '5px',
            }
        ),


    ]),
    
    html.Div(className = 'foundational', children=[
        html.H2(children='Foundational Core'),

        html.Div([ #small block upper most

        dcc.Graph(
            id='selectedglobalstaffing',
            figure=selectedglobalstaffing),
        ],
        className = 'longformgraph',
        style={
            'width': '70.8%', 
            'margin-left' : '15rem',
            'margin-bottom' : '5px',
            'display' : 'inline-block',
            }
        ),

        html.Div([ #small block upper most

        dcc.Graph(
            id='indeedus',
            figure=indeedus
        ),

        ]
        ,className = 'twobytwoleft',
        style={
            'width': '35%', 
            'margin-left' : '15rem',
            'margin-right' : '7.5px',
            'margin-bottom' : '5px',
            'margin-top' : '5px',
            'display' : 'inline-block',
        }
        ),

        html.Div([ #small block upper most

        dcc.Graph(
            id='indeednewus',
            figure=indeednewus
        ),

        ]
        ,className = 'twobytworight',
        style={
            'width': '35%', 
            'display' : 'inline-block',
            'margin-left' : '7.5px',
            'margin-top' : '5px',
            'margin-bottom' : '5px',
            }
        ),

        html.Div([ #small block upper most

        dcc.Graph(
            id='broadreits',
            figure=broadreits
        ),

        ]
        ,className = 'twobytwoleft',
        style={
            'width': '35%', 
            'margin-left' : '15rem',
            'margin-right' : '7.5px',
            'margin-bottom' : '5px',
            'margin-top' : '5px',
            'display' : 'inline-block',
        }
        ),

        html.Div([ #small block upper most

        dcc.Graph(
            id='selectedglobalrealestate',
            figure=selectedglobalrealestate
        ),
        ]
        ,className = 'twobytworight',
        style={
            'width': '35%', 
            'display' : 'inline-block',
            'margin-left' : '7.5px',
            'margin-top' : '5px',
            'margin-bottom' : '5px',
            }
        ),
                
        html.Div([ #small block upper most

        dcc.Graph(
            id='broadaeroanddefenseplot',
            figure=broadaeroanddefenseplot),
        ]
        ,className = 'twobytwoleft',
        style={
            'width': '35%', 
            'margin-left' : '15rem',
            'margin-right' : '7.5px',
            'margin-bottom' : '5px',
            'margin-top' : '5px',
            'display' : 'inline-block',
        }
        ),

        html.Div([ #small block upper most

        dcc.Graph(
            id='selectedglobaldefense',
            figure=selectedglobaldefense),
        ]
        ,className = 'twobytworight',
        style={
            'width': '35%', 
            'display' : 'inline-block',
            'margin-left' : '7.5px',
            'margin-top' : '5px',
            'margin-bottom' : '5px',
            }
        ),

     html.Div([ #small block upper most

        dcc.Graph(
            id='stapleagri',
            figure=stapleagri),
        ]
        ,className = 'longformgraph',
        style={
            'width': '70.8%', 
            'margin-left' : '15rem',
            'margin-top' : '5px',
            'margin-bottom' : '5px',
            'display' : 'inline-block',
            }
        ),

        html.Div([ #small block upper most

        dcc.Graph(
            id='corn',
            figure=corn
        ),

        ]
        ,className = 'twobytwoleft',
        style={
            'width': '35%', 
            'margin-left' : '15rem',
            'margin-right' : '7.5px',
            'margin-bottom' : '5px',
            'margin-top' : '5px',
            'display' : 'inline-block',
        }
        ),

        html.Div([ #small block upper most

        dcc.Graph(
            id='weat',
            figure=weat
        ),

        ]
        ,className = 'twobytworight',
        style={
            'width': '35%', 
            'display' : 'inline-block',
            'margin-left' : '7.5px',
            'margin-top' : '5px',
            'margin-bottom' : '5px',
            }
        ),


    ]),

    html.Div(className = 'moderncore', children=[
        html.H2(children='Modern Core'),

        html.Div([ #small block upper most

        dcc.Graph(
            id='broadmetals',
            figure=broadmetals
        ),

        ]
        ,className = 'twobytwoleft',
        style={
            'width': '35%', 
            'margin-left' : '15rem',
            'margin-right' : '7.5px',
            'margin-bottom' : '5px',
            'margin-top' : '5px',
            'display' : 'inline-block',
        }
        ),

        html.Div([ #small block upper most

        dcc.Graph(
            id='selectedmetals',
            figure=selectedmetals
        ),

        ]
        ,className = 'twobytworight',
        style={
            'width': '35%', 
            'display' : 'inline-block',
            'margin-left' : '7.5px',
            'margin-top' : '5px',
            'margin-bottom' : '5px',
            }
        ),

        html.Div([ #small block upper most

        dcc.Graph(
            id='dbb',
            figure=dbb
        ),

        ]
        ,className = 'twobytwoleft',
        style={
            'width': '35%', 
            'margin-left' : '15rem',
            'margin-right' : '7.5px',
            'margin-bottom' : '5px',
            'margin-top' : '5px',
            'display' : 'inline-block',
        }
        ),

        html.Div([ #small block upper most

        dcc.Graph(
            id='gld',
            figure=gld
        ),

        ]
        ,className = 'twobytworight',
        style={
            'width': '35%', 
            'display' : 'inline-block',
            'margin-left' : '7.5px',
            'margin-top' : '5px',
            'margin-bottom' : '5px',
            }
        ),

        html.Div([ #small block upper most

        dcc.Graph(
            id='broadlumber',
            figure=broadlumber
        ),

        ]
        ,className = 'twobytwoleft',
        style={
            'width': '35%', 
            'margin-left' : '15rem',
            'margin-right' : '7.5px',
            'margin-bottom' : '5px',
            'margin-top' : '5px',
            'display' : 'inline-block',
        }
        ),

        html.Div([ #small block upper most

        dcc.Graph(
            id='selectedgloballumber',
            figure=selectedgloballumber
        ),
        ]
        ,className = 'twobytworight',
        style={
            'width': '35%', 
            'display' : 'inline-block',
            'margin-left' : '7.5px',
            'margin-top' : '5px',
            'margin-bottom' : '5px',
            }
        ),
                
        html.Div([ #small block upper most

        dcc.Graph(
            id='broadoilandgas',
            figure=broadoilandgas),
        ]
        ,className = 'twobytwoleft',
        style={
            'width': '35%', 
            'margin-left' : '15rem',
            'margin-right' : '7.5px',
            'margin-bottom' : '5px',
            'margin-top' : '5px',
            'display' : 'inline-block',
        }
        ),

        html.Div([ #small block upper most

        dcc.Graph(
            id='selectedglobaloilandgas',
            figure=selectedglobaloilandgas),
        ]
        ,className = 'twobytworight',
        style={
            'width': '35%', 
            'display' : 'inline-block',
            'margin-left' : '7.5px',
            'margin-top' : '5px',
            'margin-bottom' : '5px',
            }
        ),

        html.Div([ #small block upper most

        dcc.Graph(
            id='opeccrude',
            figure=opeccrude),
        ]
        ,className = 'longformgraph',
        style={
            'width': '70.8%', 
            'margin-left' : '15rem',
            'margin-bottom' : '5px',
            'display' : 'inline-block',
            }
        ),    

        html.Div([ #small block upper most

        dcc.Graph(
            id='bno',
            figure=bno),
        ]
        ,className = 'twobytwoleft',
        style={
            'width': '35%', 
            'margin-left' : '15rem',
            'margin-right' : '7.5px',
            'margin-bottom' : '5px',
            'margin-top' : '5px',
            'display' : 'inline-block',
            }
        ),   

        html.Div([ #small block upper most

        dcc.Graph(
            id='ung',
            figure=ung),
        ]
        ,className = 'twobytworight',
        style={
            'width': '35%', 
            'display' : 'inline-block',
            'margin-left' : '7.5px',
            'margin-top' : '5px',
            'margin-bottom' : '5px',
            }
        ),  

        html.Div([ #small block upper most

        dcc.Graph(
            id='broadcleanenergy',
            figure=broadcleanenergy
        ),

        ]
        ,className = 'twobytwoleft',
        style={
            'width': '35%', 
            'margin-left' : '15rem',
            'margin-right' : '7.5px',
            'margin-bottom' : '5px',
            'margin-top' : '5px',
            'display' : 'inline-block',
        }
        ),

        html.Div([ #small block upper most

        dcc.Graph(
            id='selectedglobalcleanenergy',
            figure=selectedglobalcleanenergy
        ),

        ]
        ,className = 'twobytworight',
        style={
            'width': '35%', 
            'display' : 'inline-block',
            'margin-left' : '7.5px',
            'margin-top' : '5px',
            'margin-bottom' : '5px',
            }
        ),

        html.Div([ #small block upper most

        dcc.Graph(
            id='gbpusd',
            figure=gbpusd),
        ]
        ,className = 'twobytwoleft',
        style={
            'width': '35%', 
            'margin-left' : '15rem',
            'margin-right' : '7.5px',
            'margin-bottom' : '5px',
            'margin-top' : '5px',
            'display' : 'inline-block',
            }
        ),    

        html.Div([ #small block upper most

        dcc.Graph(
            id='eurusd',
            figure=eurusd),
        ]
        ,className = 'twobytworight',
        style={
            'width': '35%', 
            'display' : 'inline-block',
            'margin-left' : '7.5px',
            'margin-top' : '5px',
            'margin-bottom' : '5px',
            }
        ),   

        html.Div([ #small block upper most

        dcc.Graph(
            id='usdjpy',
            figure=usdjpy),
        ]
        ,className = 'twobytwoleft',
        style={
            'width': '35%', 
            'margin-left' : '15rem',
            'margin-right' : '7.5px',
            'margin-bottom' : '5px',
            'margin-top' : '5px',
            'display' : 'inline-block',
            }
        ),  

        html.Div([ #small block upper most

        dcc.Graph(
            id='usdchf',
            figure=usdchf),
        ]
        ,className = 'twobytworight',
        style={
            'width': '35%', 
            'display' : 'inline-block',
            'margin-left' : '7.5px',
            'margin-top' : '5px',
            'margin-bottom' : '5px',
            }
        ),  

        html.Div([ #small block upper most

        dcc.Graph(
            id='audusd',
            figure=audusd),
        ]
        ,className = 'twobytwoleft',
        style={
            'width': '35%', 
            'margin-left' : '15rem',
            'margin-right' : '7.5px',
            'margin-bottom' : '5px',
            'margin-top' : '5px',
            'display' : 'inline-block',
            }
        ),    

        html.Div([ #small block upper most

        dcc.Graph(
            id='usdcad',
            figure=usdcad),
        ]
        ,className = 'twobytworight',
        style={
            'width': '35%', 
            'display' : 'inline-block',
            'margin-left' : '7.5px',
            'margin-top' : '5px',
            'margin-bottom' : '5px',
            }
        ),   

        html.Div([ #small block upper most

        dcc.Graph(
            id='usfedfundsrate',
            figure=usfedfundsrate
        ),

        ]
        ,className = 'twobytwoleft',
        style={
            'width': '35%', 
            'margin-left' : '15rem',
            'margin-right' : '7.5px',
            'margin-bottom' : '5px',
            'margin-top' : '5px',
            'display' : 'inline-block',
        }
        ),

        html.Div([ #small block upper most

        dcc.Graph(
            id='discountrate',
            figure=discountrate
        ),

        ]
        ,className = 'twobytworight',
        style={
            'width': '35%', 
            'display' : 'inline-block',
            'margin-left' : '7.5px',
            'margin-top' : '5px',
            'margin-bottom' : '5px',
            }
        ),
        
        html.Div([ #small block upper most

        dcc.Graph(
            id='tenyrtreasbenchmark',
            figure=tenyrtreasbenchmark
        ),

        ]
        ,className = 'twobytwoleft',
        style={
            'width': '35%', 
            'margin-left' : '15rem',
            'margin-right' : '7.5px',
            'margin-bottom' : '5px',
            'margin-top' : '5px',
            'display' : 'inline-block',
        }
        ),

        html.Div([ #small block upper most

        dcc.Graph(
            id='ustwoten',
            figure=ustwoten
        ),

        ]
        ,className = 'twobytworight',
        style={
            'width': '35%', 
            'display' : 'inline-block',
            'margin-left' : '7.5px',
            'margin-top' : '5px',
            'margin-bottom' : '5px',
            }
        ),

        html.Div([ #small block upper most

        dcc.Graph(
            id='thirtyyrmortgage',
            figure=thirtyyrmortgage
        ),

        ]
        ,className = 'longformgraph',
        style={
            'width': '70.8%', 
            'margin-left' : '15rem',
            'margin-top' : '5px',
            'margin-bottom' : '5px',
            'display' : 'inline-block',
            }
        ),

        html.Div([ #small block upper most

        dcc.Graph(
            id='aaayieldidx',
            figure=aaayieldidx),
        ]
        ,className = 'longformgraph',
        style={
            'width': '70.8%', 
            'margin-left' : '15rem',
            'margin-bottom' : '5px',
            'display' : 'inline-block',
            }
        ),    

        html.Div([ #small block upper most

        dcc.Graph(
            id='bbbyieldidx',
            figure=bbbyieldidx),
        ]
        ,className = 'twobytwoleft',
        style={
            'width': '35%', 
            'margin-left' : '15rem',
            'margin-right' : '7.5px',
            'margin-bottom' : '5px',
            'margin-top' : '5px',
            'display' : 'inline-block',
            }
        ),   

        html.Div([ #small block upper most

        dcc.Graph(
            id='cccyieldidx',
            figure=cccyieldidx),
        ]
        ,className = 'twobytworight',
        style={
            'width': '35%', 
            'display' : 'inline-block',
            'margin-left' : '7.5px',
            'margin-top' : '5px',
            'margin-bottom' : '5px',
            }
        ),  

        html.Div([ #small block upper most

        dcc.Graph(
            id='xwinflationsense',
            figure=xwinflationsense),
        ]
        ,className = 'longformgraph',
        style={
            'width': '70.8%', 
            'margin-left' : '15rem',
            'margin-bottom' : '5px',
            'display' : 'inline-block',
            }
        ),   

        html.Div([ #small block upper most

        dcc.Graph(
            id='fiveyrtips',
            figure=fiveyrtips),
        ]
        ,className = 'twobytwoleft',
        style={
            'width': '35%', 
            'margin-left' : '15rem',
            'margin-right' : '7.5px',
            'margin-bottom' : '5px',
            'margin-top' : '5px',
            'display' : 'inline-block',
            }
        ),   

        html.Div([ #small block upper most

        dcc.Graph(
            id='tenyrtips',
            figure=tenyrtips),
        ]
        ,className = 'twobytworight',
        style={
            'width': '35%', 
            'display' : 'inline-block',
            'margin-left' : '7.5px',
            'margin-top' : '5px',
            'margin-bottom' : '5px',
            }
        ),  

        html.Div([ #small block upper most

        dcc.Graph(
            id='fiveyrbrkevninf',
            figure=fiveyrbrkevninf),
        ]
        ,className = 'twobytwoleft',
        style={
            'width': '35%', 
            'margin-left' : '15rem',
            'margin-right' : '7.5px',
            'margin-bottom' : '5px',
            'margin-top' : '5px',
            'display' : 'inline-block',
            }
        ),   

        html.Div([ #small block upper most

        dcc.Graph(
            id='tenyrbrkevninf',
            figure=tenyrbrkevninf),
        ]
        ,className = 'twobytworight',
        style={
            'width': '35%', 
            'display' : 'inline-block',
            'margin-left' : '7.5px',
            'margin-top' : '5px',
            'margin-bottom' : '5px',
            }
        ),  

        html.Div([ #small block upper most

        dcc.Graph(
            id='broadfinancials',
            figure=broadfinancials),
        ]
        ,className = 'twobytwoleft',
        style={
            'width': '35%', 
            'margin-left' : '15rem',
            'margin-right' : '7.5px',
            'margin-bottom' : '5px',
            'margin-top' : '5px',
            'display' : 'inline-block',
            }
        ),   

        html.Div([ #small block upper most

        dcc.Graph(
            id='selectedglobalfinancials',
            figure=selectedglobalfinancials),
        ]
        ,className = 'twobytworight',
        style={
            'width': '35%', 
            'display' : 'inline-block',
            'margin-left' : '7.5px',
            'margin-top' : '5px',
            'margin-bottom' : '5px',
            }
        ), 

        html.Div([ #small block upper most

        dcc.Graph(
            id='broadutilities',
            figure=broadutilities),
        ]
        ,className = 'twobytwoleft',
        style={
            'width': '35%', 
            'margin-left' : '15rem',
            'margin-right' : '7.5px',
            'margin-bottom' : '5px',
            'margin-top' : '5px',
            'display' : 'inline-block',
            }
        ),   

        html.Div([ #small block upper most

        dcc.Graph(
            id='selectedglobalutilities',
            figure=selectedglobalutilities),
        ]
        ,className = 'twobytworight',
        style={
            'width': '35%', 
            'display' : 'inline-block',
            'margin-left' : '7.5px',
            'margin-top' : '5px',
            'margin-bottom' : '5px',
            }
        ), 

        html.Div([ #small block upper most

        dcc.Graph(
            id='broadconsumercore',
            figure=broadconsumercore),
        ]
        ,className = 'twobytwoleft',
        style={
            'width': '35%', 
            'margin-left' : '15rem',
            'margin-right' : '7.5px',
            'margin-bottom' : '5px',
            'margin-top' : '5px',
            'display' : 'inline-block',
            }
        ),   

        html.Div([ #small block upper most

        dcc.Graph(
            id='selectedglobalconsumercore',
            figure=selectedglobalconsumercore),
        ]
        ,className = 'twobytworight',
        style={
            'width': '35%', 
            'display' : 'inline-block',
            'margin-left' : '7.5px',
            'margin-top' : '5px',
            'margin-bottom' : '5px',
            }
        ), 

        html.Div([ #small block upper most

        dcc.Graph(
            id='broadconstruction',
            figure=broadconstruction),
        ]
        ,className = 'twobytwoleft',
        style={
            'width': '35%', 
            'margin-left' : '15rem',
            'margin-right' : '7.5px',
            'margin-bottom' : '5px',
            'margin-top' : '5px',
            'display' : 'inline-block',
            }
        ),   

        html.Div([ #small block upper most

        dcc.Graph(
            id='selectedglobalconstruction',
            figure=selectedglobalconstruction),
        ]
        ,className = 'twobytworight',
        style={
            'width': '35%', 
            'display' : 'inline-block',
            'margin-left' : '7.5px',
            'margin-top' : '5px',
            'margin-bottom' : '5px',
            }
        ),

        html.Div([ #small block upper most

        dcc.Graph(
            id='broadmanu',
            figure=broadmanu),
        ]
        ,className = 'twobytwoleft',
        style={
            'width': '35%', 
            'margin-left' : '15rem',
            'margin-right' : '7.5px',
            'margin-bottom' : '5px',
            'margin-top' : '5px',
            'display' : 'inline-block',
            }
        ),   

        html.Div([ #small block upper most

        dcc.Graph(
            id='selectedglobalmanu',
            figure=selectedglobalmanu),
        ]
        ,className = 'twobytworight',
        style={
            'width': '35%', 
            'display' : 'inline-block',
            'margin-left' : '7.5px',
            'margin-top' : '5px',
            'margin-bottom' : '5px',
            }
        ),

        html.Div([ #small block upper most

        dcc.Graph(
            id='broadtranspologistics',
            figure=broadtranspologistics),
        ]
        ,className = 'twobytwoleft',
        style={
            'width': '35%', 
            'margin-left' : '15rem',
            'margin-right' : '7.5px',
            'margin-bottom' : '5px',
            'margin-top' : '5px',
            'display' : 'inline-block',
            }
        ),   

        html.Div([ #small block upper most

        dcc.Graph(
            id='selectedglobaltranslogi',
            figure=selectedglobaltranslogi),
        ]
        ,className = 'twobytworight',
        style={
            'width': '35%', 
            'display' : 'inline-block',
            'margin-left' : '7.5px',
            'margin-top' : '5px',
            'margin-bottom' : '5px',
            }
        ),

        html.Div([ #small block upper most

        dcc.Graph(
            id='broadsemi',
            figure=broadsemi),
        ]
        ,className = 'twobytwoleft',
        style={
            'width': '35%', 
            'margin-left' : '15rem',
            'margin-right' : '7.5px',
            'margin-bottom' : '5px',
            'margin-top' : '5px',
            'display' : 'inline-block',
            }
        ),   

        html.Div([ #small block upper most

        dcc.Graph(
            id='selectedglobalsemi',
            figure=selectedglobalsemi),
        ]
        ,className = 'twobytworight',
        style={
            'width': '35%', 
            'display' : 'inline-block',
            'margin-left' : '7.5px',
            'margin-top' : '5px',
            'margin-bottom' : '5px',
            }
        ),

        html.Div([ #small block upper most

        dcc.Graph(
            id='broadcomms',
            figure=broadcomms),
        ]
        ,className = 'twobytwoleft',
        style={
            'width': '35%', 
            'margin-left' : '15rem',
            'margin-right' : '7.5px',
            'margin-bottom' : '5px',
            'margin-top' : '5px',
            'display' : 'inline-block',
            }
        ),   

        html.Div([ #small block upper most

        dcc.Graph(
            id='selectedglobalcomms',
            figure=selectedglobalcomms),
        ]
        ,className = 'twobytworight',
        style={
            'width': '35%', 
            'display' : 'inline-block',
            'margin-left' : '7.5px',
            'margin-top' : '5px',
            'margin-bottom' : '5px',
            }
        ),


    ]),

    html.Div(className = 'modernedge', children=[
        html.H2(children='Modern Edge'),

        html.Div([ #small block upper most

        dcc.Graph(
            id='broadhealthbiotech',
            figure=broadhealthbiotech
        ),

        ]
        ,className = 'twobytwoleft',
        style={
            'width': '35%', 
            'margin-left' : '15rem',
            'margin-right' : '7.5px',
            'margin-bottom' : '5px',
            'margin-top' : '5px',
            'display' : 'inline-block',
        }
        ),

        html.Div([ #small block upper most

        dcc.Graph(
            id='selectedglobalbiohealth',
            figure=selectedglobalbiohealth
        ),

        ]
        ,className = 'twobytworight',
        style={
            'width': '35%', 
            'display' : 'inline-block',
            'margin-left' : '7.5px',
            'margin-top' : '5px',
            'margin-bottom' : '5px',
            }
        ),

        html.Div([ #small block upper most

        dcc.Graph(
            id='broadentertainment',
            figure=broadentertainment
        ),

        ]
        ,className = 'twobytwoleft',
        style={
            'width': '35%', 
            'margin-left' : '15rem',
            'margin-right' : '7.5px',
            'margin-bottom' : '5px',
            'margin-top' : '5px',
            'display' : 'inline-block',
        }
        ),

        html.Div([ #small block upper most

        dcc.Graph(
            id='selectedglobalentertainment',
            figure=selectedglobalentertainment
        ),
        ]
        ,className = 'twobytworight',
        style={
            'width': '35%', 
            'display' : 'inline-block',
            'margin-left' : '7.5px',
            'margin-top' : '5px',
            'margin-bottom' : '5px',
            }
        ),
                
        html.Div([ #small block upper most

        dcc.Graph(
            id='broadconsumeredge',
            figure=broadconsumeredge),
        ]
        ,className = 'twobytwoleft',
        style={
            'width': '35%', 
            'margin-left' : '15rem',
            'margin-right' : '7.5px',
            'margin-bottom' : '5px',
            'margin-top' : '5px',
            'display' : 'inline-block',
        }
        ),

        html.Div([ #small block upper most

        dcc.Graph(
            id='selectedglobalconsumeredge',
            figure=selectedglobalconsumeredge),
        ]
        ,className = 'twobytworight',
        style={
            'width': '35%', 
            'display' : 'inline-block',
            'margin-left' : '7.5px',
            'margin-top' : '5px',
            'margin-bottom' : '5px',
            }
        ),

        html.Div([ #small block upper most

        dcc.Graph(
            id='gbtc',
            figure=gbtc),
        ]
        ,className = 'twobytwoleft',
        style={
            'width': '35%', 
            'margin-left' : '15rem',
            'margin-right' : '7.5px',
            'margin-bottom' : '5px',
            'margin-top' : '5px',
            'display' : 'inline-block',
        }
        ),

        html.Div([ #small block upper most

        dcc.Graph(
            id='ethe',
            figure=ethe),
        ]
        ,className = 'twobytworight',
        style={
            'width': '35%', 
            'display' : 'inline-block',
            'margin-left' : '7.5px',
            'margin-top' : '5px',
            'margin-bottom' : '5px',
            }
        ),

    ]),

],
# this styles the outermost Div:
)

if __name__ == '__main__':
    app.run_server(debug=True)
  

