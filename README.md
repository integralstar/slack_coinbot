### slack_coinbot
주기적으로 코인 가격과 RSI를 slack에 출력
거래 기능만 추가하시면 RSI 지표를 이용한 자동거래 bot으로 사용하실 수 있습니다.

#### windows
set SLACK_API_TOKEN = xoxb-XXXXXXX

#### xnix, mac
export SLACK_API_TOKEN = xoxb-XXXXXXX

pip3 install pyupbit

pip3 install apscheduler

pip3 install slackclient
