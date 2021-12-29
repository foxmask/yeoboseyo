# 여보세요

![Yeoboseyo home page](https://gitlab.com/annyong/yeoboseyo/-/raw/master/doc/Yeoboseyo_list.png)

## Description

From your favorite RSS feeds, spread/share those news to services of your choice


## Services covered 

* RSS
* Mastodon
* Mattermost
* Slack
* Discord
* Telegram
* Wallabag
* Local Markdown files
* Any services using a Webhook to push data

### used cases:

* With Yeoboseyo you set an RSS URL and the "local storage" (the folder where to store news in markdown) then you synchronize those files with [syncthing](https://syncthing.net/) on any of your devices and read them with [Espilon Notes](http://epsilonexpert.com/), [Notable](https://notable.app/), [markor](https://gsantner.net/project/markor.html). Any markdown editor/reader can open/import those files.
This use case can be extended to any application that is able to import markdown file, use file manager or has import function, like [TagSpaces](https://www.tagspaces.org/)


* You want to publish news from your favorite news websites to `Mastodon`, Yeoboseyo will do that without any problem

 
* You need to spread news from your project on `Mattermost`/`Slack`/`Discord`, just set the URL of the `Webhook` of one of those services and the news will be published as expected on the `channel` of your choice
* If you prefer to publish that on `Telegram`, set the `TELEGRAM_CHAT_ID` of the group or channel  

Let see how to setup all of that below


## :package: Installation

### pre requisistes

- python 3.8+
- [starlette](https://www.starlette.io/) (the web application)
- [feedparser](https://feedparser.readthedocs.io/en/latest/) (for RSS support)
- [pypandoc](https://pypi.org/project/pypandoc/) (to convert html to markdown)
- [wallabag API](https://gitlab.com/foxmask/wallabag_api) for [Wallabag](https://wallabag.org/en) readit later applications

### Installation

create a virtualenv

```bash
python3 -m venv yeoboseyo
cd yeoboseyo
source bin/activate
```

then

```bash
pip install -r requirements.txt
```

or 

```bash
pip install yeoboseyo
```

##  :wrench: Settings

copy or rename the config file

```bash
mv env.sample .env
```

set the correct values for your own environment

```ini
DATABASE_URL=sqlite:///db.sqlite3
TIME_ZONE=Europe/Paris
FORMAT_FROM=markdown_github
FORMAT_TO=html
BYPASS_BOZO=False   # if you don't want to get the malformed RSS Feeds set it to False
LOG_LEVEL=logging.INFO
MASTODON_USERNAME=your username@<domain instance of mastodon> 
MASTODON_PASSWORD=your pass
MASTODON_INSTANCE=https://<domain instance of mastodon>
MASTODON_VISIBILITY=unlisted  # default is 'public', can be 'unlisted', 'private', 'direct'
TOKEN=''
TELEGRAM_TOKEN=0123456789:AZERTYUIOPQSDFGHJKLMWXCVBN123456789
TELEGRAM_CHAT_ID=-NNNNNNNNN
WALLABAG_URL=http://wallabag/
WALLABAG_CLIENTID=your id
WALLABAG_CLIENTSECRET=your secret
WALLABAG_PASSWORD=wallabag
WALLABAG_USERNAME=wallabag
```

### Mastodon

to create the app on mastodon :

on https://yourmastoinstance/settings/applications/new

* Application name : `Yeoboseyo`
* Scopes : check : `read` / `write` / `push` / `follow`
* then `submit`

then select Yeoboseyo again to retreive the access token, and fill the file `yeoboseyo_clientcred.secret` put on the first line the value of "Your access token" and on the second line the https url of your masto instance eg

```bash
Azdfghy5678hefdsgghjuju09knb
https://framapiaf.org
```

this file will be read each time something will be posted on masto

### Slack/Mattermost/Discord: Webhook

in the 'integrations' page set an "incoming webhooks" (eg from https://mattermost/teamname/integrations) and copy the URL into the field 'webhook' of the Yeoboseyo form


### Telegram

you will need to create a `Telegram Bot` by invoking [@BotFather](https://core.telegram.org/bots).
Once the bot is created, create a group / channel, and invite your bot on that group/channel and give it admin rights.

Now you need to get the ID of the group / channel where the bot can "speak"

for that : access to your bot history url

https://api.telegram.org/botXXXXX:YYYYY/getUpdates

and spot this kind of data

```json
chat:
  id: -NNNNNN
  title: "my group name"  
```

pick up the `-NNNNNN` and put it as the `TELEGRAM_CHAT_ID` in the `.env` config file

### Wallabag

Create a client API like explain here https://doc.wallabag.org/fr/developer/api/oauth.html

this will give you something like this

![Wallabag](https://gitlab.com/foxmask/wallabag_api/-/raw/master/wallabag_api_key.png)

Then replace the client_id / client_secret / login / pass in the .env file

```ini
WALLABAG_URL=http://wallabag/
WALLABAG_CLIENTID=your id
WALLABAG_CLIENTSECRET=your secret
WALLABAG_PASSWORD=wallabag
WALLABAG_USERNAME=wallabag
```


## :dvd: Database

create the database (to execute only once)

```bash
python models.py
```

## :mega: Running the Web application

start the application

```bash
cd yeoboseyo
python app.py &
여보세요 !
INFO: Started server process [13588]
INFO: Waiting for application startup.
INFO: Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
```

### :eyes: Adding some Feeds to track

Go on `http://0.0.0.0:8000` and fill the form to add new Feeds to track

* If you plan to publish RSS Feeds 
  * into a `local folder`, fill the `local storage` field with the complet path of that folder, if not leave it empty.
  * on your `Mastodon` account, tick the checkbox `Publish on Mastodon?`, if not, leave it unchecked
  * on your `Telegram` group/channel tick the checkbox `Publish on Telegram?`, if not, leave it unchecked
  * on your `Mattermost`/`Slack`/`Discord` group/channel, just set the URL of the `Webhook` of one of those services, if not, leave it empty.

###  :dizzy: Running the engine

now that you fill settings, and form, launch the command and see how many feeds are comming

```bash
여보세요 !
usage: python run.py [-h] -a {report,go,switch} [-trigger_id TRIGGER_ID]

Yeoboseyo

optional arguments:
  -h, --help            show this help message and exit
  -a {report,go,switch}
                        choose -a report or -a go or -a swtch -trigger_id <id>
  -trigger_id TRIGGER_ID
                        trigger id to switch of status


python run.py -a go

여보세요 ! RUN and GO
Trigger FoxMasK blog
 Entries created 1 / Read 1

```

### get the list

get the list of your feeds to check which one provided articles or not

```bash
$ python run.py -a report
여보세요 !
 Report
┏━━━━┳━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━┳━━━━━━━━━┳━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ ID ┃ Name                ┃ Md Folder ┃ Tags    ┃ Status ┃ Triggered                  ┃
┡━━━━╇━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━╇━━━━━━━━━╇━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
│ 1  │ Mon Blog            │ test      │ News    │ Ok     │ 2021-03-18 22:35:21        │
│ 2  │ KBS Culture         │ test      │ News    │ Ok     │ 2021-04-05 09:59:03        │
│ 3  │ KBS journal du jour │ test      │ News    │ Ok     │ 2021-04-05 09:59:05        │
│ 4  │ KBS Show biz        │ test      │ News    │ Ok     │ 2021-04-05 09:59:06        │
│ 5  │ Jux Video           │ test      │ jeux    │ Ok     │ 2021-04-01 22:22:15.113871 │
│ 6  │ PlayStation Blog    │ test      │ jeux    │ Ok     │ 2021-04-01 22:22:57.189312 │
│ 7  │ GameKult            │ test      │ jeux    │ Ok     │ 2021-04-01 22:23:21.049307 │
│ 8  │ Gameblog            │ test      │ jeux    │ Ok     │ 2021-04-01 22:23:48.350934 │
│ 9  │ NoFrag              │ test      │ jeux    │ Ok     │ 2021-04-01 22:24:15.721174 │
│ 10 │ Frandroid           │ test      │ android │ Ok     │ 2021-04-01 22:24:47.324475 │
│ 11 │ Les Numeriques      │ test      │ android │ Ok     │ 2021-04-01 22:25:09.740677 │
│ 12 │ VueJS News          │ test      │ vuejs   │ Ok     │ 2021-04-01 22:25:34.307735 │
│ 13 │ Cacktus Blog        │ test      │ python  │ Ok     │ 2021-04-01 22:26:02.412688 │
│ 14 │ Python News         │ test      │ python  │ Ok     │ 2021-04-01 22:26:41.975564 │
│ 15 │ nedbatchelder       │ test      │ python  │ Ok     │ 2021-04-01 22:28:21.838166 │
│ 16 │ Django News         │ test      │ Python  │ Ok     │ 2021-04-01 22:28:47.804644 │
│ 17 │ Python Insider      │ test      │ Python  │ Ok     │ 2021-04-01 22:29:18.791661 │
│ 18 │ PyCharm Blog        │ test      │ Python  │ Ok     │ 2021-04-01 22:29:44.568828 │
│ 19 │ Real Python         │ test      │ Python  │ Ok     │ 2021-04-01 22:30:10.952486 │
│ 20 │ VueJS               │ test      │ VueJS   │ Ok     │ 2021-04-01 22:30:34.507337 │
│ 21 │ Odieux Connard      │ test      │ Humour  │ Ok     │ 2021-04-01 22:31:03.458147 │
└────┴─────────────────────┴───────────┴─────────┴────────┴────────────────────────────┘

```

### switch the status of a trigger

switch the status of trigger to on/off

```bash
python run.py -a switch -trigger_id 1

여보세요 ! Switch
Successfully disabled Trigger 'Mon Blog'
```

and check it again to see the status moving

```bash 
09:00 $ python run.py -a report
여보세요 !
 Report
┏━━━━┳━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━┳━━━━━━━━━┳━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ ID ┃ Name                ┃ Md Folder ┃ Tags    ┃ Status   ┃ Triggered                  ┃
┡━━━━╇━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━╇━━━━━━━━━╇━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
│ 1  │ Mon Blog            │ test      │ News    │ Disabled │ 2021-05-15 09:00:27        │
│ 2  │ KBS Culture         │ test      │ News    │ Ok       │ 2021-04-05 09:59:03        │
│ 3  │ KBS journal du jour │ test      │ News    │ Ok       │ 2021-04-05 09:59:05        │
│ 4  │ KBS Show biz        │ test      │ News    │ Ok       │ 2021-04-05 09:59:06        │
│ 5  │ Jux Video           │ test      │ jeux    │ Ok       │ 2021-04-01 22:22:15.113871 │
│ 6  │ PlayStation Blog    │ test      │ jeux    │ Ok       │ 2021-04-01 22:22:57.189312 │
│ 7  │ GameKult            │ test      │ jeux    │ Ok       │ 2021-04-01 22:23:21.049307 │
│ 8  │ Gameblog            │ test      │ jeux    │ Ok       │ 2021-04-01 22:23:48.350934 │
│ 9  │ NoFrag              │ test      │ jeux    │ Ok       │ 2021-04-01 22:24:15.721174 │
│ 10 │ Frandroid           │ test      │ android │ Ok       │ 2021-04-01 22:24:47.324475 │
│ 11 │ Les Numeriques      │ test      │ android │ Ok       │ 2021-04-01 22:25:09.740677 │
│ 12 │ VueJS News          │ test      │ vuejs   │ Ok       │ 2021-04-01 22:25:34.307735 │
│ 13 │ Cacktus Blog        │ test      │ python  │ Ok       │ 2021-04-01 22:26:02.412688 │
│ 14 │ Python News         │ test      │ python  │ Ok       │ 2021-04-01 22:26:41.975564 │
│ 15 │ nedbatchelder       │ test      │ python  │ Ok       │ 2021-04-01 22:28:21.838166 │
│ 16 │ Django News         │ test      │ Python  │ Ok       │ 2021-04-01 22:28:47.804644 │
│ 17 │ Python Insider      │ test      │ Python  │ Ok       │ 2021-04-01 22:29:18.791661 │
│ 18 │ PyCharm Blog        │ test      │ Python  │ Ok       │ 2021-04-01 22:29:44.568828 │
│ 19 │ Real Python         │ test      │ Python  │ Ok       │ 2021-04-01 22:30:10.952486 │
│ 20 │ VueJS               │ test      │ VueJS   │ Ok       │ 2021-04-01 22:30:34.507337 │
│ 21 │ Odieux Connard      │ test      │ Humour  │ Ok       │ 2021-04-01 22:31:03.458147 │
└────┴─────────────────────┴───────────┴─────────┴──────────┴────────────────────────────┘

```

## Migrations

if you had the version 0.5.0:

run

```sql 
migrations/alter_table_trigger_add_telegram.sql
migrations/alter_table_trigger_add_wallabag.sql
``` 

if you had the version 0.4.0:

run 

```sql 
migrations/alter_table_trigger_add_webhook.sql
```

(Image credits to [Emojipedia](https://emojipedia.org/))

## Test

```bash
pytest
```

or

```bash
coverage run --source='.' -m pytest
coverage report -m
```
