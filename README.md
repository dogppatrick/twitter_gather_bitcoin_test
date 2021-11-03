## api 參考
https://developer.twitter.com/en/docs/twitter-api/v1/tweets/search/api-reference/get-search-tweets

## 使用限制
官方限制: 450 request / 15分  
所以有需要可以設定好參數 15分為間隔執行

## install
```
pip install -r requirements.txt
```

## example
取得 最新500 則 bitcoin 推特並且存成csv檔案
```
python main.py -c 5000 -q bitcoin -f 'twitter.csv'
```

取得 2021/11/1前最新500 則 bitcoin 推特並且存成csv檔案
```
python main.py -e '2021-11-01' -c 5000 -q bitcoin -f 'twitter.csv'
```

執行後會出現config.txt 會記錄上一次執行在哪裡  
如果還要繼續加入新的資料 則直接執行程式會從上一次執行的繼續跑