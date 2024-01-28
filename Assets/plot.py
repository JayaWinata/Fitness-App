from Database import db
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.dates import AutoDateLocator, DateFormatter

def plot_data(column_name: str,limit: int):
    data = db.get_history(column_name,limit)

    df_column_name = f'{column_name}'.capitalize()
    data = pd.DataFrame(data,columns=['Date',df_column_name])
    data['Date'] = pd.to_datetime(data['Date'])
    data = data.set_index('Date').asfreq('D',method='ffill').sort_values(by='Date',ascending=False).iloc[:limit,:].sort_values(by='Date')

    sns.set_style("whitegrid")

    fig = plt.figure(facecolor='#0F0F0F', frameon=False, figsize=(12.5,2.5))

    sns.lineplot(x=data.index,y=data[df_column_name], color='#008170',errorbar=None, linewidth=2) 

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
    ax.set_ylabel(df_column_name, color='white')

    sns.set_theme(palette='pastel',rc={'grid.alpha':0.09})
    sns.despine(right=True, top=True)

    plt.savefig(fname=f'../Assets/Image/{column_name}.png')

