#https://chasuke.com/motionsensor/
#with open de 
from datetime import datetime
import time
import RPi.GPIO as GPIO
import requests
#ローカルにもlogを保存させる(txt or csv or Liburre Office?)
# インターバル
INTERVAL = 0.5
# スリープタイム
SLEEPTIME = 0.5
# 使用するGPIO
GPIO_PIN = 18
#cOzQdIVl7aLYnG0Us0nbQX
GPIO.setmode(GPIO.BCM)
GPIO.setup(GPIO_PIN, GPIO.IN)

def ifttt_webhook(eventid):
    payload = {"value1":datetime.now().strftime('%Y/%m/%d %H:%M:%S') +
                    "：" + str("{0:05d}".format(cnt)) + "回目の人感知"}
    url = "https://maker.ifttt.com/trigger/pj3/with/key/***************"
    #アクセスキーは個人情報のため、***にしている
    response = requests.post(url, params=payload)
    print(response)

if __name__ == '__main__':
    try:
        flg = True
        print ("処理キャンセル：CTRL+C")
        cnt = 1
        while True:
            # センサー感知
            if(GPIO.input(GPIO_PIN) == GPIO.HIGH):
                if flg:               
                    x = datetime.now().strftime('%Y/%m/%d %H:%M:%S') + "：" + str("{0:05d}".format(cnt)) + "回目の人感知"
                    print(x)
                    #print(datetime.now().strftime('%Y/%m/%d %H:%M:%S') +
                    #    "：" + str("{0:05d}".format(cnt)) + "回目の人感知")

                    # IFTTT_Webhook
                    ifttt_webhook("line_event")
                    #with open("./log.txt","w") as txt:
                    #    txt.write("x\n")
                    cnt = cnt + 1
                    time.sleep(SLEEPTIME)
                    flg = False
            else:
                flg = True
                y = GPIO.input(GPIO_PIN)
                #print(y)
                print("感知しない")
                #print(GPIO.input(GPIO_PIN))
                #with open("./log.txt","w") as txt:
                #    txt.write(y)
                time.sleep(INTERVAL)
    except KeyboardInterrupt:
        print("終了処理中...")
    finally:
        GPIO.cleanup()
        print("GPIO clean完了")
