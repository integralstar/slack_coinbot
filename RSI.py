import pandas as pd
import datetime
import requests
import pandas as pd
import time
import numpy as np

def RSI(coin, min=5, cnt=100):
    url = "https://api.upbit.com/v1/candles/minutes/" + str(min)
    querystring = {"market":coin,"count":str(cnt)}
    response = requests.request("GET", url, params=querystring)
    data = response.json()
    df = pd.DataFrame(data)
    df = df.reindex(index=df.index[::-1]).reset_index()
    df['close'] = df["trade_price"]

    #print(df['close'])
    
    def rsi(ohlc: pd.DataFrame, period: int = 14):
        ohlc["close"] = ohlc["close"]
        delta = ohlc["close"].diff()

        up, down = delta.copy(), delta.copy()
        up[up < 0] = 0
        down[down > 0] = 0

        _gain = up.ewm(com=(period - 1), min_periods=period).mean()
        _loss = down.abs().ewm(com=(period - 1), min_periods=period).mean()

        RS = _gain / _loss
        return pd.Series(100 - (100 / (1 + RS)), name="RSI")

    rsi = rsi(df, 14).iloc[-1]
    #print(rsi)

    return rsi

if __name__ == '__main__':
    RSI("KRW-XRP", 3, 200)