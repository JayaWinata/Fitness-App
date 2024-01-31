import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.dates import AutoDateLocator, DateFormatter
from Database import db

column_name = ['weight','height','daily_calories','calories_limit']

def plot_data(column_name: str,limit: int):
    if column_name == 'daily_calories':
        plot_daily_calories(limit)
    else:
        data = db.get_history(column_name,limit)

        df_column_name = f'{column_name}'.replace('_',' ').title()
        data = pd.DataFrame(data,columns=['Date',df_column_name])
        data['Date'] = pd.to_datetime(data['Date'])
        data = data.set_index('Date').asfreq('D',method='ffill').sort_values(by='Date',ascending=False).iloc[:limit,:].sort_values(by='Date')

        sns.set_style("whitegrid")

        fig = plt.figure(facecolor='#0F0F0F', frameon=False, figsize=(12.5,2.5))

        sns.lineplot(x=data.index,y=data[df_column_name], color='#008170',errorbar=None, linewidth=3)
        plt.title(df_column_name,loc='left',color='white',fontsize=14,y=1.05)
        lower, upper = data[df_column_name].min() - data[df_column_name].mean(), data[df_column_name].max() + data[df_column_name].mean()
        lower = lower if lower > 0 else 0
        plt.ylim(lower,upper)
        ticks = [round(i) for i in np.linspace(lower,upper,5)]
        plt.yticks(ticks)


        ax = plt.gca()
        ax.patch.set_alpha(0) 
        ax.spines['bottom'].set_color('white')  
        ax.spines['left'].set_color('white')
        ax.fill_between(data.index,0,data[df_column_name],alpha=0.1,color='#008170')

        ax.tick_params(axis='x', colors='white')
        ax.tick_params(axis='y', colors='white') 

        locator = AutoDateLocator()
        ax.xaxis.set_major_locator(locator)
        formater = DateFormatter('%d/%m/%y')
        ax.xaxis.set_major_formatter(formater)

        ax.set_xlabel('', color='white')
        ax.set_ylabel('', color='white')

        sns.set_theme(palette='pastel',rc={'grid.alpha':0.09})
        sns.despine(right=True, top=True)

        plt.savefig(fname=f'../Assets/Image/{column_name}.png',bbox_inches='tight')
        plt.close()

def plot_daily_calories(limit: int):
    data = db.get_calories_history(limit)

    df_column_name = f'daily_calories'.replace('_',' ').title()
    data = pd.DataFrame(data,columns=['Date',df_column_name])
    data['Date'] = pd.to_datetime(data['Date'])
    data = data.set_index('Date').asfreq('D',method='ffill').sort_values(by='Date',ascending=False).iloc[:limit,:].sort_values(by='Date')

    sns.set_style("whitegrid")

    fig = plt.figure(facecolor='#0F0F0F', frameon=False, figsize=(12.5,2.5))

    sns.lineplot(x=data.index,y=data[df_column_name], color='#008170',errorbar=None, linewidth=3)
    plt.title(df_column_name,loc='left',color='white',fontsize=14,y=1.05)
    lower, upper = data[df_column_name].min() - data[df_column_name].mean(), data[df_column_name].max() + data[df_column_name].mean()
    lower = lower if lower > 0 else 0
    plt.ylim(lower,upper)
    ticks = [round(i) for i in np.linspace(lower,upper,5)]
    plt.yticks(ticks)

    ax = plt.gca()
    ax.patch.set_alpha(0) 
    ax.spines['bottom'].set_color('white')  
    ax.spines['left'].set_color('white')
    ax.fill_between(data.index,0,data[df_column_name],alpha=0.1,color='#008170')

    ax.tick_params(axis='x', colors='white')
    ax.tick_params(axis='y', colors='white') 

    locator = AutoDateLocator()
    ax.xaxis.set_major_locator(locator)
    formater = DateFormatter('%d/%m/%y')
    ax.xaxis.set_major_formatter(formater)

    ax.set_xlabel('', color='white')
    ax.set_ylabel('', color='white')

    sns.set_theme(palette='pastel',rc={'grid.alpha':0.09})
    sns.despine(right=True, top=True)

    plt.savefig(fname=f'../Assets/Image/daily_calories.png',bbox_inches='tight')
    plt.close()

def plot_all():
    for i in column_name:
        plot_data(i,10)


