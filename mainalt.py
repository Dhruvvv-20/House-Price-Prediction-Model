from flask import Flask, render_template,request
import pandas as pd
import pickle


def num_to_indian_words(number): 
    words = ["", "One", "Two", "Three", "Four", "Five", "Six", "Seven", "Eight", "Nine", "Ten",
             "Eleven", "Twelve", "Thirteen", "Fourteen", "Fifteen", "Sixteen", "Seventeen", "Eighteen", "Nineteen"]
    tens_words = ["", "", "Twenty", "Thirty", "Forty", "Fifty", "Sixty", "Seventy", "Eighty", "Ninety"]

    if number < 20:
        return words[number]
    elif number < 100:
        return tens_words[number // 10] + (" " + words[number % 10] if (number % 10 != 0) else "")
    elif number < 1000:
        return words[number // 100] + " Hundred" + (" " + num_to_indian_words(number % 100) if (number % 100 != 0) else "")
    elif number < 100000:
        return num_to_indian_words(number // 1000) + " Thousand" + (" " + num_to_indian_words(number % 1000) if (number % 1000 != 0) else "")
    elif number < 10000000:
        return num_to_indian_words(number // 100000) + " Lakh" + (" " + num_to_indian_words(number % 100000) if (number % 100000 != 0) else "")
    else:
        return num_to_indian_words(number // 10000000) + " Crore" + (" " + num_to_indian_words(number % 10000000) if (number % 10000000 != 0) else "")


app= Flask(__name__)
data = pd.read_csv('Cleaned_data.csv')
pipe = pickle.load(open("RidgeModel.pkl", 'rb'))


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    location = request.form.get('location')
    bhk = float(request.form.get('bhk'))
    bath = float(request.form.get('bath'))
    sqft = request.form.get('total_sqft')

    input_data = pd.DataFrame([[location,sqft,bath,bhk]],columns=['location', 'total_sqft','bath','bhk'])
    input_data['Unnamed: 0'] = 0
    prediction = pipe.predict(input_data)[0] * 100000
    formatted_prediction = "{:,.2f}".format(prediction)
    worded_prediction = num_to_indian_words(int(prediction))
    
    prediction_string = f"₹ {formatted_prediction} ({worded_prediction} Rupees)"
    return prediction_string


if __name__ == "__main__":
    app.run(debug=True,port=5001)
