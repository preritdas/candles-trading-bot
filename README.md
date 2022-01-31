# Volume and Candles Trading Bot

This bot uses volume imbalances (deprecated) and candlestick patterns to determine if it should be long or short a particular symbol every minute. Each order is submitted to Alpaca Markets with a 2% bracket attached. All trades are played out to target or stop. If no trade setup is detected in a particular minute, it waits until the next minute to check for a setup. 

## Configuration

Currently, the bot is set to trade engulfing candles, morning-star series, and their confluence. Originally, it was configured to trade those along with volume imbalance and four other patterns. I retired those after seeing suboptimal results with high trade fees (trades were triggered long or short almost every minute).

New patterns can be calculated using the imported `TA-Lib` library:

```python
pattern = talib.CDLcandlePattern(data['Opens'], data['Highs'], data['Lows'], data['Closes'])
data["pattern"] = pattern # append running data with the new pattern
```

Then, modifying the execution script (where the Alpaca order is actually sent in `main.py`):
```python
if data["pattern"][4] == 100:
    # some multi-triggered or individual trade logic involving this pattern being long
if data["pattern"][4] == -100:
    # some multi-triggered or individual trade logic involving this pattern being short
```

## Automated Profit-Tracking

I originally wrote this for another trading bot and haven't translated it for this one, so some of the code might references data that isn't specific to this program. It can be easily translated, though. The corresponding file in the repository is `profits.py`.

### How it works

When you call the `updateCSV()` function at a certain time (probably after market close every day), it will read the associated Alpaca account and calculate the percent change (performance of the bot). It then uses Yahoo Finance to find out how much SPY changed. It then appends (or creates if nonexistent) a `Profit Tracker.csv` file located in the `Data/` subdirectory. It calculates an `alpha` for the day, defined as `botPerformance - spyChange`. 

It has a deprecated function for graphing, too. It graphs a notional account with $10,000, daily profits, outperformance of SPY by dollar, relative profit, and alpha. All of this data comes from the `Data/'Profit Tracker.csv` which updates itself every day.