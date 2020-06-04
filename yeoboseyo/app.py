# coding: utf-8
"""
   여보세요 App
"""
import arrow
import logging
import os
import sys

# starlette
from starlette.applications import Starlette
from starlette.config import Config
from starlette.responses import JSONResponse
from starlette.routing import Mount, Route, Router
from starlette.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates

# uvicorn
import uvicorn
# yeoboseyo
PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
PARENT_FOLDER = os.path.dirname(PROJECT_DIR)
sys.path.append(PARENT_FOLDER)
from yeoboseyo.forms import TriggerSchema
from yeoboseyo.models import Trigger

templates = Jinja2Templates(directory="templates")
statics = StaticFiles(directory="static")
config = Config('.env')

main_app = Starlette()
main_app.debug = config('', default=False)

logger = logging.getLogger(__name__)


async def homepage(request):
    context = {"request": request}
    return templates.TemplateResponse("base.html", context)


async def get_all(request):
    """
    responses:
      200:
        description: get the list of source of feeds
        examples:
          [{"id": 1}, {"title": "Github Rss Feeds"}, {"url": "https://github.com/rss"}, {"folder": 1},
          {"date_created": "2020-05-12T01:00"}, {"date_modified": "2020-05-12T18:27:2"}, {"status": True}]
    """
    data = await Trigger.objects.all()
    content = [
        {
            "id": result["id"],
            "rss_url": result["rss_url"],
            "description": result["description"],
            "joplin_folder": result["joplin_folder"],
            "reddit": result["reddit"],
            "localstorage": result["localstorage"],
            "mastodon": result["mastodon"],
            "mail": result["mail"],
            "status": result["status"],
            "date_created": result['date_created'],
            "date_triggered": result['date_triggered']
        }
        for result in data
    ]
    logger.debug("get that trigger")
    return JSONResponse(content)


async def get(request):
    """
    responses:
      200:
        description: get the list of source of feeds
        examples:
          [{"id": 1}, {"title": "Github Rss Feeds"}, {"url": "https://github.com/rss"}, {"folder": 1},
          {"date_created": "2020-05-12T01:00"}, {"date_modified": "2020-05-12T18:27:2"}, {"status": True}]
    """
    # trigger_id provided, form to edit this one
    trigger_id = request.path_params['trigger_id']
    result = await Trigger.objects.get(id=trigger_id)
    content = {"id": trigger_id,
               "rss_url": result["rss_url"],
               "description": result["description"],
               "joplin_folder": result["joplin_folder"],
               "reddit": result["reddit"],
               "localstorage": result["localstorage"],
               "mastodon": result["mastodon"],
               "mail": result["mail"],
               "status": result["status"],
               "date_created": result['date_created'],
               "date_triggered": result['date_triggered']}
    logger.debug("get all Triggers")
    return JSONResponse(content)


async def create(request):
    payload = await request.json()
    trigger, errors = TriggerSchema.validate_or_error(payload)

    if errors:
        content = {"errors": errors, "data": payload}
        logger.debug("error during creating a trigger")

    else:
        result = await Trigger.objects.create(description=trigger.description,
                                              rss_url=trigger.rss_url,
                                              joplin_folder=trigger.joplin_folder,
                                              reddit=trigger.reddit,
                                              localstorage=trigger.localstorage,
                                              mastodon=trigger.mastodon,
                                              mail=trigger.mail,
                                              status=trigger.status,
                                              )
        payload = {
            'description': result.description,
            'rss_url': result.rss_url,
            'joplin_folder': result.joplin_folder,
            'reddit': result.reddit,
            'localstorage': result.localstorage,
            'mastodon': result.mastodon,
            'mail': result.mail,
            'status': result.status,
            'date_created': str(result.date_created),
            'date_triggered': str(result.date_triggered),
        }
        content = {"errors": errors, "data": payload}
        logger.debug("create a trigger")
    return JSONResponse(content)


async def update(request):
    if 'trigger_id' in request.path_params:
        trigger_id = int(request.path_params['trigger_id'])
        data = await request.form()
        trigger, errors = TriggerSchema.validate_or_error(data)

        if errors:
            content = {"errors": errors,
                       "data": trigger,
                       "trigger_id": trigger_id}
            logger.debug(f"error during updating trigger {trigger_id}")
        else:
            trigger_to_update = await Trigger.objects.get(id=trigger_id)
            result = await trigger_to_update.update(rss_url=trigger.rss_url,
                                                    joplin_folder=trigger.joplin_folder,
                                                    reddit=trigger.reddit,
                                                    mastodon=trigger.mastodon,
                                                    localstorage=trigger.localstorage,
                                                    mail=trigger.mail,
                                                    status=trigger.status,
                                                    description=trigger.description)
            payload = {
                'description': result.description,
                'rss_url': result.rss_url,
                'joplin_folder': result.joplin_folder,
                'reddit': result.reddit,
                'localstorage': result.localstorage,
                'mastodon': result.mastodon,
                'mail': result.mail,
                'status': result.status,
                'date_created': str(result.date_created),
                'date_triggered': str(result.date_triggered),
            }
            content = {'errors': [], 'data': payload}
    else:
        errors = dict({'message': 'Trigger id is missing'})
        content = {'errors': errors, 'data': ''}

    logger.debug(f"update trigger {trigger_id}")
    return JSONResponse(content)


async def delete(request):
    """
    delete a trigger
    :param request:
    :return:
    """
    if 'trigger_id' in request.path_params:
        trigger_id = int(request.path_params['trigger_id'])
        trigger = await Trigger.objects.get(id=trigger_id)
        result = await trigger.delete()
        logger.debug("delete a trigger")
        content = {'errors': [], 'data': result}
        logger.debug(f"error during deleting trigger {trigger_id}")
    else:
        errors = dict({'message': 'Trigger id is missing'})
        content = {'errors': errors, 'data': ''}
        logger.debug(f"delete trigger")
    return JSONResponse(content)


async def switch(request):
    """
    switch some status of that trigger
    :param request:
    :return:
    """
    if 'trigger_id' in request.path_params:
        trigger_id = int(request.path_params['trigger_id'])
        trigger = await Trigger.objects.get(id=trigger_id)
        date_triggered = trigger.date_triggered
        if trigger.status is False:
            date_triggered = arrow.utcnow().to(
                config('TIME_ZONE')).format('YYYY-MM-DD HH:mm:ssZZ')
        trace = ''
        if 'switch_type' in request.path_params and \
                request.path_params['switch_type'] == 'status':
            await trigger.update(status=not trigger.status,
                                 date_triggered=date_triggered)
            trace = f"switch status trigger {trigger_id}"
        elif 'switch_type' in request.path_params and \
                request.path_params['switch_type'] == 'masto':
            await trigger.update(mastodon=not trigger.mastodon)
            trace = f"switch mastodon trigger {trigger_id}"
        elif 'switch_type' in request.path_params and \
                request.path_params['switch_type'] == 'mail':
            await trigger.update(mail=not trigger.mail)
            trace = f"switch mail trigger {trigger_id}"

        payload = {
            'description': trigger.description,
            'rss_url': trigger.rss_url,
            'joplin_folder': trigger.joplin_folder,
            'reddit': trigger.reddit,
            'localstorage': trigger.localstorage,
            'mastodon': trigger.mastodon,
            'mail': trigger.mail,
            'status': trigger.status,
            'date_created': str(trigger.date_created),
            'date_triggered': str(trigger.date_triggered),
        }
        content = {'errors': [], 'data': payload}
        logger.debug(trace)
    else:
        errors = dict({'message': 'Trigger id is missing'})
        content = {'errors': errors, 'data': ''}
        logger.debug(f"error during switch status trigger")
    return JSONResponse(content)


# The API Routes
api = Router(routes=[
    Mount('/yeoboseyo', app=Router([
        Route('/', endpoint=get_all, methods=['GET']),
        Route('/{trigger_id}', endpoint=get, methods=['GET']),
        Route('/', endpoint=create, methods=['POST']),
        Route('/{trigger_id}', endpoint=update, methods=['PATCH']),
        Route('/{trigger_id}', endpoint=delete, methods=['DELETE']),
        Route('/switch/{switch_type}/{trigger_id:int}', switch, methods=['PATCH'], name='switch'),
    ]))
])

app = Starlette(
    debug=True,
    routes=[
        Route('/', homepage, methods=['GET'], name='homepage'),
        Mount('/static', StaticFiles(directory="static")),
    ],
)

main_app.mount('/api', app=api)
main_app.mount('/', app=app)

# Bootstrap
if __name__ == '__main__':
    print('여보세요 !')
    uvicorn.run(main_app, host='0.0.0.0', port=8000)
