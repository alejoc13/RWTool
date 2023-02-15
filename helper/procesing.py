import pandas as pd
import numpy as np
import datetime
import re
import os
from tqdm import tqdm


def cut_values(row,column = 'MANUFACTURING ADDRESS',sep = '\n' ):
    var = str(row[column])
    if sep in var:
        var = var.split(sep)
        var1 = [name.strip() for name in var]
        return var1
    else:
        return var

def trim_column(row,column = 'REGISTRATION NUMBER'):
    a = str(row[column])
    a = a.strip()
    return a

def paste_problem(row,name ='CUT ADDRESS',address =  'CUT ADDRESS'):
    a = row[name]
    b = row[address]
    if type(a) is list:
        junto = ''
        for nombre,dir in zip(a,b):
            junto += nombre + ' ' + dir + '\n'
        return junto
    else:
        junto = a + ' ' + b + '\n'
        return junto

def concatMfg(row,colum1 = 'Manufacturing site 1',colum2 = 'Manufacturing site 2'):
    mfg1 = str(row[colum1])
    mfg2 = str(row[colum2])
    mfg = mfg1 + '\n' + mfg2
    return mfg


def reference(row,col='Expected Approval Date'):
    a = row[col]
    delta = datetime.timedelta(90)
    ref = a + delta
    return ref


def sp_trim(df):
    print('Pre proesando los datos:')
    for name in tqdm(df.columns):
        if name not in ['Expected Submission Date','Submission Date','Approval Date','Expected Approval Date','Created','PC3 Due Date','DM Complete date','PC3 Complete Date','License Expiration Date','EXPIRATION DATE']:
            df[name] = df.apply(trim_column,axis = 1,column = name)
    print('Los datos fueron correctamente trimeados')
    return df

def chageSeparator(row,col = 'Submission Type'):
    a = str(row[col])
    a = a.replace("\n", "/")
    return a

def newCol(df):
    df2 = pd.DataFrame(columns=df.columns)
    for i in range(len(df)):
        if type(df['ST cut'][i]) is list:
            temporal = pd.DataFrame(columns=df.columns)
            a = [val for val in df['ST cut'][i]]
            for j in range(len(a)):
                for name in df.columns:
                    temporal[name] = [df[name][i]]
                temporal['Submission Type']= [a[j]]
                df2 = pd.concat([df2,temporal],ignore_index = True)
        else:
            temporal = pd.DataFrame(columns=df.columns)
            for name in df.columns:
                temporal[name] = [df[name][i]]
        
            temporal['Submission Type'] =df['Submission Type'][i]
            df2 = pd.concat([df2,temporal],ignore_index = True)
    df2 = df2.drop('ST cut',axis=1)
    df2 = df2[df2['Submission Type'].isin(['CFN Withdrawal','Renewal'])]
    return df2

def expandRows(df):
    df['Submission Type'] = df.apply(chageSeparator,axis=1,col = 'Submission Type')
    df['ST cut'] = df.apply(cut_values,axis =1,column='Submission Type',sep='/')
    new_criticals = newCol(df)
    return new_criticals


def sufix_search(df,ref):
     temp = df[df['CFN'].str.startswith(ref)]
     return temp

def treadCFNs(row):
    cfn = str(row['CFN'])
    pattern = r'[^A-Za-z0-9]+'
    aux = re.sub(pattern, '', str(cfn))
    return aux

def searchSP(row,sp):
    rs = str(row['REGISTRATION NUMBER'])
    rs = rs.strip()
    temp = sp[sp['REGISTRATION NUMBER'] == rs]
    text = ''
    for id,Status,type in zip(temp['Id'],temp['Status'],temp['Submission Type']):
        text += f'ID:{id}, type(s):{type} ,Status Regulatorio:{Status}\n'
    if text == '':
        text+='No info on Submission plan'
    return text

def SumCountries(row):
    ref = ['CFN']
    count = 0
    for col in row.index:
        if col in ref:
            count+=0
        else:
            if row[col] !=0:
                count+=1
    return count


def ChangeValues(df):
    ref = ['CFN','# of Countries']
    for col in df.columns:
        if col not in ref:
            df[col] = df[col].replace([1],'Si')
            df[col] = df[col].replace([0],' No')
    return df

def createInCountry(df):
    print('Generando Hoja in country')
    df1 = df[df['Critical?']=='Critical CFN']
    df1['count'] = 1
    pivoted = pd.pivot_table(data=df1,index=['CFN'],columns=['Country'],values = 'count',fill_value=0,
                            margins=False)
    pivoted['# of Countries'] = pivoted.apply(SumCountries,axis=1)
    pivoted = ChangeValues(pivoted)
    return pivoted

def Createportfoliostatus(df,filters):
    cantidad = len(filters['CFN'])
    df1 = df[df['Critical?']=='Critical CFN']
    countries = list(df['Country'].unique())
    df2 = pd.DataFrame(columns=['Pais','Cantidad Presente','Cantidad ausente','Total','Porcentaje Presente'])
    print('Generando Hoja Portaflio')
    for country in tqdm(countries):
        aux = pd.DataFrame(columns=['Pais','Cantidad Presente','Cantidad ausente','Total','Porcentaje Presente'])
        Temp = df1[df1['Country'] == country]
        aux['Pais'] = [country]
        aux['Cantidad Presente'] = [len(Temp)]
        aux['Total'] = [cantidad]
        aux['Cantidad ausente'] = [cantidad-len(Temp)]
        df2 = pd.concat([df2,aux])
    df2['Porcentaje Presente'] =  (df2['Cantidad Presente']/df2['Total'])*100
    return df2


def create_excel(df):
    print('Generando Reporte')
    user = os.path.expanduser('~').split('\\')[2]
    date = datetime.datetime.now()
    date = date.strftime(('%Y-%m-%d_%H-%M-%S'))
    path = f'Results\{user} {date} RW dates calculation.xlsx'
    df.to_excel(path,index=False)

    print('Proceso Exitosamente finalizado')


def NewDates(row,date = 'License Expiration Date',using = 'VoC SSC'):
    try: 
        new_date = row[date] - datetime.timedelta(days=row[using])
        return new_date
    except:
        return 'Manual Review'

def defineDateParts(row,part = 'month'):
    if part == 'month':
        try:
            a  = row['MoH Date']
            mes = a.month
            return mes
        except:
            return 'No Date'
    if part == 'year':
        try:
            a  = row['MoH Date']
            año = a.year
            return año
        except:
            return 'No date'
        