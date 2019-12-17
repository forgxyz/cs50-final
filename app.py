import os.path
import calendar
import csv
import datetime

from cs50 import SQL
from flask import Flask, jsonify, redirect, render_template, request, session
from flask_session import Session
from html import escape
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

import helpers

# configure application
app = Flask(__name__)

# auto-reload templates on any change
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# global variables
CSVFILE = "data/sample_tx.csv"

@app.route('/')
def index():
    # return render_template("index.html")
    return render_template('record.html')


@app.route('/record', methods=['GET', 'POST'])
def record():

    if request.method == 'POST':
        # record input on submit

        # if file does not exist, ensure the header is written
        exists = os.path.isfile(CSVFILE)

        # open, or create, a response log and write the user input
        with open(CSVFILE, 'a+', newline ='') as csvfile:
            fieldnames = ['amount', 'date', 'categoryid', 'method', 'comment']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames, restval=' ')

            if not exists:
                writer.writeheader()

            writer.writerow({
                'amount': request.form['amount'],
                'date': request.form['date'],
                'categoryid': request.form.get('category'),
                'method': request.form.get('method'),
                'comment': request.form['comment']
                })

        return render_template("success.html")
    
    return render_template("record.html")


@app.route('/responses')
def responses():
    form_responses = ''

    # open and read the csv file
    with open(CSVFILE, newline='') as csvfile:
        reader = csv.DictReader(csvfile)

        for line in reader:
        # wrap each new line in <tr>
            form_responses += "<tr>"

            for key, value in line.items():
                # wrap each value in <td>
                if key == 'amount':
                    form_responses += f"<td>{helpers.usd(value)}</td>"
                elif key == 'categoryid':
                    form_responses += f"<td>{helpers.CategoryID[value]}</td>"
                else:
                    form_responses += f"<td>{value}</td>"
            # add edit and delete buttons and end the table row
            form_responses += """
                <td><button onclick="alert('Coming Soon!')" class="btn btn-secondary">Edit</button></td>
                <td><button onclick="alert('Coming Soon!')" class="btn btn-secondary">Delete</button></td>
                </tr>"""

    # post to table in responses.html
    return render_template('responses.html', form_responses=form_responses)


@app.route('/summary', methods=['GET', 'POST'])
def summary():
    if request.args.get('month'):
        monthnum = int(request.args.get('month'))

    else:
        monthnum = datetime.date.today().month

    month = calendar.month_name[monthnum]
    monthtx = []
    cattotal, total = 0, 0
    tabledata = ''

    with open(CSVFILE, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        
        # isolate transactions for the selected month
        for line in reader:
            if monthnum == datetime.datetime.strptime(line['date'] , '%Y-%m-%d').month:
                total += float(line['amount'])
                monthtx.append({'categoryid': line['categoryid'], 'amount': line['amount']})
        
        # sum transactions by category and post 
        for key, value in helpers.CategoryID.items():
            for row in monthtx:
                if int(row['categoryid']) == int(key):
                    cattotal += float(row['amount'])
            if cattotal != 0:
                pct = round(round((cattotal / total), 3) * 100, 1)
                tabledata += f"<tr><td>{value}</td><td>{helpers.usd(cattotal)}</td><td>{pct}%</td></tr>"
                cattotal = 0
        
        tabledata += f"<tr class='table-secondary'><td>Total Spending for {month}</td><td>{helpers.usd(total)}</td><td>100%</td>"

    return render_template("summarytable.html", month=month, tabledata=tabledata)
