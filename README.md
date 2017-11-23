# django-currency-converter
This Django project collect, stores and displays current and historic data foreign exchange rates published by the European Central Bank for a selected basket of currencies. Currencies can be converted at historic rates and a chart displays the rates between two currencies for a selected period.

Collecting Data.
Rates are collected from the api ‘https://api.fixer.io/’, using coreapi. A dataset consisting of the date and selected currencies are saved into the sqlite database.

Displaying a chart.
The django-jchart app is used to effectively and quickly render charts. You may view charts of rates for any two currencies between any two dates. The charts are called asynchronously so there is no need to refresh the page.

Displaying a rate calculation.
An amount may be converted from one currency to another at the current date or a historic date. Again this is done asynchronously so the calculation is displayed without refreshing the page.

Skills utilized.

Backend:

    Python 3.6
    Django 1.11.7
    coreapi

Frontend:

    JQuery 3.1
    Bootstrap 3.3
    Chart.js 2.4
