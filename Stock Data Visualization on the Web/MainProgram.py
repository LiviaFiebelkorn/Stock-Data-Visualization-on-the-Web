# mainprogram.py
import Functions
from datetime import datetime
import pygal
import webbrowser
while True: 
    print("Stock Data Visualizer\n-----------------\n")

    symbol = input("Please enter the symbol for the stock: ").upper()

    while not symbol.isalnum():
        print("Invalid symbol. Please enter a valid stock symbol.")
        symbol = input("Please enter the symbol for the stock: ").upper()

    print("\nChart Types\n---------------\n1. Bar\n2. Line")
    chart_type = input("Enter the type of chart you would like (1 or 2): ")

    while chart_type not in ['1', '2']:
        print("Invalid choice. Please enter 1 or 2.")
        chart_type = input("Enter the type of chart you would like (1 or 2): ")

    print("\nPlease select the time series of the chart you would like to generate")
    print("--------------------------------------------")
    print("1. Intraday")
    print("2. Daily")
    print("3. Weekly")
    print("4. Monthly")
    time_option = input("Enter a time series option (1, 2, 3, 4): ")

    while time_option not in ['1', '2', '3', '4']:
        print("Invalid choice. Please enter 1, 2, 3, or 4.")
        time_option = input("Enter a time series option (1, 2, 3, 4): ")

    if time_option in ['2', '3', '4']:
        start_date = input("Enter the start date (YYYY-MM-DD): ")
        end_date = input("Enter the end date (YYYY-MM-DD): ")

        try:
            datetime.strptime(start_date, '%Y-%m-%d')
            datetime.strptime(end_date, '%Y-%m-%d')
        except ValueError:
            print("Invalid date format. Please use YYYY-MM-DD.")
            exit()

        if start_date > end_date:
            print("Start date cannot be after end date.")
            exit()

    if time_option == '1':
        valid_intervals = ['1', '5', '15', '30', '60']
        interval = input("Please enter the interval (options: 1, 5, 15, 30, 60): ")

        while interval not in valid_intervals:
            print("Invalid interval. Please enter one of the following intervals: 1, 5, 15, 30, 60")
            interval = input("Please enter the interval: ")

        data = Functions.TIME_SERIES_INTRADAY(symbol, interval)
        time_series_key = f'Time Series ({interval}min)'
        time_series_data = data.get(time_series_key, {}) if data else None
        data_filter = time_series_data
    elif time_option == '2':
        data = Functions.TIME_SERIES_DAILY(symbol)
        data_key = next((key for key in data.keys() if "Time Series" in key), None)
        if data_key:
            time_series_data = data[data_key]
            data_filter = {date: values for date, values in time_series_data.items() if start_date <= date <= end_date}
        else:
            print("No data found")
            exit()
    elif time_option == '3':
        data = Functions.TIME_SERIES_WEEKLY(symbol)
        data_key = next((key for key in data.keys() if "Time Series" in key), None)
        if data_key:
            time_series_data = data[data_key]
            data_filter = {date: values for date, values in time_series_data.items() if start_date <= date <= end_date}
        else:
            print("No data found")
            exit()
    elif time_option == '4':
        data = Functions.TIME_SERIES_MONTHLY(symbol)
        data_key = next((key for key in data.keys() if "Time Series" in key), None)
        if data_key:
            time_series_data = data[data_key]
            data_filter = {date: values for date, values in time_series_data.items() if start_date <= date <= end_date}
        else:
            print("No data found")
            exit()

    if chart_type == "1":
        chart = pygal.Bar(x_label_rotation = 45)
    elif chart_type == "2":
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

        for date in sorted(data_filter.keys()):
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
    if time_option == '1':
        chart.title = f"Stock data for {symbol} ({interval}min)"
        chart.x_labels_major_every = 30
    else:
        chart.title = f"Stock data for {symbol}: {start_date} to {end_date}"

    chart_file = "chart.html"
    chart.render_to_file(chart_file)
    print(f"chart: {chart_file}")
    webbrowser.open(chart_file)

    repeat = input("Would you like to visualize another stock?(y/n)")
    if repeat != 'y':
        break
