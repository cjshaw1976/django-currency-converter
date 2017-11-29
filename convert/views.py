from django.http import HttpResponse
from django.shortcuts import render, redirect

from .models import rates
from . import charts

import coreapi
import datetime
import json

# Home View (Landing Page)
def home(request):
    latestData = getLatest()

    endday = latestData.date
    startday = datetime.date.today() - datetime.timedelta(28)

    schema = {'date': latestData,
              'base': 'USD',
              'target': 'ZAR',
              'dateStart': startday.strftime("%Y-%m-%d"),
              'dateEnd': endday.strftime("%Y-%m-%d") }

    return render(request, 'convert.html', { 'schema': schema, 'time_series_chart': charts.TimeSeriesChart(), })


# Convert currencies
today = datetime.date.today()
def convert(request, amount=1, target="ZAR", base="USD", convert_date=today.strftime("%Y-%m-%d")):
    curRate = lambda x, y: {'AUD': y.curencyAUD,
                   'CAD': y.curencyCAD,
                   'CHF': y.curencyCHF,
                   'CNY': y.curencyCNY,
                   'EUR': y.curencyEUR,
                   'GBP': y.curencyGBP,
                   'NZD': y.curencyNZD,
                   'ZAR': y.curencyZAR,
                   'USD': 1}[x]

    # Get the cross rate
    rate = rates.objects.order_by('-date').filter(date__lte=convert_date).first()
    crossRate = curRate(base, rate) / curRate(target, rate)

    responseDict =  {'date_long': rate.date.strftime("%A %B %-d %Y"),
                     'date': rate.date.strftime("%Y-%m-%d"),
                     'value': "{:.2f}".format(float(amount) * crossRate),
                     'crossrate': "{:.2f}".format(crossRate),
                     'crossrateinverse': "{:.2f}".format(1 / crossRate) }

    # Return Value as JSON
    return HttpResponse(json.dumps(responseDict), content_type='application/json')


# Check if we have latest rates
# Save if not in db
def getLatest():
    today = datetime.date.today()
    yesterday = datetime.date.today() - datetime.timedelta(1)

    # Get latest in db
    latest = rates.objects.order_by('-date').first()

    # If there are no records, get latest
    if latest is None:
        latest = queryApi(today)
        fullMissing()

    else:
        # Check if date is today or yesterday
        lastday = latest.date

        if lastday != today and lastday != yesterday:
            # Get latest
            latest = queryApi(today)
            fullMissing()

    return latest


# Get the rates for a date and save to datebase
def queryApi(date):
    # lambda function to check the rate exists in the fetched data
    exists = lambda x, y: y[x] if x in y else None

    # Coreapi fetches an OrderedDict
    client = coreapi.Client()
    result = client.get('https://api.fixer.io/{}?base=USD'.format(date.strftime("%Y-%m-%d")))
    latest = rates(date=datetime.datetime.strptime(result['date'] , '%Y-%m-%d'),
                curencyAUD=exists('AUD', result['rates']),
                curencyCAD=exists('CAD', result['rates']),
                curencyCHF=exists('CHF', result['rates']),
                curencyCNY=exists('CNY', result['rates']),
                curencyEUR=exists('EUR', result['rates']),
                curencyGBP=exists('GBP', result['rates']),
                curencyNZD=exists('NZD', result['rates']),
                curencyZAR=exists('ZAR', result['rates']),)
    try:
        latest.save();
    except:
        pass

    return latest


# Check for missing days
def fullMissing():
    latest = rates.objects.order_by('-date').first().date
    seriesCheck = 0
    addedCheck = 0
    while seriesCheck < 10 or addedCheck < 90:
        latest = latest + datetime.timedelta(-1)
        if latest.weekday() < 5:
            if rates.objects.order_by('-date').filter(date=latest).first():
                seriesCheck += 1
            else:
                queryApi(latest)
                seriesCheck = 0
                addedCheck += 1


# Update historic
def historic():
    count = 0
    first = rates.objects.order_by('date').first()
    while count < 7:
        count = count + 1
        day = first.date - datetime.timedelta(count)
        queryApi(day)
