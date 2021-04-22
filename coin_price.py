from pyupbit import WebSocketManager

#print(pyupbit.get_tickers())
#print(pyupbit.get_current_price("KRW-BTC"))

if __name__ == "__main__":
    wm_btc = WebSocketManager("ticker", ["KRW-BTC"])
    wm_xrp = WebSocketManager("ticker", ["KRW-XRP"])
    btc = wm_btc.get()
    xrp = wm_xrp.get()
    
    print("BTC 현재가: ", btc['trade_price'], "원")
    print(format(btc['signed_change_rate'] * 100, '.3f'), "%", btc['signed_change_price'], "원 변동기준(일)")
    print()
    print("XRP 현재가: ", xrp['trade_price'], "원")
    print(format(xrp['signed_change_rate'] * 100, '.3f'), "%", xrp['signed_change_price'], "원 변동기준(일)")

    wm_btc.terminate()
    wm_xrp.terminate()