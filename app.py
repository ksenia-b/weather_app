import requests
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///weather.db'

db = SQLAlchemy(app)

class City(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)


@app.route('/')
def index():
    cities = City.query.all()


    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=Celsius&appid=cec38802cad45ce75d6a573c6d188633'
    weather_data = []

    for city in cities:

        r = requests.get(url.format(city.name)).json()
        print("r = ", r)

        weather = {
            "city": city.name,
            "temperature": r['main']['temp'],
            "description": r['weather'][0]['description'],
            "icon": r['weather'][0]['icon']
        }

        # print("weather = ", weather)

        weather_data.append(weather)

    return render_template('weather.html', weather_data=weather_data)


if '__name__' == "___main__":
    app.run()