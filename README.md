# StandupBot
A bot for daily standups

### Setup

#### Linux

```bash
pip install virtualenv
virtualenv env
source env/bin/activate
pip install slackclient
export SLACK_BOT_TOKEN='your slack token here'
export BOT_ID='your bot user id here'
```

#### Windows

```batch
pip install virtualenv
virtualenv env
env\Scripts\activate
pip install slackclient
set SLACK_BOT_TOKEN=your slack token here
set BOT_ID=your bot user id here
```