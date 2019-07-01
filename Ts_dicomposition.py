import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
import matplotlib.gridspec as grid
from statsmodels.tsa.stattools import adfuller
from tabulate import tabulate

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




def stationary_test(Data):
    """
    we consider four different time windows including:
    1. hourly window=1
    2. daily window=1*24
    3. weekly window= 1*24*7
    4. monthly window= 1*24*7*4
    variable to work with DA_DEMAND, DEMAND, DA_LMP, RT_LMP
    :param Data:
    :return: plots and Dickey-Fuller test results for each zone
    """

    # we need 9 figures for 9 zones
    # figure_list=[None for i in range(1,len(Data)+1)]
    zone_names=['ISONE CA', 'Portland','Concord','Burlington','Bridgeport','Providence','SEMASS','Worcester','Boston']
    dicky_fuller_output=pd.ExcelWriter('Dicky Fuller results.xlsx', engine='xlsxwriter')
    for i,(key,val) in enumerate(Data.items()):
        figure_list = plt.figure(figsize=[18,10])
        figure_list.suptitle(zone_names[i])
        df = pd.DataFrame(index=Data[key].index)
        df['Day-Ahead_Demand']= Data[key].iloc[:,1]
        df['Real-time_Demand']= Data[key].iloc[:,2]
        df['Day-Ahead_Price'] = Data[key].iloc[:,3]
        df['Real-time_Price'] = Data[key].iloc[:,7]
        df_daily=df.resample('D').mean()
        df_weekly=df.resample('W').mean()
        df_monthly=df.resample('M').mean()
        df_list=[df,df_daily,df_weekly,df_monthly]



        mygrid=grid.GridSpec(4,4)
        mygrid.update(wspace=.3, hspace=.3)
        var_list=['Day-Ahead_Demand','Real-time_Demand','Day-Ahead_Price','Real-time_Price']
        time_slots=['Hourly','Daily','Weekly','Monthly']
        Analysis_type=['' for i in range(len(var_list)*len(time_slots))]
            # np.zeros(len(var_list)*len(time_slots))
        dicky_fuller_results =[pd.Series() for i in range(len(var_list)*len(time_slots))]
            # np.zeros(len(var_list) * len(time_slots))

        for k in range(len(var_list)):
            for j in range(len(time_slots)):
                plot_rolling(figure_list,df_list[j][var_list[k]],mygrid[k,j],var_list[k],time_slots[j])
                Analysis_type[k+j]= time_slots[j]+var_list[k]
                dicky_fuller_results[i+j]=Dickey_Fuller_Test(df_list[j][var_list[k]])

        figure_list.savefig(zone_names[i]+'.png')
        plt.close(figure_list)
        Data_to_write_excel = pd.concat(dicky_fuller_results[:],axis=1,sort=False)
        Data_to_write_excel.columns = Analysis_type
        Data_to_write_excel.to_excel(dicky_fuller_output,sheet_name=zone_names[i])
    dicky_fuller_output.save()


def plot_rolling(fig,dataframe,location,variable_name,time_slot):
    ax = fig.add_subplot(location)
    ax.set_title(variable_name,fontsize=8)
    ax.set_ylabel(time_slot + variable_name,fontsize=8)
    ax.plot(dataframe, label='Raw Data')
    ax.plot(dataframe.rolling(window=6).mean(), label='Rolling Mean')
    ax.plot(dataframe.rolling(window=6).std(), label='Rolling Standard Deviation')
    ax.legend(loc=1,fontsize=8)

def Dickey_Fuller_Test(TS):
    test = adfuller(TS, autolag='AIC')
    result = pd.Series(test[0:4], index=['Test Statistic', 'p-value', '#Lags Used', 'Number of Observations Used'])
    for key, value in test[4].items():
        result['Critical Value (%s)' % key] = value
    # result['Type of time series']= Ts_type
    return result



def transformation(Data,type):
    ''' transformations are
    log, moving average, first order diggerential, second order diffrential,log-moving average log, log-first order diff,
    weighted moving average, log moving average-weighted moving average, log weighted average-log differential
    :return all above mentioned as list
    '''
    Data_log = np.log(Data)






stationary_test(DataBase)






a=1


