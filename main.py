#test_line.py
#https://chasuke.com/motionsensor/
from datetime import datetime
import time
import RPi.GPIO as GPIO
import requests
#ローカルにもlogを保存させる(txt or csv or Liburre Office?)
# インターバル
INTERVAL = 2
# スリープタイム
SLEEPTIME = 2
# 使用するGPIO
GPIO_PIN = 18

GPIO.setmode(GPIO.BCM)
GPIO.setup(GPIO_PIN, GPIO.IN)

def ifttt_webhook(eventid):
    payload = {'value1': "おーい、椅子に誰か座ったぞー!!"}
    url = "https://maker.ifttt.com/trigger/" + eventid + "/with/key/*****"
    response = requests.post(url, data=payload)

if __name__ == '__main__':
    try:
        print ("処理キャンセル：CTRL+C")
        cnt = 1
        while True:
            # センサー感知
            if(GPIO.input(GPIO_PIN) == GPIO.HIGH):

                print(datetime.now().strftime('%Y/%m/%d %H:%M:%S') +
                    "：" + str("{0:05d}".format(cnt)) + "回目の人感知")

                # IFTTT_Webhook
                ifttt_webhook("line_event")

                cnt = cnt + 1
                time.sleep(SLEEPTIME)
            else:
                print(GPIO.input(GPIO_PIN))
                time.sleep(INTERVAL)
    except KeyboardInterrupt:
        print("終了処理中...")
    finally:
        GPIO.cleanup()
        print("GPIO clean完了")
