from django.template.loader import get_template
from django.template import Template, Context
from django.http import HttpResponse
import datetime

def hello(request):
    return HttpResponse("Hello world")

def overview(request):
    now = datetime.datetime.now()
    t = get_template('overview.html')
    html = t.render(Context({'current_date': now}))
    return HttpResponse(html)

def switches(request):
    now = datetime.datetime.now()
    t = get_template('switches.html')
    html = t.render(Context({'current_date': now}))
    return HttpResponse(html)
