from config import api, clock, account
import talib, pandas as pd, math, time
from datetime import datetime as dt

def dataLogic():
    aaplData = api.get_barset("AAPL", "minute", "5")["AAPL"]

    closes = []
    opens = []
    highs = []
    lows = []
    times = []
    for i in range(len(aaplData)):
        opens.append(aaplData[i].o)
        highs.append(aaplData[i].h)
        lows.append(aaplData[i].l)
        closes.append(aaplData[i].c)
        times.append(aaplData[i].t)

    data = pd.DataFrame(
        {
            "Times": times,
            "Opens": opens,
            "Highs": highs,
            "Lows": lows,
            "Closes": closes
        }
    )

    morningstars = talib.CDLMORNINGSTAR(data['Opens'], data['Highs'], data['Lows'], data['Closes'])
    data["morningstars"] = morningstars

    engulfings = talib.CDLENGULFING(data['Opens'], data['Highs'], data['Lows'], data['Closes'])
    data["engulfings"] = engulfings

    if data["engulfings"][4] == 100:
        print("Going long.")
        api.submit_order(
            symbol = "AAPL",
            qty = math.floor(0.05*(float(account.equity)/data["Closes"][4])), # 5% of account equity 
            side = 'buy',
            type = 'market',
            time_in_force = 'gtc',
            order_class='bracket', # Bracket order with 2% profit/loss, 1:1 RR 
            stop_loss = {'stop_price': data["Closes"][4] * 0.998,
            'limit_price': data["Closes"][4] * 0.997},
            take_profit = {'limit_price': data["Closes"][4] * 1.002}
        )
    elif data["engulfings"][4] == -100:
        print("Short")
        api.submit_order(
            symbol = "AAPL",
            qty = math.floor(0.05*(float(account.equity)/data["Closes"][4])), # 5% of account equity 
            side = 'sell',
            type = 'market',
            time_in_force = 'gtc',
            order_class='bracket', # Bracket order with 2% profit/loss, 1:1 RR 
            stop_loss = {'stop_price': data["Closes"][4] * 1.002,
            'limit_price': data["Closes"][4] * 1.003},
            take_profit = {'limit_price': data["Closes"][4] * 0.998}
        )
    else:
        print("No trade this minute.")

if __name__ == "__main__":
    print("MA Bot is online and ready.")
    print(f"Account balance: {api.get_account().equity}", "\n")
    while True:
        if clock.is_open == True:
            while clock.is_open == True:
                tic = time.perf_counter()
                dataLogic()
                toc = time.perf_counter()
                print(f"{toc - tic}")
                time.sleep(60)
        else:
            pass
        
        currentTime = dt.now().strftime("%H-%M")
        if currentTime == "13-05":
            print(f"Time for an update. Account net change: \
                {(float(api.get_account().equity) - float(api.get_account().last_equity))/(float(api.get_account().last_equity))}")
        else:
            pass #repeat cycle