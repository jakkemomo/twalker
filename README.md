# *Twalker*

#### Twalker is a library that gathers information from big influencers.
#### Right now it uses Twitter API to collect tweets and retweets of added influencer accounts.

##### Basic flow to start Twalker: 
- Add environment variables TELEGRAM_BOT_TOKEN, TWITTER_TOKEN, etc.
- Run main.py
- Enter name of the influencer
- Choose source of information (e.g. Twitter)
- Add influencer profile url from selected source of information
- Choose menu option: Start
##### At this point program will start stalking the influencer: each new message connected to this person will be sent to Telegram Channel.