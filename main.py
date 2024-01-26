import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

df_tesla = pd.read_csv('TESLA Search Trend vs Price.csv')

df_btc_search = pd.read_csv('Bitcoin Search Trend.csv')
df_btc_price = pd.read_csv('Daily Bitcoin Price.csv')

df_unemployment = pd.read_csv('UE Benefits Search vs UE Rate 2004-19.csv')

# remove any missing values
dfs = [df_tesla, df_btc_search, df_btc_price, df_unemployment]
for i in range(len(dfs)):
    if dfs[i].isna().values.any():
        dfs[i].dropna(inplace=True)


# covnvert string dates to datetime objects
df_tesla.MONTH = pd.to_datetime(df_tesla.MONTH)
df_btc_search.MONTH = pd.to_datetime(df_btc_search.MONTH)
df_unemployment.MONTH = pd.to_datetime(df_unemployment.MONTH)
df_btc_price.DATE = pd.to_datetime(df_btc_price.DATE)

# this is daily data, change it to monthly to make it easier to compare
df_btc_price = df_btc_price.resample('M', on='DATE').last()

def graph_two_axes(size, titleInfo, xticksRotation, labels, colors, axes, saveFile):
    """
    Generate graph with two axes.

    Input: 
        size - INTEGER, size of the graph
        titleInfo - TUPLE, (Title, Font Size)
        xticksRotation - INTEGER, rotation on x-axis labels and ticks
        labels - TUPLE, ((x-axis label, color, fontsize), (y-axis label, color, fontsize))
        colors - TUPLE, (color of left axis line, color of right axis line)
        axes - TUPLE, (dataframe of common axis, dataframe of left axis, dataframe of right axis)
        saveFile - STRING, name of file to save graph in
    """
    years = mdates.YearLocator()
    months = mdates.MonthLocator()
    years_fmt = mdates.DateFormatter('%Y')

    plt.figure(figsize=size)

    plt.xticks(rotation=xticksRotation)
    plt.title(titleInfo[0], fontsize=titleInfo[1])


    ax1 = plt.gca()

    ax2 = ax1.twinx()

    ax1.xaxis.set_major_locator(years)
    ax1.xaxis.set_major_formatter(years_fmt)
    ax1.xaxis.set_minor_locator(months)

    ax1.set_ylabel(labels[0][0], color=labels[0][1], fontsize=labels[0][2])
    ax2.set_ylabel(labels[1][0], color=labels[1][1], fontsize=labels[1][2])
    
    ax1.plot(axes[0], axes[1], color=colors[0])
    ax2.plot(axes[0], axes[2], color=colors[1])
    plt.savefig(saveFile)


title = ("Tesla Web Search vs Price", 22)
axis1Title = ('TSLA Stock Price', '#FF5733', 14)
axis2Title = ('Search Trend', 'royalblue', 14)
tsla_axes_dfs = (df_tesla.MONTH, df_tesla.TSLA_USD_CLOSE, df_tesla.TSLA_WEB_SEARCH)
graph_two_axes((14, 8), title, 45, (axis1Title, axis2Title), ("#FF5733", "royalblue"), tsla_axes_dfs, "tesla.png")


bitcoin_title = ("Bitcoin News Search vs Resampled Price", 22)
bitcoin_axis1_title = ('BTC Price', 'red', 14)
bitcoin_axis2_title = ('Search Trend', 'royalblue', 14)
bitcoin_axes_dfs = (df_btc_search.MONTH, df_btc_price.CLOSE, df_btc_search.BTC_NEWS_SEARCH)
graph_two_axes((14, 8), bitcoin_title, 45, (bitcoin_axis1_title, bitcoin_axis2_title), ("#FF5733", "royalblue"), bitcoin_axes_dfs, "bitcoin.png")


