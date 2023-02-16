import helper.loadData as ld
import helper.procesing as pr
import pandas as pd
from tqdm import tqdm
tqdm.pandas()

def rwCreation(rw,times):
    df = rw.merge(times,on = 'Country',how='inner')
    print('Creando columna SSC Date:')
    df['SSC Date'] = df.progress_apply(pr.NewDates,axis = 1)
    print('Creando columna MoH SSC:')
    df['MoH Date'] = df.progress_apply(pr.NewDates,axis = 1,using= 'MoH SSC')
    print('Creando columna MoH Month:')
    df['MoH Month'] = df.progress_apply(pr.defineDateParts,axis=1,part = 'month')
    print('Creando columna MoH Year:')
    df['MoH Year'] = df.progress_apply(pr.defineDateParts,axis=1,part = 'year')
    return df

def review(token):
    sp,cof = pr.PrepareData(token)
    pr.searchdiff(cof,sp)