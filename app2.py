from flask import Flask, render_template, request, redirect, url_for
import joblib
import numpy as np
import pickle
import sklearn

app = Flask(__name__)

# Load the trained model
model = joblib.load('bank.pkl')

@app.route('/')
def index():
    return render_template('index.html')
@app.route('/aboutus')
def aboutus():
    return render_template('aboutus.html')

@app.route('/predict', methods=['GET', 'POST'])
def predict():
    if request.method == 'POST':
        try:
            # Get form data
            amount = float(request.form['amount'])
            nameOrig = request.form['nameOrig']
            oldbalanceOrg = float(request.form['oldbalanceOrg'])
            newbalanceOrg = float(request.form['newbalanceOrg'])
            oldbalanceDest = float(request.form['oldbalanceDest'])
            newbalanceDest = float(request.form['newbalanceDest'])

            # Prepare input for prediction
            input_data = np.array([amount, oldbalanceOrg, newbalanceOrg, oldbalanceDest, newbalanceDest]).reshape(1, -1)

            # Make prediction
            global prediction
            prediction = model.predict(input_data)
            return redirect(url_for('show_prediction'))
        except Exception as e:
            print(str(e))
            # Handle error scenario or redirect to error page
            return redirect(url_for('error_page'))
    return redirect(url_for('show_prediction'))  # Redirect to index if GET request

@app.route('/fraud')
def show_prediction():
    return render_template('fraud.html')

@app.route('/error')
def error_page():
    return render_template('error.html')

if __name__ == '__main__':
    app.run(debug=True)
