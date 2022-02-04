# *Twalker*

#### Twalker is a library that gathers information from big influencers.
#### Right now it uses Twitter API to collect tweets and retweets of added influencer accounts.

##### Basic flow to start Twalker: 
- Add environment variables TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID, TWITTER_TOKEN
- Run main.py
- Choose source of information (e.g. Twitter)
- Add influencer profile url from selected source of information (e.g. https://twitter.com/elonmusk)
- Choose menu option "Start"
##### At this point program will start stalking the influencer: each new message connected to this person will be sent to Telegram Channel.
