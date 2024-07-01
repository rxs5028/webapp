#!/usr/bin/env python3

from flask import Flask, request, render_template
from datetime import datetime, timedelta
import json
import os

app = Flask(__name__)

flights = None

def load_flights():
    global flights
    data_path = os.path.join(app.root_path, 'data', 'flights.json')
    with open(data_path) as f:
        flights = json.load(f)

load_flights()

@app.route("/")
def main():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    airport = request.form['airport']
    month = request.form['month']
    days = int(request.form['days'])
    min_cost = float('inf')
    best = None

    for to_date in flights["to_AUA"]:
        from_date = (datetime.strptime(to_date, '%Y-%m-%d') + timedelta(days=days)).strftime('%Y-%m-%d')
        if from_date in flights["from_AUA"]:
            to_flights = [f for f in flights["to_AUA"][to_date] if f["origin"] == airport]
            from_flights = [f for f in flights["from_AUA"][from_date] if f["destination"] == airport]

            for to_flight in to_flights:
                for from_flight in from_flights:
                    total_cost = to_flight["cost"] + from_flight["cost"]
                    if total_cost < min_cost:
                        min_cost = total_cost
                        from_airline = from_flight["airline"]
                        to_airline = to_flight["airline"]
                        best = {
                           "to_date": to_date,
                           "from_date": from_date,
                           "to_flight": to_flight,
                           "from_flight": from_flight,
                           "total_cost": total_cost,
                           "from_airline": from_airline,
                           "to_airline": to_airline
                        }

    print(f"Airport: {airport}")
    print(f"Month: {month}")
    print(f"Days: {days}")
    total_cost = best["total_cost"]
    print(f"Total cost: {total_cost}")
    from_airline = best["from_flight"]["airline"]
    print(f"From airline: {from_airline}")

    to_date = best["to_date"]
    from_date = best["from_date"]
    #to_flight = best["to_flight"]["origin"]
    #from_flight = best["from_flight"]["origin"]
    to_airline = best["to_flight"]["airline"]
    from_airline = best["from_flight"]["airline"]
    total_cost = best["total_cost"]

    return('Your best flight is $' + str(total_cost) + ' from ' + to_date + '('+ airport + ') on ' + to_airline + ' to ' + from_date + '(' + 'AUA' + ') on ' + from_airline + '!')

@app.route("/echo")
def echo():
    return '''
    <form action="/echo_user_input" method="POST">
         <input name="user_input">
         <input type="submit" value="Submit!">
    </form>
    '''

@app.route("/echo_user_input", methods=["POST"])
def echo_input():
    input_text = request.form.get("user_input", "")
    return "You entered: " + input_text
