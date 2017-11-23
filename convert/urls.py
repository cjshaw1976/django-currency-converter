from django.conf.urls import url
from . import views
from . import charts

from jchart.views import ChartView

urlpatterns = [
    url(r'^$', views.home, name='home'),

    url(r'^convert/(?P<amount>\d+(?:\.\d+)?)/(?P<target>\w+)/(?P<base>\w+)/(?P<convert_date>\d{4}-\d{2}-\d{2})/$',
        views.convert, name="convert"),

    url(r'^charts/time_series_chart/(?P<target>\w+)/$',
        ChartView.from_chart(charts.TimeSeriesChart()),
        name='time_series_chart'),

    url(r'^charts/time_series_chart/(?P<target>\w+)/(?P<start_date>\d{4}-\d{2}-\d{2})/$',
        ChartView.from_chart(charts.TimeSeriesChart())),

    url(r'^charts/time_series_chart/(?P<target>\w+)/(?P<base>\w+)/(?P<start_date>\d{4}-\d{2}-\d{2})/$',
        ChartView.from_chart(charts.TimeSeriesChart())),

    url(r'^charts/time_series_chart/(?P<target>\w+)/(?P<start_date>\d{4}-\d{2}-\d{2})/(?P<end_date>\d{4}-\d{2}-\d{2})/$',
        ChartView.from_chart(charts.TimeSeriesChart())),

    url(r'^charts/time_series_chart/(?P<target>\w+)/(?P<base>\w+)/(?P<start_date>\d{4}-\d{2}-\d{2})/(?P<end_date>\d{4}-\d{2}-\d{2})/$',
        ChartView.from_chart(charts.TimeSeriesChart())),
]
