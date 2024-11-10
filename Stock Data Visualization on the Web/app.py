import sqlite3
import pandas
from flask import Flask, render_template, request, url_for, flash, redirect, abort, send_from_directory
from Functions import *
import os

# make a Flask application object called app
app = Flask(__name__)
app.config["DEBUG"] = True
app.config['SECRET_KEY'] = 'your secret key'


# Function to open a connection to the database.db file
def get_db_connection():
    # create connection to the database
    conn = sqlite3.connect('database.db')
    
    # allows us to have name-based access to columns
    # the database connection will return rows we can access like regular Python dictionaries
    conn.row_factory = sqlite3.Row

    #return the connection object
    return conn

#function to retrieve a post from the database
def get_post(post_id):
    conn = get_db_connection()
    post = conn.execute('SELECT * FROM posts WHERE id = ?', (post_id,)).fetchone()
    conn.close()

    if post is None:
        abort(404)
    return post

# use the app.route() decorator to create a Flask view function called index()
@app.route('/')
def index():
    # #Get a connection to the database
    # conn = get_db_connection()

    # #execute a query to read all posts from the posts table in the database
    # posts = conn.execute('SELECT * FROM posts').fetchall()

    # #close the connection
    # conn.close()

    #send the posts to the index.html template to be displayed
    symbols = loadsymbols()

    return render_template('index.html', symbols=symbols)


# route to create a post
@app.route('/create/', methods=('GET', 'POST'))
def create():
    #determine if the page is being requested with a POST or GET request
    if request.method == 'POST':
        #get the title and content that was submitted
        title = request.form['title']
        content = request.form['content']

        #display an error if title or content is not submitted
        #else make a database connection and insert the blog post content
        if not title:
            flash("Title is required")
        elif not content:
            flash('Content is required')
        else:
            conn = get_db_connection()
            #insert data into database
            conn.execute('INSERT INTO posts (title, content) VALUES (?, ?)', (title,content))
            conn.commit()
            conn.close()
            return redirect(url_for('index'))

    return render_template('create.html')

#create a route to edit a post. Load page with get or post method
#pass the post id as a url parameter
@app.route('/<int:id>/edit', methods=('GET', 'POST'))
def edit(id):
    #get the post from the database with a select query for the post with that id
    post = get_post(id)

    #determine if the page was requested with GET or POST
    
    #If POST, process the form data. Get the data and validate it. Update the post and redirect to the homepage
    if request.method == 'POST':
        #get the title and content
        title = request.form['title']
        content = request.form['content']
    
       #if not title or content, flash an error message
        if not title:
            flash('Title is required')
        elif not content:
            flash('Content is required')
        else:
            conn = get_db_connection()
            conn.execute('UPDATE posts SET title = ?, content = ? WHERE id = ?', (title, content, id))
            conn.commit()
            conn.close()

            #redirect to the home page
            return redirect(url_for('index'))

    #If GET then display page
    return render_template('edit.html', post=post)
@app.route('/stock_data', methods=['POST'])
def stock_data():
    symbol = request.form['symbol']
    timeseries = request.form['time_series']
    charttype = request.form['charttype']
    startdate = request.form['startdate']
    enddate = request.form['enddate']


    if timeseries == 'intraday':
        data = TIME_SERIES_INTRADAY(symbol, interval = 5)
        key = 'Time Series (5min)'
    elif timeseries == 'daily':
        data = TIME_SERIES_DAILY(symbol)
        key = 'Time series (Daily)'
    elif timeseries == 'weekly':
        data = TIME_SERIES_WEEKLY(symbol)
        key = 'Weekly Time Series'
    elif timeseries == 'monthly':
        data = TIME_SERIES_MONTHLY(symbol)
        key = 'Monthly Time Series'

    dataforchart = data.get(key, {})

    chart_file = MAKE_CHART(dataforchart, charttype, symbol, start_date=startdate, end_date = enddate)
    symbols = loadsymbols()
    return render_template('base.html', chart_file=chart_file)
    


#create a route to delete a post
#delete page will only be processed with a POST method
#the post id is the url parameter
@app.route('/<int:id>/delete', methods=('POST',))
def delete(id):
    #get the post 
    post = get_post(id)

    #connect to the database
    conn = get_db_connection()

    #execute a delete query
    conn.execute('DELETE from posts WHERE id = ?', (id,))

    #commit and close the connection
    conn.commit()
    conn.close()

    #flash a success message
    flash('"{}" was successfully deleted!'.format(post['title']))

    #redirect to the homepage
    return redirect(url_for('index'))

def loadsymbols():
    file = pandas.read_csv('stocks.csv')
    symbols = file['Symbol']
    symbolslist = symbols.tolist()
    return symbolslist

    

app.run(host="0.0.0.0")