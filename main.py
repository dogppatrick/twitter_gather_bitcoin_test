from config import TweetConfig
from twython import Twython
from datetime import datetime
import pandas as pd
# api refence: https://developer.twitter.com/en/docs/twitter-api/v1/tweets/search/api-reference/get-search-tweets

APP_KEY = TweetConfig.API_KEY
APP_SECRET = TweetConfig.API_KEY_SECRET

def format_twitter(raw_twitter):
    try:
        create_time = datetime.strptime(raw_twitter['created_at'],'%a %b %d %H:%M:%S +0000 %Y')
        text = raw_twitter['text']
        user_id = raw_twitter['user']['id']
        twitter_id = raw_twitter['id']
        return {'twitter_id':twitter_id, 'user_id':user_id, 'create_time':create_time, 'text':text}
    except Exception as e:
        print(f'e:{e}, {raw_twitter}')

t = Twython(APP_KEY, APP_SECRET)
query_target = 'bitcoin'
start_date = datetime.strftime(datetime(2021,10,25),'%Y-%m-%d')
end_date = datetime.strftime(datetime(2021,10,31),'%Y-%m-%d')
last_id = None
request_limit = 400
for i in range(request_limit):
    data_per_request = 100
    if last_id:
        query_result = t.search(q=query_target,count=data_per_request, max_id=last_id)
    else:
        query_result = t.search(q=query_target,count=data_per_request, until=end_date)
    twitters = query_result['statuses']
    result = [format_twitter(twitter) for twitter in twitters]
    last_id = result[-1]['twitter_id'] -1
    print(f'{i*data_per_request} data got, last id: {last_id}')
    df = pd.DataFrame(result)
    df.to_csv('tweet.csv', mode='a', encoding='utf-8',index=False)


