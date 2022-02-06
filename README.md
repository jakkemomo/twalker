# *Twalker*

#### Twalker is a library that gathers information from big influencers.
#### Right now it uses Twitter API to collect tweets of added influencer accounts and tweets of people that have more than 500.000 followers that communicate with the influencer.

##### Basic flow to start Twalker: 
- Add environment variables:
  * TELEGRAM_BOT_TOKEN (Main token for telegram bot)
  * TWITTER_TOKEN (Bearer token for your app: get at the https://developer.twitter.com/)
  * TELEGRAM_CHAT_ID (ID of the chat where bot should send notifications)
- Run main.py
- Add influencer account name from selected source of information (e.g. elonmusk)
- Type "Start" to initiate stalking
##### At this point program will start stalking the influencer: each new message connected to this person will be sent to Telegram Channel.
