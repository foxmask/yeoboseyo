# 여보세요

let's the services say "hello" (여보세요 in Korean : `yeoboseyo`) to each others

This `hello` can be any data you want to get and send from any internet service to another

Services covered:

- Joplin markdown editor
- RSS Feeds

## Installation

create a virtualenv

```bash
python3.6 -m venv yeoboseyo
cd yeoboseyo
source bin/activate
pip install -r requirements.txt
```

## Database

create the database (to execute only once)
```bash
python models.py
```

## Settings
```bash
mv env.sample .env
```
set the correct values for oyour environments
```ini
DATABASE_URL=sqlite:///db.sqlite3
TIME_ZONE=Europe/Paris
JOPLIN_URL=http://127.0.0.1
JOPLIN_PORT=41184
JOPLIN_TOKEN=
FORMAT_FROM=markdown_github
FORMAT_TO=html
BYPASS_BOZO=False
LOG_LEVEL=logging.INFO
```

## Running

start the application
```bash
cd yeoboseyo
python app.py &여보세요 !
INFO: Started server process [13588]
INFO: Waiting for application startup.
INFO: Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
```

grab the Feeds to create joplin note, for example
```bash
python run.py

여보세요 ! RUN and GO
Trigger FoxMasK blog
 Entries created 1 / Read 1

```