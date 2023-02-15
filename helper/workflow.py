import helper.loadData as ld
import helper.procesing as pr
import pandas as pd
from tqdm import tqdm
tqdm.pandas()

def rwCreation(rw,times):
    df = rw.merge(times,on = 'Country',how='inner')
    return df