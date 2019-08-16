# coding: utf-8
"""
   여보세요 App
"""
import os
import sys

# starlette
from starlette.applications import Starlette
from starlette.endpoints import HTTPEndpoint
from starlette.responses import RedirectResponse
from starlette.routing import Mount, Route
from starlette.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates

# schema validation
import typesystem
# uvicorn
import uvicorn
# yeoboseyo
PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
PARENT_FOLDER = os.path.dirname(PROJECT_DIR)
sys.path.append(PARENT_FOLDER)
from yeoboseyo.forms import TriggerSchema
from yeoboseyo.models import Trigger

forms = typesystem.Jinja2Forms(package="bootstrap4")
templates = Jinja2Templates(directory="templates")
statics = StaticFiles(directory="static")


class TriggerEndpoint(HTTPEndpoint):

    async def get(self, request):
        # trigger_id provided, form to edit this one
        trigger_id = request.path_params['trigger_id']
        trigger = await Trigger.objects.get(id=trigger_id)
        form = forms.Form(TriggerSchema, values=trigger)

        triggers = await Trigger.objects.all()
        context = {"request": request, "form": form, "triggers_list": triggers, "trigger_id": trigger_id}
        return templates.TemplateResponse("index.html", context)

    async def post(self, request):
        triggers = await Trigger.objects.all()

        data = await request.form()
        trigger, errors = TriggerSchema.validate_or_error(data)

        if errors:
            form = forms.Form(TriggerSchema, values=data, errors=errors)
            context = {"request": request, "form": form, "triggers_list": triggers}
            return templates.TemplateResponse("index.hml", context)

        if 'trigger_id' in request.path_params:
            trigger_id = request.path_params['trigger_id']
            trigger_to_update = await Trigger.objects.get(id=trigger_id)
            await trigger_to_update.update(rss_url=trigger.rss_url,
                                           joplin_folder=trigger.joplin_folder,
                                           subreddit=trigger.subreddit,
                                           mastodon=trigger.mastodon,
                                           status=trigger.status,
                                           description=trigger.description)
        else:
            await Trigger.objects.create(rss_url=trigger.rss_url,
                                         joplin_folder=trigger.joplin_folder,
                                         subreddit=trigger.subreddit,
                                         mastodon=trigger.mastodon,
                                         status=trigger.status,
                                         description=trigger.description)

        return RedirectResponse(request.url_for("homepage"))


async def homepage(request):
    """
    get the list of triggers
    :param request:
    :return:
    """
    trigger_id = 0
    form = forms.Form(TriggerSchema)
    triggers = await Trigger.objects.all()
    context = {"request": request, "form": form, "triggers_list": triggers, "trigger_id": trigger_id}
    return templates.TemplateResponse("index.html", context)


async def delete(request):
    """
    delete a trigger
    :param request:
    :return:
    """
    if 'trigger_id' in request.path_params:
        trigger_id = int(request.path_params['trigger_id'])
        trigger = await Trigger.objects.get(id=trigger_id)
        await trigger.delete()
    return RedirectResponse(request.url_for("homepage"))


app = Starlette(
    debug=True,
    routes=[
        Route('/', homepage, methods=['GET', 'POST'], name='homepage'),
        Route('/new', endpoint=TriggerEndpoint, methods=['POST'], name='new'),
        Route('/edit/{trigger_id:int}', endpoint=TriggerEndpoint, methods=['POST', 'GET'], name='edit'),
        Route('/delete/{trigger_id:int}', delete, methods=['GET'], name='delete'),
        Mount('/static', StaticFiles(directory='static'), name='static')
    ],
)


# HTTP Requests
# Error Pages
@app.exception_handler(404)
async def not_found(request, exc):
    """
    Return an HTTP 404 page.
    """
    template = "404.html"
    context = {"request": request}
    return templates.TemplateResponse(template, context, status_code=404)


@app.exception_handler(500)
async def server_error(request, exc):
    """
    Return an HTTP 500 page.
    """
    template = "500.html"
    context = {"request": request}
    return templates.TemplateResponse(template, context, status_code=500)

# Bootstrap
if __name__ == '__main__':
    print('여보세요 !')
    uvicorn.run(app, host='0.0.0.0', port=8000)
