import os
import time
from slack import WebClient
from slack.errors import SlackApiError

from pyupbit import WebSocketManager
from apscheduler.schedulers.background import BackgroundScheduler
from RSI import RSI

TIME_MIN = 3
CNT = 200

client = WebClient(
    token = os.environ['SLACK_API_TOKEN']
)

def send_to_slack(channel, text):
    try:
       
        response = client.chat_postMessage(
            channel=channel,
            text=text
        )
        # print(response)
    
    except SlackApiError as e:
        raise e

def info():
    text = []
    wm_btc = WebSocketManager("ticker", ["KRW-BTC"]) # 비트코인 정보
    wm_xrp = WebSocketManager("ticker", ["KRW-XRP"]) # 리플 정보

    # print(wm_btc)
    # print(wm_xrp)

    try:
        btc = wm_btc.get()
        xrp = wm_xrp.get()

        # print(btc)
        # print(xrp)
        if btc and xrp :

            text1 = "BTC 현재가: " + str(btc['trade_price']) + "원\n" + str(btc['signed_change_rate'] * 100) + "%\n" +  str(btc['signed_change_price']) + "원 변동기준(일)\n\n"
            text2 = "XRP 현재가: " + str(xrp['trade_price']) + "원\n" + str(xrp['signed_change_rate'] * 100) + "%\n" + str(xrp['signed_change_price']) + "원 변동기준(일)\n"

            text.append(text1)
            text.append(text2)

            try:

                for info in text:
                    send_to_slack(channel="#ai", text=info)

                rsi = []

                btc_rsi = RSI("KRW-BTC", TIME_MIN, CNT)
                xrp_rsi = RSI("KRW-XRP", TIME_MIN, CNT)

                btc_rsi = "BTC RSI 값 : " + str(btc_rsi) + "\n"
                xrp_rsi = "XRP RSI 값 : " + str(xrp_rsi) + "\n"

                rsi.append(btc_rsi)
                rsi.append(xrp_rsi)

                for rsi_value in rsi:
                    send_to_slack(channel="#ai", text=rsi_value)

            except SlackApiError as e:
                print("error : ", e)

        wm_btc.terminate()
        wm_xrp.terminate()

    except Exception as e:
        raise e

if __name__ == '__main__':
    sched = BackgroundScheduler()
    sched.add_job(info, 'interval', minutes=TIME_MIN) # 메세지 전송 간격
    sched.start()

    print("Service started...")

    try:
        while True:
            time.sleep(TIME_MIN)

    except (KeyboardInterrupt, SystemExit):
        sched.shutdown()
