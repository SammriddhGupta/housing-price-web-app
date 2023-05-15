from flask import Flask, render_template, request, flash

import json
from predict import predict
app = Flask(__name__)

app.secret_key = 'asdf'

AVERAGE_SQUARE_FOOTAGE = 1827
AVERAGE_PRICE_PER_SQUARE_FOOT = 195

NON_DISCLOSURE_STATES = ['AK', 'ID', 'KS', 'LA', 'MI', 'MO', 'MN', 'MT', 'NM', 'ND', 'TX', 'UT', 'WY']

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        form_dict = request.form
        try:
            if(request.form['state']) in NON_DISCLOSURE_STATES:
              flash('You are asking for a prediction about a house in a non-disclosure state, so take this prediction with a grain of salt')

            prediction = predict(form_dict)
        except Exception as e:
            print(e)
            flash('We weren\'t able to make a prediction. Maybe check your input and try again?')
            prediction = None
    else:
        form_dict = {}
        prediction = None
        
    states = json.load(open('states.json'))
    print(form_dict)
    return render_template('index.html', states=states, prediction=prediction, form_dict=form_dict)

if __name__ == '__main__':
    #app.run(host='0.0.0.0',port=1234, debug=True)
    from waitress import serve
    serve(app, host="0.0.0.0", port=8080)
