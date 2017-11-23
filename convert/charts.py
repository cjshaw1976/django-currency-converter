from jchart import Chart
from jchart.config import Axes, DataSet, rgba

from .models import rates

import datetime

# http://www.chartjs.org for chart options
class TimeSeriesChart(Chart):
    chart_type = 'line'
    scales = {
        'xAxes': [Axes(type='time', position='bottom',)],
    }

    legend = {
            'display': False,
    }

    title = {
            'display': True,
            'text': ''
    }

    end_date=datetime.date.today()
    start_date=datetime.date.today() - datetime.timedelta(365)


    def get_datasets(self, target='ZAR', base='USD', start_date=start_date.strftime("%Y-%m-%d"), end_date=end_date.strftime("%Y-%m-%d")):

        # Set the title
        self.title = {
                'display': True,
                'text': '{} to {} chart between {} and {}.'.format(base, target, start_date, end_date)
        }

        # Use a lambda for a switch statement
        curRate = lambda x, y: {'AUD': y.curencyAUD,
                       'CAD': y.curencyCAD,
                       'CHF': y.curencyCHF,
                       'CNY': y.curencyCNY,
                       'EUR': y.curencyEUR,
                       'GBP': y.curencyGBP,
                       'NZD': y.curencyNZD,
                       'ZAR': y.curencyZAR,
                       'USD': 1}[x]

        historic = rates.objects.filter(date__range=[start_date, end_date]).order_by('-date')

        # Use list comprehension to get the data
        data = [{'y': curRate(target, result) / curRate(base, result), 'x': result.date} for result in historic]

        return [DataSet(
            type='line',
            label='Time Series',
            data=data,
            borderColor='#0000ff',
            pointRadius=0,
            borderWidth=1,
            backgroundColor='rgba(0, 0, 255, 0.1)',

        )]
