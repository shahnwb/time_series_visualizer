import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()


# Import data (Make sure to parse dates. Consider setting index column to 'date'.)
df = pd.read_csv('fcc-forum-pageviews.csv')
df.date = pd.to_datetime(df.date)
# Clean data
df.drop(df.loc[(df['value'] > df['value'].quantile(0.975))].index, inplace=True)
df.drop(df.loc[(df['value'] < df['value'].quantile(0.025))].index, inplace=True)



def draw_line_plot():
    # Draw line plot
    fig, ax = plt.subplots(1,1)
    plt.plot(df.date, df.value)
    plt.xlim('2016-05','2019-12')
    plt.xlabel('Date')
    plt.ylabel('Page Views')
    plt.title('Daily freeCodeCamp Forum Page Views')
    plt.tight_layout()

    # Save image and return fig (don't change this part)
    fig.savefig('line_plot.png')
    return fig

def draw_bar_plot():
    # Copy and modify data for monthly bar plot
    df_bar = df.groupby(pd.PeriodIndex(df['date'], freq='M'))['value'].mean().reset_index()    

    # Draw bar plot
    fig, ax = plt.subplots(1,1)
    g = sns.catplot(data=df_bar, kind='bar', x=df_bar.date.dt.year, y=df_bar['value'], hue=df_bar.date.dt.month, legend='full')
    g._legend.set_title('Months')
    g.set_axis_labels('Years','Average Page Views')

    # Save image and return fig (don't change this part)
    fig.savefig('bar_plot.png')
    return fig

def draw_box_plot():
    # Prepare data for box plots (this part is done!)
    df_box = df.copy()
    df_box.reset_index(inplace=True)
    df_box['year'] = [d.year for d in df_box.date]
    df_box['month'] = [d.strftime('%b') for d in df_box.date]

    # Draw box plots (using Seaborn)
    fig, ax = plt.subplots(1,2)
    fig.set_size_inches(20,6)
    order = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
    g = sns.boxplot(data=df_box, x='year', y='value', ax=ax[0])
    g.set_title('Year-wise Box Plot (Trend)')
    g.set_ylabel('Page Views')
    f = sns.boxplot(data=df_box, x='month', y='value', ax=ax[1], order=order)
    f.set_title('Month-wise Box Plot (Seasonality)')
    f.set_ylabel('Page Views')


    # Save image and return fig (don't change this part)
    fig.savefig('box_plot.png')
    return fig
