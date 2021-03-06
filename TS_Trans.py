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

All_TSs=DataBase
All_zones=[]
for i, (key, val) in enumerate(DataBase.items()):
    # figure_list = plt.figure(figsize=[18, 10])
    # figure_list.suptitle(zone_names[i])
    df = pd.DataFrame(index=DataBase[key].index)
    df['Day-Ahead_Demand'] = DataBase[key].iloc[:, 1]
    df['Real-time_Demand'] = DataBase[key].iloc[:, 2]
    df['Day-Ahead_Price'] = DataBase[key].iloc[:, 3]
    df['Real-time_Price'] = DataBase[key].iloc[:, 7]
    df_daily = df.resample('D').mean()
    df_weekly = df.resample('W').mean()
    df_monthly = df.resample('M').mean()
    df_list = [df, df_daily, df_weekly, df_monthly]
    All_zones.append(df_list)

def transformation(DataFrame):
    """

    :param DataFrame:
    :return: Logarithmic transformation, Removing Moving Average, Removing exponential Moving Average, Removing Logarithmic MA,
    First Order Differential Transformation
    """
    listoftransformations=[]
    for i in DataFrame.columns:
        newdf=pd.DataFrame(index=DataFrame.index,columns=[i],data=DataFrame[i])
        newdf["Log_"+i]=np.log(newdf[i])
        newdf["Removed_MA_"+i]=newdf[i]-newdf[i].rolling(window=7,center=False).mean()
        newdf["Removed_Exp_WMA_"+i]=newdf[i]-newdf[i].ewm(halflife=7,ignore_na=False,min_periods=0).mean()
        newdf["First_Diff_"+i]=newdf[i].diff()
        newdf["Second_Diff_"+i]=newdf[i].diff(periods=2)
        newdf["Removed_Log_MA_"+i]=newdf["Log_"+i]-newdf["Log_"+i].rolling(window=7,center=False).mean()
        newdf["Removed_Exp_WMA_"+i]=newdf["Log_"+i]-newdf["Log_"+i].ewm(halflife=7,ignore_na=False,min_periods=0,adjust=True).mean()
        df=newdf.dropna()
        listoftransformations.append(df)
    return listoftransformations

# Define the an excel file for ADF tests
writer = pd.ExcelWriter('ADF_Results.xlsx', engine='xlsxwriter')

# feed the Daily Time Series to Transformation method and choosing only Real-time data
counter=0
zone_names=['ISONE CA', 'Portland','Concord','Burlington','Bridgeport','Providence','SEMASS','Worcester','Boston']
for zone_info in All_zones:
    Daily_Info=zone_info[1]
    DA_RT_Demand_Price_Trans=transformation(Daily_Info)
    Transformed_Daily_RT_prices=DA_RT_Demand_Price_Trans[-1]
    ADF_res=pd.DataFrame(columns=Transformed_Daily_RT_prices.columns)
    for trans in Transformed_Daily_RT_prices.columns:
        ADF_res[trans]=Stationarytest(Transformed_Daily_RT_prices[trans])

    ADF_res.to_excel(writer,zone_names[counter])
    counter+=1

writer.save()







a=1
