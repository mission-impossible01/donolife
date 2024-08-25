from flask import Flask, request, jsonify, render_template,redirect,request,url_for
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, IntegerField, SubmitField, BooleanField, SelectField, TextAreaField
from wtforms.validators import DataRequired, Length, Optional, NumberRange

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key'  # Replace with a secure key

# Example data
donors = [
    {"name": "Donor1", "blood_group": "A+", "units": 5, "has_transmissible_disease": False, "health_conditions": []},
    {"name": "Donor2", "blood_group": "O-", "units": 3, "has_transmissible_disease": True, "health_conditions": ["mild cold"]},
    {"name": "Donor3", "blood_group": "B+", "units": 4, "has_transmissible_disease": False, "health_conditions": ["heart disease"]}
]

recipients = [
    {"name": "Recipient1", "blood_group": "A+", "units": 2},
    {"name": "Recipient2", "blood_group": "O-", "units": 1},
    {"name": "Recipient3", "blood_group": "B+", "units": 4}
]

class DonorForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(max=100)])
    age = IntegerField('Age', validators=[DataRequired(), NumberRange(min=18, max=100)])
    blood_group = SelectField('Blood Group', choices=[('A+', 'A+'), ('A-', 'A-'), ('B+', 'B+'), ('B-', 'B-'), ('AB+', 'AB+'), ('AB-', 'AB-'), ('O+', 'O+'), ('O-', 'O-')], validators=[DataRequired()])
    units_available = IntegerField('Units Available', validators=[DataRequired(), NumberRange(min=1)])
    has_transmissible_disease = BooleanField('Has Transmissible Disease')
    health_conditions = TextAreaField('Health Conditions (Comma Separated)', validators=[Optional(), Length(max=200)])
    submit = SubmitField('Submit')

class RecipientForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(max=100)])
    blood_group = SelectField('Blood Group', choices=[('A+', 'A+'), ('A-', 'A-'), ('B+', 'B+'), ('B-', 'B-'), ('AB+', 'AB+'), ('AB-', 'AB-'), ('O+', 'O+'), ('O-', 'O-')], validators=[DataRequired()])
    units_needed = IntegerField('Units Needed', validators=[DataRequired(), NumberRange(min=1)])
    submit = SubmitField('Submit')

@app.route('/')
def home():
    return render_template('web.html')

@app.route('/more_info')
def more_info():
    return render_template('benefit.html')

@app.route('/match')
def match():
    return render_template('index.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/Question')
def Question():
    return render_template('faq.html')

@app.route('/Donate')
def Donate():
    return render_template('donate.html')

@app.route('/thankyou')
def thank_you():
    return render_template('thankyou.html')


@app.route('/donor', methods=['POST', 'GET'])
def donor():
    if request.method == 'POST':
        # Process the form data here
        donor_data = {
            'name': request.form.get('donorName'),
            'dob': request.form.get('donorDob'),
            'phone': request.form.get('donorPhone'),
            'email': request.form.get('donorEmail'),
            'address': request.form.get('donorAddress'),
            'health_status': request.form.get('donorHealthStatus'),
            'medical_conditions': request.form.get('donorMedicalConditions'),
            'medications': request.form.get('donorMedications'),
            'allergies': request.form.get('donorAllergies'),
            'surgeries': request.form.get('donorSurgeries'),
            'travel': request.form.get('donorTravel'),
            'risk_behaviors': request.form.get('donorRiskBehaviors'),
            'occupation': request.form.get('donorOccupation'),
            'blood_type': request.form.get('donorBloodType'),
            'vital_signs': request.form.get('donorVitalSigns'),
            'hemoglobin': request.form.get('donorHemoglobin'),
            'past_donations': request.form.get('donorPastDonations'),
            'reactions': request.form.get('donorReactions'),
            'consent_donate': request.form.get('donorConsentDonate'),
            'consent_test': request.form.get('donorConsentTest')
        }
        
        # Here you could save the donor_data to a database or process it further
        print(donor_data)  # For debugging purposes
        
        # After processing, redirect to the thank you page
        return redirect(url_for('thank_you'))

    # If GET request, render the donor form page
    return render_template('donor.html')

@app.route('/thank_a')
def recipient_thank_you():
    return render_template('thank_a.html')


@app.route('/acceptor', methods=['GET', 'POST'])
def acceptor():
    if request.method == 'POST':
        print("Sumanta")
        # Extracting data from the form
        recipient_data = {
            'name': request.form.get('recipientName'),
            'dob': request.form.get('recipientDob'),
            'phone': request.form.get('recipientPhone'),
            'email': request.form.get('recipientEmail'),
            'address': request.form.get('recipientAddress'),
            'diagnosis': request.form.get('recipientDiagnosis'),
            'blood_type': request.form.get('recipientBloodType'),
            'medications': request.form.get('recipientMedications'),
            'allergies': request.form.get('recipientAllergies'),
            'transfusions': request.form.get('recipientTransfusions'),
            'vital_signs': request.form.get('recipientVitalSigns'),
            'lab_tests': request.form.get('recipientLabTests'),
            'consent_receive': request.form.get('recipientConsentReceive'),
            'consent_medical': request.form.get('recipientConsentMedical'),
            'emergency_contact': request.form.get('recipientEmergencyContact'),
            'emergency_phone': request.form.get('recipientEmergencyPhone'),
            'insurance': request.form.get('recipientInsurance')
        }

        # Here you would typically save the data to a database

        # Redirect to a thank-you page
        return redirect(url_for('recipient_thank_you'))

    # Render the form if it's a GET request
    return render_template('acceptor.html')


@app.route('/match_donors', methods=['POST'])
def match_donors():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Invalid input"}), 400

    matches = []
    for recipient in data.get('recipients', []):
        for donor in donors:
            if donor['blood_group'] == recipient['blood_group'] and donor['units'] >= recipient['units']:
                if not donor['has_transmissible_disease'] and not any(condition in donor['health_conditions'] for condition in ["heart disease", "diabetes"]):
                    matches.append({
                        "recipient": recipient['name'],
                        "donor": donor['name'],
                        "units": recipient['units']
                    })
                    donor['units'] -= recipient['units']
                    break
    return jsonify({"matches": matches, "donors": donors})

if __name__ == '__main__':
    app.run(debug=True)