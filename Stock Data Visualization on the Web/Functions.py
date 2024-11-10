import requests
import pygal
import lxml
import os
from flask import Flask, render_template, request, url_for, flash, redirect, abort, send_from_directory

apikey = "FVQDMTI5GIVCHLQT"

def TIME_SERIES_INTRADAY(symbol, interval):

    url = f'https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol={symbol}&interval={interval}min&apikey={apikey}'
    r = requests.get(url)
    data = r.json()
    for i in r:
        print(i)
    return data

def TIME_SERIES_DAILY(symbol):

    url = f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&apikey={apikey}'
    r = requests.get(url)
    data = r.json()
    return data

def TIME_SERIES_WEEKLY(symbol):
    url = f'https://www.alphavantage.co/query?function=TIME_SERIES_WEEKLY&symbol={symbol}&apikey={apikey}'
    r = requests.get(url)
    data = r.json()
    return data


def TIME_SERIES_MONTHLY(symbol):

    url = f'https://www.alphavantage.co/query?function=TIME_SERIES_MONTHLY&symbol={symbol}&apikey={apikey}'
    r = requests.get(url)
    data = r.json()
    return data


def MAKE_CHART(data_filter, chart_type, symbol, interval=None, start_date=None, end_date=None):
    print("Data Filter:", data_filter)  # Debugging line
    
    if chart_type == "bar":
        chart = pygal.Bar(x_label_rotation = 45)
    elif chart_type == "line":
        chart = pygal.Line(x_label_rotation = 45)
    else:
        print("Invalid chart type selected")
        exit()
        
    if not data_filter:
        print("No data found")
    else:
        dates = []
        open_prices = []
        high_prices = [] 
        low_prices =[]
        close_prices =[]

        if start_date:
            start_date = start_date.strip()
        if end_date:
            end_date = end_date.strip()

        for date in sorted(data_filter.keys()):

            if (start_date and date < start_date) or (end_date and date > end_date):
                continue

            items = data_filter[date]
            dates.append(date)
            open_prices.append(float(items['1. open']))
            high_prices.append(float(items['2. high']))
            low_prices.append(float(items['3. low']))
            close_prices.append(float(items['4. close']))

        chart.add("Open", open_prices)
        chart.add("High", high_prices)
        chart.add("Low", low_prices)
        chart.add("Close", close_prices)
    chart.x_labels = dates
    if interval:
        chart.title = f"Stock data for {symbol} ({interval}min)"
        chart.x_labels_major_every = 30
    else:
        chart.title = f"Stock data for {symbol}: {start_date} to {end_date}"

    chart_file = os.path.join('static', 'chart.html')
    chart.render_to_file(chart_file)
    return url_for('static', filename='chart.html')
