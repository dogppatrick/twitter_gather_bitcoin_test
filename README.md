api 參考
https://developer.twitter.com/en/docs/twitter-api/v1/tweets/search/api-reference/get-search-tweets

install
'''
pip install -r requirements.txt
'''

需要修改參數:
'''
query_target = 'bitcoin' #你要查的關鍵字
start_date = datetime.strftime(datetime(2021,10,25),'%Y-%m-%d') #最後時間格是為 2021-11-02
end_date = datetime.strftime(datetime(2021,10,31),'%Y-%m-%d')
last_id = None # 一次request 只拿到100筆 要繼續取完就 要拿id -1
'''