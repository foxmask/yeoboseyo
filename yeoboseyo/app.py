# coding: utf-8
"""
   여보세요 App
"""
import databases
# yeoboseyo
from forms import TriggerSchema
from models import Trigger

# starlette
from starlette.applications import Starlette
from starlette.config import Config
from starlette.responses import RedirectResponse
from starlette.routing import Mount, Route

from starlette.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates

import sqlalchemy
# schema validation
import typesystem
import uvicorn

forms = typesystem.Jinja2Forms(package="bootstrap4")
templates = Jinja2Templates(directory="templates")
statics = StaticFiles(directory="static")

metadata = sqlalchemy.MetaData()
config = Config('.env')
DATABASE_URL = config('DATABASE_URL')
database = databases.Database(DATABASE_URL, force_rollback=True)


async def homepage(request):
    """
    get the list of triggers
    :param request:
    :return:
    """
    triggers = await Trigger.objects.all()
    template = "index.html"
    form = forms.Form(TriggerSchema)
    context = {"request": request, "form": form, "triggers_list": triggers}
    return templates.TemplateResponse(template, context)


async def add_trigger(request):
    data = await request.form()
    trigger, errors = TriggerSchema.validate_or_error(data)
    print(trigger, errors)
    if errors:
        triggers = await Trigger.objects.all()
        form = forms.Form(TriggerSchema, values=data, errors=errors)
        context = {"request": request, "form": form, "triggers": triggers}
        return templates.TemplateResponse("index.html", context)
    # Execute
    await Trigger.objects.create(rss_url=trigger.rss_url,
                                 joplin_folder=trigger.joplin_folder,
                                 description=trigger.description)

    return RedirectResponse(request.url_for("homepage"))

# HTTP Requests
# Error Pages
async def not_found(request, exc):
    """
    Return an HTTP 404 page.
    """
    template = "404.html"
    context = {"request": request}
    return templates.TemplateResponse(template, context, status_code=404)


app = Starlette(
    debug=True,
    routes=[
        Route('/', homepage, methods=['GET'], name='homepage'),
        Route('/', add_trigger, methods=['POST'], name='add_trigger'),
        Mount('/static', StaticFiles(directory='static'), name='static')
    ],
)

# Bootstrap
if __name__ == '__main__':
    print('여보세요 !')
    uvicorn.run(app, host='0.0.0.0', port=8000)
