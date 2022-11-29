import requests
import os
import json
from apscheduler.schedulers.blocking import BlockingScheduler


class BING:
    def __init__(self):
        self.api_url = 'https://bing.biturl.top'
        self.tg_token = os.environ.get('TG_TOKEN')
        self.tg_chat_id = os.environ.get('TG_CHAT_ID')

    def mian(self):
        res = requests.get(self.api_url)
        if res.status_code == 200:
            data = json.loads(res.text)
            url = data['url']
            caption = data['copyright']
            self.send_image_telegram(url, caption)
        else:
            print('取得資料失敗')

    def send_image_telegram(self, _url, caption):
        url = 'https://api.telegram.org/bot{}/sendPhoto'.format(self.tg_token)
        data = {
            'chat_id': self.tg_chat_id,
            'photo': _url,
            'caption': caption
        }
        res = requests.post(url, data=data)
        if res.status_code == 200:
            print('發送成功')
        else:
            print('發送失敗')


if __name__ == '__main__':
    bing = BING()
    scheduler = BlockingScheduler(timezone="Asia/Taipei")
    scheduler.add_job(bing.mian, 'cron', hour=9, minute=0)
    scheduler.start()
