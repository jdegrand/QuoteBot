## Initialization
Set an environment variable `TELEGRAM_BOT_KEY` to your bot key.
Ex: `export TELEGRAM_BOT_KEY=keyhere`.

### Advent Of Code Keys
To link Advent Of Code Private Leaderboards, I used three other environment variables
To set them:
First you need to login an account on Advent Of Code that has access to these private leaderboards and retrieve your session key from your browser's cookies
```
export aoc_session=session_key
```
The next two are the numbers in the link of the two private leaderboards. I replaced with random numbers to show you what it looks like:
```
export aoc_csh=222444
export aoc_b1=111111
```

## Usage
`python3 QOTC.py`

## About This Bot
I made this bot for Telegram for use in my group chats to add an even better experience to our messaging, on top of the already spectacular one Telegram provides
