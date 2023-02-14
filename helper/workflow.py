import helper.loadData as ld
import helper.procesing as pr
import pandas as pd
from tqdm import tqdm
tqdm.pandas()
def prepareData(token):
    filters = ld.chargeFilters()
    df = ld.uploadData()
    print('Generando CFNs Tratados:')
    df['Treated CFN'] = df.progress_apply(pr.treadCFNs,axis = 1)
    df = df.dropna(subset=['CFN'])
    df = pr.sp_trim(df)
    sp = ld.load_SPlan(token)
    sp = pr.sp_trim(sp)
    return df,sp,filters

def PrepareNotfound(df,filters):
    filterCFNs = list(filters['Treated'].unique())
    notFound = []
    for cfn in filterCFNs:
        if cfn in df['Treated CFN']:
            print('estoy aqui perrini')
            continue
        else:
            notFound.append(cfn)
    return notFound

def defineCriticalCFN(row,filterList):
    a = row['Treated CFN']
    if a in filterList:
        return 'Critical CFN'
    else:
        return 'Not critical CFN'

def determinenotFound(df,FilterList):
    CnF = pd.DataFrame(columns = ['Treated CFN'])
    reference = list(df['Treated CFN'].unique())
    notFound = []
    for val in FilterList:
        if val in reference:
            pass
        else:
            notFound.append(val)
    
    CnF['Treated CFN'] = notFound
    return CnF

def searchOriginal(row,df2):
    a = row['Treated CFN']
    b = df2.loc[df2['Treated'] == a,'CFN'].unique()
    b= b[0]
    return b


def filteringData(token):
    df,sp,filters = prepareData(token)
    listOU  = [ou.strip() for ou in filters['SubOU'].unique()]
    df = df[df['OU'].isin(listOU)]
    print('Buscando información en el Submission Plan:')
    df['Regulatory info'] = df.progress_apply( pr.searchSP,axis = 1,sp = sp)
    print('La información ya ha sido asignado a los Produtos')
    aux = list(filters['Treated'].unique())
    filterList = [val.strip() for val in aux]
    print('Asignando Prioridad a los Productos:')
    df['Critical?'] = df.progress_apply(defineCriticalCFN,axis = 1,filterList = filterList)
    print('Prioridad satisfactoriamente asignada')
    CnF = determinenotFound(df,filterList)
    df2 = filters.drop('SubOU',axis = 1)
    print('Generando CFNs no encontrados:')
    CnF['Original CFN'] = CnF.progress_apply(searchOriginal,axis=1,df2=df2)
    inCountry = pr. createInCountry(df)
    portfolio = pr.Createportfoliostatus(df,filters)
    pr.create_excel(df,CnF,inCountry,portfolio)