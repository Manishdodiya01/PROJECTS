import flask
import pandas as pd
from flask import Flask , render_template , request
from xgboost import XGBClassifier
import joblib

model = joblib.load('artifacts/XGB_MODEL.joblib')
preprocessor = joblib.load('artifacts/Preprocessor')

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/result', methods=['POST'])
def result():
    if request.method == 'POST':

        form_data = request.form
        
        input_data = {
            'months_as_customer': int(form_data['months_as_customer']),
            'age': int(form_data['age']),
            'policy_number': int(form_data['policy_number']),
            'policy_state': form_data['policy_state'],
            'policy_csl': form_data['policy_csl'],
            'policy_deductable': int(form_data['policy_deductable']),
            'policy_annual_premium': float(form_data['policy_annual_premium']),
            'umbrella_limit': int(form_data['umbrella_limit']),
            'insured_sex': form_data['insured_sex'],
            'insured_education_level': form_data['insured_education_level'],
            'insured_occupation': form_data['insured_occupation'],
            'insured_hobbies': form_data['insured_hobbies'],
            'insured_relationship': form_data['insured_relationship'],
            'capital-gains': int(form_data['capital-gains']),
            'capital-loss': int(form_data['capital-loss']),
            'incident_type': form_data['incident_type'],
            'collision_type': form_data['collision_type'],
            'incident_severity': form_data['incident_severity'],
            'authorities_contacted': form_data['authorities_contacted'],
            'incident_state': form_data['incident_state'],
            'incident_city': form_data['incident_city'],
            'incident_hour_of_the_day': int(form_data['incident_hour_of_the_day']),
            'number_of_vehicles_involved': int(form_data['number_of_vehicles_involved']),
            'property_damage': form_data['property_damage'],
            'bodily_injuries': int(form_data['bodily_injuries']),
            'witnesses': int(form_data['witnesses']),
            'police_report_available': form_data['police_report_available'],
            'total_claim_amount': int(form_data['total_claim_amount']),
            'injury_claim': int(form_data['injury_claim']),
            'property_claim': int(form_data['property_claim']),
            'vehicle_claim': int(form_data['vehicle_claim']),
            'auto_make': form_data['auto_make'],
            'auto_year': int(form_data['auto_year']),
            'policy_bind_year': int(form_data['policy_bind_year']),
            'policy_bind_month': int(form_data['policy_bind_month']),
            'policy_bind_day': int(form_data['policy_bind_day']),
            'incident_year': int(form_data['incident_year']),
            'incident_month': int(form_data['incident_month']),
            'incident_day': int(form_data['incident_day'])
        }

        input_df = pd.DataFrame([input_data])
        preprocessed_input_data = preprocessor.transform(input_df)
        prediction = model.predict(preprocessed_input_data)

        return render_template('result.html', prediction=prediction[0])
    

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)

