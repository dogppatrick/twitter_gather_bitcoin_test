import praw
reddit = praw.Reddit('bot_bitcoin', user_agent='bot_bitcoin')
subreddit = reddit.subreddit("Bitcoin")
subs = subreddit.hot(limit=10)
for sub in subs:
    print(sub.title)
    print(sub.score)
    for comment in sub.comments:
        print(comment.body)