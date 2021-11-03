import argparse
import time
import pickle
import os
from datetime import datetime
import pandas as pd
from twython import Twython
from config import TweetConfig
from urllib.parse import urlencode
# api refence: https://developer.twitter.com/en/docs/twitter-api/v1/tweets/search/api-reference/get-search-tweets

def load_config():
    try:
        with open('config.txt', 'rb') as f:
            config = pickle.load(f)
            print(f'config:{config} load')
        return config
    except Exception as e:
        print('config not exist')
        return {}

def save_config(config):
    try:
        with open('config.txt', 'wb') as f:
            pickle.dump(config,f)
        print(f'{config} saved')
    except Exception as e:
        print(f'save_config fail {e}')

def sleep_min(m):
    for i in range(m):
        for j in range(60):
            time.sleep(1)

def format_twitter(raw_twitter):
    try:
        create_time = datetime.strptime(raw_twitter['created_at'],'%a %b %d %H:%M:%S +0000 %Y')
        text = raw_twitter['text']
        user_id = raw_twitter['user']['id']
        twitter_id = raw_twitter['id']
        return {'twitter_id':twitter_id, 'user_id':user_id, 'create_time':create_time, 'text':text}
    except Exception as e:
        print(f'e:{e}, {raw_twitter}')

def get_parser():
    parser = argparse.ArgumentParser(description='推特查詢參數')
    parser.add_argument('-q', '--querykey', default='bitcoin', help='數入要搜尋的twitter # tag')
    parser.add_argument('-f', '--filename', default='tweet.csv', help='爬到的資料存取的路徑')
    parser.add_argument('-c', '--count', default=1000, type=int, help='一次要取多少資料 上限為450*100 (450次/15min 上限)')
    parser.add_argument('-l', '--last_id', default=-1,type=int, help='重複執行會從./config.txt 取得上次跑到那的紀錄')
    parser.add_argument('-e', '--end_date', default='',type=str, help='ex: "2021-11-01" 如果不是要從當下時間開始往回找資料則需要指定日期')
    parser.add_argument('-n', '--new',default='',help='重啟搜尋')
    parser.add_argument('-v',help='是否顯示log')
    return parser

def key_encoding(key):
    """
    encoding for urlencode
    """
    return urlencode({'q':key})[2:]

if __name__ == "__main__":
    try:
        
        parser = get_parser()
        args = parser.parse_args()
        if args.new:
            config = {}
        else:
            config = load_config()
        t = Twython(TweetConfig.API_KEY, TweetConfig.API_KEY_SECRET)
        query_key = args.querykey
        fn = args.filename
        total_data_count = args.count
        request_limit = min(args.count//100,450)
        last_id = args.last_id if args.last_id>0 else config.get('last_id',-1)
        end_date = args.end_date
        data_count = 0
        if end_date:
            end_date = datetime.strftime(datetime.now(),'%Y-%m-%d')
            print(f'搜尋 {end_date} 之前資料')
        if args.v:
            print(f'log config: {config} {request_limit}')
        if request_limit ==0:
            request_limit +=1
        for i in range(request_limit):
            data_per_request = 100
            if total_data_count - data_count <100:
                data_per_request = total_data_count - data_count
            if last_id >0 :
                query_result = t.search(q=query_key,count=data_per_request, max_id=last_id)
            else:
                if end_date:
                    query_result = t.search(q=query_key,count=data_per_request, until=end_date)
                else:
                    query_result = t.search(q=query_key,count=data_per_request)
            twitters = query_result['statuses']
            result = [format_twitter(twitter) for twitter in twitters]
            if result:
                last_id = result[-1]['twitter_id'] -1
            data_count = data_count + len(result)
            if args.v:
                print(f'{(i+1)*data_per_request:5d} data got, last id: {last_id}')
            df = pd.DataFrame(result)
            if os.path.isfile(fn):
                df.to_csv(fn, mode='a', encoding='utf-8',index=False, header=False)
            else:
                df.to_csv(fn, mode='a', encoding='utf-8',index=False)
        config['last_id'] = last_id
        print(f'data_add:{data_count}')
        save_config(config)
    except Exception as e:
        print(f"error:{e}")
    
    