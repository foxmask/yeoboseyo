# coding: utf-8
"""
   여보세요 App
"""
# starlette
from starlette.applications import Starlette
from starlette.responses import RedirectResponse
from starlette.routing import Mount, Route
from starlette.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates
# schema validation
import typesystem
# uvicorn
import uvicorn
# yeoboseyo
from yeoboseyo.forms import TriggerSchema
from yeoboseyo.models import Trigger

forms = typesystem.Jinja2Forms(package="bootstrap4")
templates = Jinja2Templates(directory="templates")
statics = StaticFiles(directory="static")


async def homepage(request):
    """
    get the list of triggers
    :param request:
    :return:
    """
    triggers = await Trigger.objects.all()
    template = "index.html"
    if request.method == 'GET':
        # trigger_id provided, form to edit this one
        if 'trigger_id' in request.path_params:
            trigger_id = request.path_params['trigger_id']
            trigger = await Trigger.objects.get(id=trigger_id)
            form = forms.Form(TriggerSchema, values=trigger)
        # empty form
        else:
            trigger_id = 0
            form = forms.Form(TriggerSchema)
        for trigger in triggers:
            print(trigger)
        context = {"request": request, "form": form, "triggers_list": triggers, "trigger_id": trigger_id}
        return templates.TemplateResponse(template, context)
    # POST
    else:
        data = await request.form()
        trigger, errors = TriggerSchema.validate_or_error(data)

        if errors:
            form = forms.Form(TriggerSchema, values=data, errors=errors)
            context = {"request": request, "form": form, "triggers_list": triggers}
            return templates.TemplateResponse(template, context)

        if 'trigger_id' in request.path_params:
            trigger_id = request.path_params['trigger_id']
            trigger_to_update = await Trigger.objects.get(id=trigger_id)
            print(trigger.rss_url, trigger.joplin_folder, trigger.description)
            await trigger_to_update.update(rss_url=trigger.rss_url,
                                           joplin_folder=trigger.joplin_folder,
                                           status=bool(trigger.status),
                                           description=trigger.description)
        else:
            await Trigger.objects.create(rss_url=trigger.rss_url,
                                         joplin_folder=trigger.joplin_folder,
                                         description=trigger.description)
        return RedirectResponse(request.url_for("homepage"))


async def delete(request):
    """
    get the list of triggers
    :param request:
    :return:
    """
    if 'trigger_id' in request.path_params:
        trigger_id = int(request.path_params['trigger_id'])
        trigger = await Trigger.objects.get(id=trigger_id)
        await trigger.delete()
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
        Route('/', homepage, methods=['GET', 'POST'], name='homepage'),
        Route('/id/{trigger_id:int}', homepage, methods=['POST', 'GET'], name='homepage'),
        Route('/delete/{trigger_id:int}', delete, methods=['GET'], name='delete'),
        Mount('/static', StaticFiles(directory='static'), name='static')
    ],
)

# Bootstrap
if __name__ == '__main__':
    print('여보세요 !')
    uvicorn.run(app, host='0.0.0.0', port=8000)
