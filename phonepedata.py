#Import important libraries
import json
import os
import pandas as pd
from utils import copytomysql

# Create the Empty dictionary against each dataframe
agg_user = {'reg_users':[],'app_opens':[],'brand':[],'count':[],'percentage':[],'agg_year':[],'quarter':[],'state':[] }
agg_transaction = {'name':[],'amount':[],'count':[],'agg_year':[],'quarter':[],'state':[] }
agg_insurance = {'name':[],'amount':[],'count':[],'agg_year':[],'quarter':[],'state':[] }

map_user = {'reg_users':[],'app_opens':[],'agg_year':[],'quarter':[],'state':[],'district':[] }
map_transaction = {'name':[],'amount':[],'count':[],'agg_year':[],'quarter':[],'state':[] ,'district':[]}
map_insurance = {'name':[],'amount':[],'count':[],'agg_year':[],'quarter':[],'state':[] ,'district':[]}

top_user = {'reg_users':[],'agg_year':[],'quarter':[],'state':[],'district':[],'pincode':[] }
top_transaction = {'entity_name':[],'amount':[],'count':[],'agg_year':[],'quarter':[],'state':[],'district':[],'pincode':[] }
top_insurance = {'entity_name':[],'amount':[],'count':[],'agg_year':[],'quarter':[],'state':[],'district':[] ,'pincode':[]}

# Get the Json file path
def getjsonpath(filepath):
    getlistval = os.listdir(filepath)
    for i in getlistval:
        #Gather the state information separately
        if i == 'state':
            agg_state = os.listdir(filepath + i + '/')
            for j in agg_state:
                agg_yr = os.listdir(filepath + i + '/' + j)
                for k in agg_yr:
                    agg_path = os.listdir(filepath + i + '/' + j + '/' + k + '/')
                    for l in agg_path:
                        readjson((filepath + i + '/' + j + '/' + k + '/' + l),k,j)
        # All india data
        else:
            p_i = filepath+i+'/'
            agg_path = os.listdir(p_i)
            for j in agg_path:
                readjson((p_i+j),i,'')

# Json Read functionality
def readjson(filepath,year,state):
    txtval = filepath.split("/")
    valtype = txtval[3]
    subvaltype= txtval[4]
    quarter = txtval[-1].strip('.json')
    with open(filepath, 'r') as f:
        D = json.load(f)
    createdf(D,valtype,subvaltype,year,state,quarter)

# Data moved from JSON to Dataframe
def createdf(jsondata, valtype, subvaluetype, year, state, quarter):
    if (valtype=='aggregated') & (subvaluetype=='user'):
        reguser = jsondata['data']['aggregated']['registeredUsers']
        appopens = jsondata['data']['aggregated']['appOpens']
        data_list = (jsondata.get('data') or {}).get('usersByDevice') or []
        for jdata in data_list:
            if jdata:
                brand = jdata['brand']
                count = jdata['count']
                percentage = jdata['percentage']
                agg_user['reg_users'].append(reguser)
                agg_user['app_opens'].append(appopens)
                agg_user['brand'].append(brand)
                agg_user['count'].append(count)
                agg_user['percentage'].append(percentage)
                agg_user['agg_year'].append(year)
                agg_user['quarter'].append(quarter)
                agg_user['state'].append(state)
    if (valtype == 'aggregated') & (subvaluetype == 'transaction'):
        data_list = (jsondata.get('data') or {}).get('transactionData') or []
        for jdata in data_list:
            if jdata:
                name = jdata['name']
                count = jdata['paymentInstruments'][0]['count']
                amount = jdata['paymentInstruments'][0]['amount']
                agg_transaction['name'].append(name)
                agg_transaction['count'].append(count)
                agg_transaction['amount'].append(amount)
                agg_transaction['agg_year'].append(year)
                agg_transaction['quarter'].append(quarter)
                agg_transaction['state'].append(state)
    if (valtype == 'aggregated') & (subvaluetype == 'insurance'):
        data_list = (jsondata.get('data') or {}).get('transactionData') or []
        for jdata in data_list:
            if jdata:
                name = jdata['name']
                count = jdata['paymentInstruments'][0]['count']
                amount = jdata['paymentInstruments'][0]['amount']
                agg_insurance['name'].append(name)
                agg_insurance['count'].append(count)
                agg_insurance['amount'].append(amount)
                agg_insurance['agg_year'].append(year)
                agg_insurance['quarter'].append(quarter)
                agg_insurance['state'].append(state)
    if (valtype == 'map') & (subvaluetype == 'user'):
        data_list = (jsondata.get('data') or {}).get('hoverData') or {}
        for jdata in data_list:
            if jdata:
                if state=='':
                    regusers = data_list[jdata]['registeredUsers']
                    appopens = data_list[jdata]['appOpens']
                    map_user['reg_users'].append(regusers)
                    map_user['agg_year'].append(year)
                    map_user['quarter'].append(quarter)
                    map_user['state'].append(jdata)
                    map_user['district'].append('')
                    map_user['app_opens'].append(appopens)
                else:
                    regusers = data_list[jdata]['registeredUsers']
                    appopens = data_list[jdata]['appOpens']
                    map_user['reg_users'].append(regusers)
                    map_user['agg_year'].append(year)
                    map_user['quarter'].append(quarter)
                    map_user['state'].append(state)
                    map_user['district'].append(jdata)
                    map_user['app_opens'].append(appopens)
    if (valtype == 'map') & (subvaluetype == 'transaction'):
        data_list = (jsondata.get('data') or {}).get('hoverDataList') or []
        for jdata in data_list:
            if jdata:
                if state=='':
                    name = jdata['name']
                    count = jdata['metric'][0]['count']
                    amount = jdata['metric'][0]['amount']
                    map_transaction['name'].append(name)
                    map_transaction['count'].append(count)
                    map_transaction['amount'].append(amount)
                    map_transaction['agg_year'].append(year)
                    map_transaction['quarter'].append(quarter)
                    map_transaction['state'].append(name)
                    map_transaction['district'].append('')
                else:
                    name = jdata['name']
                    count = jdata['metric'][0]['count']
                    amount = jdata['metric'][0]['amount']
                    map_transaction['name'].append(name)
                    map_transaction['count'].append(count)
                    map_transaction['amount'].append(amount)
                    map_transaction['agg_year'].append(year)
                    map_transaction['quarter'].append(quarter)
                    map_transaction['state'].append(state)
                    map_transaction['district'].append(name)
    if (valtype == 'map') & (subvaluetype == 'insurance'):
        data_list = (jsondata.get('data') or {}).get('hoverDataList') or []
        for jdata in data_list:
            if jdata:
                if state=='':
                    name = jdata['name']
                    count = jdata['metric'][0]['count']
                    amount = jdata['metric'][0]['amount']
                    map_insurance['name'].append(name)
                    map_insurance['count'].append(count)
                    map_insurance['amount'].append(amount)
                    map_insurance['agg_year'].append(year)
                    map_insurance['quarter'].append(quarter)
                    map_insurance['state'].append(name)
                    map_insurance['district'].append('')
                else:
                    name = jdata['name']
                    count = jdata['metric'][0]['count']
                    amount = jdata['metric'][0]['amount']
                    map_insurance['name'].append(name)
                    map_insurance['count'].append(count)
                    map_insurance['amount'].append(amount)
                    map_insurance['agg_year'].append(year)
                    map_insurance['quarter'].append(quarter)
                    map_insurance['state'].append(state)
                    map_insurance['district'].append(name)
    if (valtype == 'top') & (subvaluetype == 'user'):
        if state=='':
            data_list = (jsondata.get('data') or {}).get('states') or []
        else:
            data_list = (jsondata.get('data') or {}).get('districts') or []
            data_listpin = (jsondata.get('data') or {}).get('pincodes') or []
        for jdata in data_list:
            if jdata:
                if state=='':
                    name = jdata['name']
                    reguser = jdata['registeredUsers']
                    top_user['reg_users'].append(reguser)
                    top_user['agg_year'].append(year)
                    top_user['quarter'].append(quarter)
                    top_user['state'].append(name)
                    top_user['district'].append('')
                    top_user['pincode'].append(None)
                else:
                    name = jdata['name']
                    reguser = jdata['registeredUsers']
                    top_user['reg_users'].append(reguser)
                    top_user['agg_year'].append(year)
                    top_user['quarter'].append(quarter)
                    top_user['state'].append(state)
                    top_user['district'].append(name)
                    top_user['pincode'].append(None)
        if state != '':
            for jdata1 in data_listpin:
                name = jdata1['name']
                reguser = jdata1['registeredUsers']
                top_user['reg_users'].append(reguser)
                top_user['agg_year'].append(year)
                top_user['quarter'].append(quarter)
                top_user['state'].append(state)
                top_user['district'].append('')
                top_user['pincode'].append(name)
    if (valtype == 'top') & (subvaluetype == 'transaction'):
        if state=='':
            data_list = (jsondata.get('data') or {}).get('states') or []
        else:
            data_list = (jsondata.get('data') or {}).get('districts') or []
            data_listpin = (jsondata.get('data') or {}).get('pincodes') or []
        for jdata in data_list:
            if jdata:
                if state=='':
                    name = jdata['entityName']
                    count = jdata['metric']['count']
                    amount = jdata['metric']['amount']
                    top_transaction['entity_name'].append(name)
                    top_transaction['count'].append(count)
                    top_transaction['amount'].append(amount)
                    top_transaction['agg_year'].append(year)
                    top_transaction['quarter'].append(quarter)
                    top_transaction['state'].append(name)
                    top_transaction['district'].append('')
                    top_transaction['pincode'].append(None)
                else:
                    name = jdata['entityName']
                    count = jdata['metric']['count']
                    amount = jdata['metric']['amount']
                    top_transaction['entity_name'].append(name)
                    top_transaction['count'].append(count)
                    top_transaction['amount'].append(amount)
                    top_transaction['agg_year'].append(year)
                    top_transaction['quarter'].append(quarter)
                    top_transaction['state'].append(state)
                    top_transaction['district'].append(name)
                    top_transaction['pincode'].append(None)
        if state != '':
            for jdata in data_listpin:
                name = jdata['entityName']
                count = jdata['metric']['count']
                amount = jdata['metric']['amount']
                top_transaction['entity_name'].append(name)
                top_transaction['count'].append(count)
                top_transaction['amount'].append(amount)
                top_transaction['agg_year'].append(year)
                top_transaction['quarter'].append(quarter)
                top_transaction['state'].append(state)
                top_transaction['district'].append('')
                top_transaction['pincode'].append(name)
    if (valtype == 'top') & (subvaluetype == 'insurance'):
        if state=='':
            data_list = (jsondata.get('data') or {}).get('states') or []
        else:
            data_list = (jsondata.get('data') or {}).get('districts') or []
            data_listpin = (jsondata.get('data') or {}).get('pincodes') or []
        for jdata in data_list:
            if jdata:
                if state=='':
                    name = jdata['entityName']
                    count = jdata['metric']['count']
                    amount = jdata['metric']['amount']
                    top_insurance['entity_name'].append(name)
                    top_insurance['count'].append(count)
                    top_insurance['amount'].append(amount)
                    top_insurance['agg_year'].append(year)
                    top_insurance['quarter'].append(quarter)
                    top_insurance['state'].append(name)
                    top_insurance['district'].append('')
                    top_insurance['pincode'].append(None)
                else:
                    name = jdata['entityName']
                    count = jdata['metric']['count']
                    amount = jdata['metric']['amount']
                    top_insurance['entity_name'].append(name)
                    top_insurance['count'].append(count)
                    top_insurance['amount'].append(amount)
                    top_insurance['agg_year'].append(year)
                    top_insurance['quarter'].append(quarter)
                    top_insurance['state'].append(state)
                    top_insurance['district'].append(name)
                    top_insurance['pincode'].append(None)
        if state != '':
            for jdata in data_listpin:
                name = jdata['entityName']
                count = jdata['metric']['count']
                amount = jdata['metric']['amount']
                top_insurance['entity_name'].append(name)
                top_insurance['count'].append(count)
                top_insurance['amount'].append(amount)
                top_insurance['agg_year'].append(year)
                top_insurance['quarter'].append(quarter)
                top_insurance['state'].append(state)
                top_insurance['district'].append('')
                top_insurance['pincode'].append(name)

# Push the data from dataframe to SQL tables
def sqlinsert(filepath):
    txtval = filepath.split("/")
    valtype = txtval[3]
    subvaltype = txtval[4]
    if (valtype=='aggregated') & (subvaltype=='user'):
        aggregated_user = pd.DataFrame(agg_user)
        copytomysql(aggregated_user,'aggregated_user')
    if (valtype == 'aggregated') & (subvaltype == 'transaction'):
        aggregated_trans = pd.DataFrame(agg_transaction)
        copytomysql(aggregated_trans, 'aggregated_transaction')
    if (valtype == 'aggregated') & (subvaltype == 'insurance'):
        aggregated_insurance = pd.DataFrame(agg_insurance)
        copytomysql(aggregated_insurance, 'aggregated_insurance')
    if (valtype == 'map') & (subvaltype == 'user'):
        mapusers = pd.DataFrame(map_user)
        copytomysql(mapusers, 'map_user')
    if (valtype == 'map') & (subvaltype == 'transaction'):
        maptransaction = pd.DataFrame(map_transaction)
        copytomysql(maptransaction, 'map_map')
    if (valtype == 'map') & (subvaltype == 'insurance'):
        mapinsurance = pd.DataFrame(map_insurance)
        copytomysql(mapinsurance, 'map_insurance')
    if (valtype == 'top') & (subvaltype == 'user'):
        topuser = pd.DataFrame(top_user)
        copytomysql(topuser, 'top_user')
    if (valtype == 'top') & (subvaltype == 'transaction'):
        toptransaction = pd.DataFrame(top_transaction)
        copytomysql(toptransaction, 'top_map')
    if (valtype == 'top') & (subvaltype == 'insurance'):
        topinsurance = pd.DataFrame(top_insurance)
        copytomysql(topinsurance, 'top_insurance')
