from flask import Flask, render_template, redirect, url_for
from flask_bootstrap import Bootstrap5
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired, URL
import csv

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your Key'
bootstrap = Bootstrap5(app)

class CafeForm(FlaskForm):
    cafe = StringField('Cafe name', validators=[DataRequired()])
    cafe_location = StringField(label="Cafe Location on Google Maps (URL)", validators=[DataRequired(), URL()])
    opening_time = StringField(label="Opening Time e.g 8A.M", validators=[DataRequired()])
    closing_time = StringField(label="Closing Time e.g 8P.M", validators=[DataRequired()])
    coffee_rating = SelectField(label="Coffee Rating", choices=["☕️","☕️☕️","☕️☕️☕️","☕️☕️☕️☕️","☕️☕️☕️☕️☕️"], validators=[DataRequired()])
    wifi_rating = SelectField(label="Wifi Strength Rating", choices=[" ✘","💪","💪💪","💪💪💪","💪💪💪💪"], validators=[DataRequired()])
    power_outlet_rating = SelectField(label="Power Socket Availability", choices=[" ✘","🔌","🔌🔌","🔌🔌🔌","🔌🔌🔌🔌"], validators=[DataRequired()])
    submit = SubmitField('Submit')

@app.route("/")
def home():
    return render_template("index.html")


@app.route('/add', methods=["GET", "POST"])
def add_cafe():
    form = CafeForm()
    if form.validate_on_submit():
        with open("cafe-data.csv", mode="a", encoding='utf-8') as csv_file:
            csv_file.write(f"\n{form.cafe.data},"
                           f"{form.cafe_location.data},"
                           f"{form.opening_time.data},"
                           f"{form.closing_time.data},"
                           f"{form.coffee_rating.data},"
                           f"{form.wifi_rating.data},"
                           f"{form.power_outlet_rating.data}")
        return redirect(url_for('cafes'))
    return render_template('add.html', form=form)

@app.route('/cafes')
def cafes():
    with open('cafe-data.csv', newline='', encoding='utf-8') as csv_file:
        csv_data = csv.reader(csv_file, delimiter=',')
        list_of_rows = [row for row in csv_data]
    return render_template('cafes.html', cafes=list_of_rows)

if __name__ == '__main__':
    app.run(debug=True)
