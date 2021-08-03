# 여보세요

![Yeoboseyo home page](doc/Yeoboseyo_list.png)

## Description

The app allow you to generate markdown files from grabbed RSS Feeds


## Services covered 

* RSS
* Mastodon
* Mattermost
* Slack
* Discord
* Local Markdown file

## :package: Installation

### pre requisistes

- python 3.8+
- starlette (the web application)
- feedparser (for RSS support)
- pypandoc (to convert html to markdown)

### Installation
create a virtualenv

```bash
python3 -m venv yeoboseyo
cd yeoboseyo
source bin/activate
pip install -r requirements.txt
```

##  :wrench: Settings
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
MASTODON_USERNAME=your email
MASTODON_PASSWORD=your pass
MASTODON_INSTANCE=https://url instance of mastodon
MASTODON_VISIBILITY=unlisted  # default is 'public', can be 'unlisted', 'private', 'direct'
```

### Mastodon

to create the app on mastodon :

on https://yourmasto instance/settings/applications/new

Application name : Yeoboseyo
Scopes : check : read / write / push / follow
then submit

then select Yeoboseyo again to retreive the access token, in a file name `yeoboseyo_clientcred.secret` put on the first line the value of "Your access token" and on the second line the https url of your masto instance eg
```
Azdfghy5678hefdsgghjuju09knb
https://framapiaf.org
```
this file will be read each time something will be posted on masto

### Slack/Mattermost/Discord Webhook

in the 'integrations' page set an "incoming webhooks" (eg from https://mattermost/teamname/integrations) and copy the URL into the field 'webhook' of the Yeoboseyo form


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

Go on http://0.0.0.0:8000 and fill the form to add new Feeds to track

* If you plan to publish RSS Feeds into a joplin note, fill the "Joplin folder" field, if not leave it empty.
* If you plan to publish RSS Feeds on your Mastodon account, check the checkbox "Publish on Mastodon?", if not, leave it unchecked

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


(Image credits to [Emojipedia](https://emojipedia.org/))
