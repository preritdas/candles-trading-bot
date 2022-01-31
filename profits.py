import pandas as pd
from datetime import datetime as dt
import matplotlib.pyplot as plt
from config import *
import os
import yfinance as yf
import pysftp

def updateCSVNoSPY():
    accountChange = (float(api.get_account().equity) - float(api.get_account().last_equity))/float(api.get_account().last_equity)
    accountChange = round(accountChange, 4)

    try:
        profits = pd.read_csv("Data/Profit Tracker.csv", index_col = 0)
    except FileNotFoundError: #if there's no profits file yet
        profits = pd.DataFrame(
            {
                "Day": [],
                "Profit": []
            }
        )

    dayList = list(profits["Day"])
    profitList = list(profits["Profit"])

    dayList.append(str(dt.now()))
    profitList.append(accountChange)

    newCSV = pd.DataFrame(
        {
            "Day": dayList,
            "Profit": profitList
        }
    )

    try:
        newCSV.to_csv("Data/Profit Tracker.csv")
    except FileNotFoundError: # If the directory doesn't exist
        os.mkdir('Data') # then make the directory
        newCSV.to_csv("Data/Profit Tracker.csv")
    except:
        print("Error with updating CSV.")

def updateCSV():
    accountChange = (float(api.get_account().equity) - float(api.get_account().last_equity))/float(api.get_account().last_equity)
    accountChange = round(accountChange, 4)

    # Get SPY Change for benchmarking and alpha
    spy = yf.Ticker("SPY").history()

    today = dt.today().strftime("%Y-%m-%d")

    spy = yf.Ticker("SPY").history()
    spy = spy.reset_index()

    today = dt.today().strftime("%Y-%m-%d")

    idx = spy.index[spy["Date"] == today].tolist()
    for x in idx:
        todayIDX = int(x)
        yesterdayIDX = todayIDX - 1
    
    spyTodayClose = spy["Close"][todayIDX]
    spyYesterdayClose = spy["Close"][yesterdayIDX]
    spyChange = (spyTodayClose - spyYesterdayClose)/spyYesterdayClose
    spyChange = round(spyChange, 4)

    try:
        profits = pd.read_csv("Data/Profit Tracker.csv", index_col = 0)
    except: #if there's no profits file yet
        profits = pd.DataFrame(
            {
                "Day": [],
                "Profit": [],
                "SPY Change": [],
                "Alpha": []
            }
        )

    dayList = list(profits["Day"])
    profitList = list(profits["Profit"])
    spyChangeList = list(profits["SPY Change"])
    alphaList = list(profits["Alpha"])

    dayList.append(str(dt.now()))
    profitList.append(accountChange)
    spyChangeList.append(spyChange)
    alphaList.append(round((accountChange - spyChange), 4))

    newCSV = pd.DataFrame(
        {
            "Day": dayList,
            "Profit": profitList,
            "SPY Change": spyChangeList,
            "Alpha": alphaList
        }
    )

    # # Cumulative Profit List
    # cumulativeProfitList = []
    # i = 0
    # for i in range(len(profitList)):
    #     j = 0
    #     currentCumulativeProfit = 0
    #     for j in range(i):
    #         currentCumulativeProfit = currentCumulativeProfit + profitList[j]
    #     cumulativeProfitList.append(currentCumulativeProfit)

    # # Cumulative Alpha List
    # cumulativeAlphaList = []
    # i = 0
    # for i in range(len(alphaList)):
    #     j = 0
    #     currentCumulativeAlpha = 0
    #     for j in range(i):
    #         currentCumulativeAlpha = currentCumulativeAlpha + alphaList[j]
    #     cumulativeAlphaList.append(currentCumulativeAlpha)

    # # Plot returns and alpha
    # plt.plot(cumulativeProfitList, label = "Profits")
    # plt.plot(cumulativeAlphaList, label = "Alpha")
    # plt.ylabel("Percentage (%)")
    # plt.xlabel("Days Run")
    # plt.title("Profits and Alpha")
    # plt.legend()
    # plt.savefig('Data/profits.png')

    try:
        newCSV.to_csv("Data/Profit Tracker.csv")
    except FileNotFoundError: # If the directory doesn't exist
        os.mkdir('Data') # then make the directory
        newCSV.to_csv("Data/Profit Tracker.csv")
    except:
        print("Error with updating CSV.")

def relativeNotionalGraph():
    profitsDF = pd.read_csv('Data/Profit Tracker.csv', index_col = 0)
    returnsList = list(profitsDF["Profit"])
    spyChangeList = list(profitsDF["SPY Change"])
    alphaList = list(profitsDF["Alpha"])

    notional = [10000]
    i = 1
    for i in range(len(returnsList)):
        notional.append(notional[i] * (1 + returnsList[i-1]))

    notionalSpy = [10000]
    i = 1
    for i in range(len(spyChangeList)):
        notionalSpy.append(notionalSpy[i] * (1 + spyChangeList[i-1]))

    relativePerformance = []
    i = 0
    for i in range(len(notional)):
        relativePerformance.append(notional[i] - notionalSpy[i])

    plt.plot(relativePerformance)
    plt.title("Profits On $10,000 Account Relative to SPY")
    plt.xlabel("Days Traded")
    plt.ylabel("Relative Profit ($, Bot - SPY)")
    plt.savefig('Data/Relative Profit.png')

def sftpDroplet():
    with pysftp.Connection(host = 'HOSTNAMEIP', username = 'SERVERUSERNAME', password = 'PASSWORD') as sftp:
        with sftp.cd('SPY Follows AAPL/Data'):
            sftp.put('Data/Relative Profit.png')
            sftp.put('Data/Profit Tracker.csv')