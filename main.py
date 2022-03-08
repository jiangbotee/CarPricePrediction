#
# from flask import Flask, render_template, request
# import jsonify
# import requests
# import pickle
# import numpy as np
# import pandas as pd
# import joblib
# import sklearn
# from sklearn.preprocessing import StandardScaler
# app = Flask(__name__)
# model = pickle.load(open('linearRegression.pkl', 'rb'))
# df_cleaned = pd.read_csv('cleanedDF_no_outliers.csv').iloc[:,:-1]
# s = joblib.load('standardScaler.joblib')
# @app.route('/',methods=['GET'])
# def Home():
#     return render_template('index.html')
#
#
# standard_to = StandardScaler()
# @app.route("/predict", methods=['POST'])
#
#
# def get_brand(bd):
#     american = ['Chevrolet','GMC','Pontiac','Chrysler','Ford','Cadillac','Tesla','Jeep','Ram','Lincoln','Saturn','Dodge','Buick']
#     german = ['Volkswagen','BMW','Porsche','Audi','Mercedes-Benz','MINI']
#     japanese = ['Acura','Honda','Toyota','Mazda','Nissan','Lexus','Subaru','Mitsubishi','Suzuki','Infiniti']
#     korean = ['Hyundai','Kia','Genesis']
#     british = ['Jaguar','Land Rover'],
#     italian = ['Ferrari','Fiat','alfaromeo','Maserati']
#     if bd in american:
#         country = 'american'
#     elif bd in german:
#         country = 'german'
#     elif bd in japanese:
#         country = 'japanese'
#     elif bd in korean:
#         country = 'korean'
#     elif bd in british:
#         country = 'british'
#     elif bd in italian:
#         country = 'italian'
#     else:
#         country = 'other'
#     return country
#
#
# def one_hot(row):
#     df = df_cleaned
#     df.iloc[-1] = pd.Series(row)
#     df_oh = pd.get_dummies(df, drop_first=True)
#     df_oh = df_oh.drop(columns=['carfax_link_New_Car'])
#     return df_oh.iloc[-1]
#
#
#
# def predict():
#     df_cleaned = pd.read_csv('cleanedDF_no_outliers.csv')
#     Fuel_Type_Diesel=0
#     if request.method == 'POST':
#         brand = get_brand(request.form['brand'])
#         vehicle_age = 2022-int(request.form['year'])
#         mileage=np.log(float(request.form['mileage']))
#         color = request.form['color']
#         condition = request.form['condition']
#         body_type = request.form['body_type']
#         wheel_config = request.form['wheel_config']
#         cylinders = int(request.form['cylinders'])
#         transmission = request.form['transmission']
#         carfax_link = request.form['carfax_link']
#         dealer_address = request.form['area']
#
#         row = [brand, color, condition, body_type, wheel_config,
#                transmission, mileage, carfax_link, dealer_address, cylinders,
#                vehicle_age]
#
#         oh_row = one_hot(row)
#
#         inp = s.transform([oh_row])
#
#         prediction=model.predict(inp)
#         output=round(np.exp(prediction[0]),2)
#         if output<0:
#             return render_template('index.html',prediction_texts="Sorry you cannot sell this car")
#         else:
#             return render_template('index.html',prediction_text="You Can Sell The Car at {}".format(output))
#     else:
#         return render_template('index.html')
#
# if __name__=="__main__":
#     app.run(debug=True)


from flask import Flask, render_template, request, redirect, url_for
import jsonify
import requests
import pickle
import numpy as np
import pandas as pd
import joblib
import sklearn
from sklearn.preprocessing import StandardScaler
app = Flask(__name__)
model = pickle.load(open('linearRegression.pkl', 'rb'))
df_cleaned = pd.read_csv('cleanedDF_no_outliers.csv').iloc[:,:-1]
s = joblib.load('standardScaler.joblib')
@app.route('/',methods=['GET'])
def Home():
    return render_template('index.html')

def get_brand(bd):
    american = ['Chevrolet','GMC','Pontiac','Chrysler','Ford','Cadillac','Tesla','Jeep','Ram','Lincoln','Saturn','Dodge','Buick']
    german = ['Volkswagen','BMW','Porsche','Audi','Mercedes-Benz','MINI']
    japanese = ['Acura','Honda','Toyota','Mazda','Nissan','Lexus','Subaru','Mitsubishi','Suzuki','Infiniti']
    korean = ['Hyundai','Kia','Genesis']
    british = ['Jaguar','Land Rover'],
    italian = ['Ferrari','Fiat','alfaromeo','Maserati']
    if bd in american:
        country = 'american'
    elif bd in german:
        country = 'german'
    elif bd in japanese:
        country = 'japanese'
    elif bd in korean:
        country = 'korean'
    elif bd in british:
        country = 'british'
    elif bd in italian:
        country = 'italian'
    else:
        country = 'other'
    return country


def one_hot(row):
    df = df_cleaned
    df.iloc[-1] = pd.Series(row)
    df_oh = pd.get_dummies(df, drop_first=True)
    df_oh = df_oh.drop(columns=['carfax_link_New_Car'])
    return df_oh.iloc[-1]
standard_to = StandardScaler()
@app.route("/predict", methods=['POST'])
def predict():
    Fuel_Type_Diesel=0
    if request.method == 'POST':
        Fuel_Type_Diesel=0
        if request.method == 'POST':
            brand = get_brand(request.form['brand'])
            md = request.form['model']
            vehicle_age = 2022-int(request.form['year'])
            mileage=np.log(float(request.form['mileage']))
            color = request.form['color']
            condition = request.form['condition']
            body_type = request.form['body_type']
            wheel_config = request.form['wheel_config']
            cylinders = int(request.form['cylinders'])
            transmission = request.form['transmission']
            carfax_link = request.form['carfax_link']
            dealer_address = request.form['area']

            row = [brand, color, condition, body_type, wheel_config,
                   transmission, mileage, carfax_link, dealer_address, cylinders,
                   vehicle_age]

            oh_row = one_hot(row)

            inp = s.transform([oh_row])

            prediction=model.predict(inp)
            output=round(np.exp(prediction[0]),2)
        if output<0:
            return render_template('index.html',prediction_texts="Sorry you cannot sell this car")
        else:
            outstr = "You can sell your "+str(int(request.form['year']))+" "+md + " "+str(request.form['brand'])+" for $"+str(output)
            return redirect(url_for("result", rst=outstr))
            # return render_template('index.html',prediction_text=outstr)
    else:
        return render_template('index.html')
@app.route("/<rst>")
def result(rst):
    return f"<h1>{rst}</h1>"

if __name__=="__main__":
    app.run(debug=True)
