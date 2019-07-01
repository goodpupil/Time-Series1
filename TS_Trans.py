import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
import matplotlib.gridspec as grid
from statsmodels.tsa.stattools import adfuller



def get_excel_content(NameofFolder):
    os.chdir(os.getcwd()+'\\'+NameofFolder)
    excel_list = [i for i in os.listdir(os.getcwd()) if i.endswith('.xls')]
    return excel_list

def process_excel_sheets(Nameofexcel):
    excel_file=pd.ExcelFile(Nameofexcel)
    sheet_dict={}
    for i,sheet in enumerate(excel_file.sheet_names):
        if i!=0:
            df=excel_file.parse(sheet,header=0,index_col='Date')
            df.index=pd.to_datetime(df.index)+ pd.to_timedelta(df.Hour, unit='h')
            sheet_dict[i]=df
    return sheet_dict

def gather_info(ExcelList,Nofsheerts):
    info=dict.fromkeys(np.arange(1,Nofsheerts+1),[])
    for excel in ExcelList:
        print(excel)
        tmp=process_excel_sheets(excel)
        for key, val in tmp.items():
            info[key].append(val)
    return info


All_excels= get_excel_content('DATA2')
# Initialize the Data dictionary
#tmp=gather_info(All_excels,9)

All_Data={}
for i in range(1,10):
    All_Data[i]=[]

for i in All_excels:
    print(i)
    tmp_dict= process_excel_sheets(i)
    for key,val in tmp_dict.items():
        All_Data[key].append(val)



DataBase=dict.fromkeys(np.arange(1,10),None)
for key,_ in DataBase.items():
    DataBase[key]=pd.concat(All_Data[key][:])


def Stationarytest(TS):
    test = adfuller(TS, autolag='AIC')
    result = pd.Series(test[0:4], index=['Test Statistic', 'p-value', '#Lags Used', 'Number of Observations Used'])
    for key, value in test[4].items():
        result['Critical Value (%s)' % key] = value
    return result
