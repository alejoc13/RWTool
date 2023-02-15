import helper.loadData as ld
import helper.procesing as pr
import pandas as pd
from tqdm import tqdm
tqdm.pandas()

def rwCreation(rw,times):
    df = rw.merge(times,on = 'Country',how='inner')
    df['SSC Date'] = df.apply(pr.NewDates,axis = 1)
    df['MoH Date'] = df.apply(pr.NewDates,axis = 1,using= 'MoH SSC')
    return df