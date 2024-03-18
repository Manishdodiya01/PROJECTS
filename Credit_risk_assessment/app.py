from flask import Flask , render_template , request
import joblib
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.ensemble import AdaBoostClassifier , RandomForestClassifier , VotingClassifier
from sklearn.pipeline import Pipeline , make_pipeline
from sklearn.model_selection import GridSearchCV , RandomizedSearchCV , StratifiedKFold
from xgboost import XGBClassifier
from catboost import CatBoostClassifier
from sklearn.preprocessing import StandardScaler , MinMaxScaler , LabelEncoder , OneHotEncoder
from sklearn.metrics import confusion_matrix , classification_report , accuracy_score , f1_score
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer


preprocessor = joblib.load('artifacts/preprocessor.joblib')
model = joblib.load('artifacts/xgb_model.joblib')

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home_.html')

@app.route('/result',methods=['POST'])
def result():
    if request.method == 'POST':
        person_age = int(request.form['age'])
        person_income = int(request.form['income'])
        person_home_ownership = request.form['home_ownership']
        person_emp_length = float(request.form['emp_length'])
        loan_intent = request.form['loan_intent']
        loan_grade = request.form['loan_grade']
        loan_amnt = int(request.form['loan_amnt'])
        loan_int_rate = float(request.form['loan_int_rate'])
        cb_person_default_on_file = request.form['cb_person_default_on_file']
        cb_person_cred_hist_length = int(request.form['cb_person_cred_hist_length'])

        input_data = {
            'person_age': [person_age],
            'person_income': [person_income],
            'person_home_ownership': [person_home_ownership],
            'person_emp_length': [person_emp_length],
            'loan_intent': [loan_intent],
            'loan_grade': [loan_grade],
            'loan_amnt': [loan_amnt],
            'loan_int_rate': [loan_int_rate],
            'cb_person_default_on_file': [cb_person_default_on_file],
            'cb_person_cred_hist_length': [cb_person_cred_hist_length]
        }
        input_data = pd.DataFrame(input_data)

        preprocessed_input_data = preprocessor.transform(input_data)

        # Make Predicion
        prediction = model.predict(preprocessed_input_data)
        
        return render_template('result.html', prediction=prediction[0])
    

if __name__=="__main__":
    app.run(host="0.0.0.0")  