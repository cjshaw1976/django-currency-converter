import datetime

from django import template

from convert.models import rates

register = template.Library()
earlist = rates.objects.order_by('date').first()

@register.simple_tag
def current_date(diff=0):
    return datetime.date.today()  + datetime.timedelta(diff)

@register.simple_tag
def data_start():
    return earlist.date
