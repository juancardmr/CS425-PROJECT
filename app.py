from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

ENV = 'dev'

if ENV == 'dev':
    app.debug = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@localhost/flight_app'
else:
    app.debug = False
    app.config['SQLALCHEMY_DATABASE_URI'] = ''

app.config['SQLALCHEMY_DTRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
app.secret_key = 'secret key'


class customer(db.Model):
    __tablename__ = 'Customer'
    email = db.Column(db.String(200), primary_key=True)
    firstName = db.Column(db.String(200))
    middleName = db.Column(db.String(200))
    lastName = db.Column(db.String(200))
    line1 = db.Column(db.String(200))
    line2 = db.Column(db.String(200))
    city = db.Column(db.String(200))
    zipCode = db.Column(db.String(200))
    state = db.Column(db.String(200))
    country = db.Column(db.String(200))
    cardNumber = db.Column(db.String(200))
    cardName = db.Column(db.String(200))

    def __init__(self, email, firstName, middleName, lastName, line1, line2, city, zipCode, state, country, cardNumber, cardName):
        self.email = email
        self.firstName = firstName
        self.middleName = middleName
        self.lastName = lastName
        self.line1= line1
        self.line2 = line2
        self.city = city
        self.zipCode = zipCode
        self.state = state
        self.country = country
        self.cardNumber = cardNumber
        self.cardName = cardName


@app.route('/', methods=['GET', 'POST'])
def index():
    msg = ''
    if request.method == 'POST' and 'email' in request.form and 'password' in request.form:
        email = request.form['email']
        session['email'] = email
        password = request.form['password']
        sql = f"select emailaddress, password from customer where emailaddress = '{email}' and password = '{password}'"
        cursor = db.session.execute(sql)
        account = cursor.fetchone()
        if account:
            return redirect(url_for('success'))
        else:
            msg = 'Invalid Credential, try again or Register'
    return render_template('login.html')

@app.route('/new', methods=['POST', 'GET'])
def new_user():
    if request.method == 'POST':
        email = request.form['email']
        firstName = request.form['firstName']
        middleName = request.form['middleName']
        lastName = request.form['lastName']
        IATA = request.form['IATA']
        password = request.form['password']

        if email == '' or firstName == '' or lastName == '' or password == '' or IATA == '':
            return render_template('register.html', message='Please enter required fields')
        else:
            sql = f"insert into customer values ('{email}', '{firstName}', '{middleName}', '{lastName}', '{password}', '{IATA}')"
            cursor = db.session.execute(sql)
            db.session.commit()
            return redirect(url_for('success'))

    return render_template('register.html')

@app.route('/success', methods=["GET", "POST"])
def success():
    sql = "select distinct country from airport where IATA in (select IATA from departure)"
    items = db.session.execute(sql)
    items = items.fetchall()

    if request.method == 'POST':
        country = request.form['country']
        return redirect(url_for('state', country=country))
    else:
        return render_template('success.html', items=items)


@app.route('/state', methods=["GET", "POST"])
def state():
    country = request.args.get('country')
    sql = f"select distinct state from airport where IATA in (select IATA from departure) and country='{country}'"
    items = db.session.execute(sql)
    items = items.fetchall()
    if request.method == 'POST':
        state = request.form['state']
        return redirect(url_for('flights', state=state))
    else:
        return render_template('state.html', items=items)


@app.route('/flights', methods=['GET'])
def flights():
    state = request.args.get('state')
    sql = f"select d.flightnumber, d.IATA, d.departuretime, a.IATA, a.arrivaltime from departure d, arrival a where a.flightnumber=d.flightnumber and d.IATA in (select IATA from airport where state='{state}')"
    data = db.session.execute(sql)
    data = data.fetchall()
    if request.method == 'POST':
        book = request.form["book"]
        return redirect(url_for('booking', book=book))
    else:
        return render_template('flights.html', data=data)


@app.route('/booking', methods=['POST', 'GET'])
def booking():
    flightid = request.get_data()
    flightid = flightid.decode()
    flightid = flightid[5:]
    session['flight'] = flightid
    sql = f"select firstclassprice, economyprice from flight where flightnumber='{flightid}' "
    data = db.session.execute(sql)
    data = data.fetchall()
    if request.method == 'post':
        payment = request.form['payment']
        return redirect(url_for('payment', payment=payment))
    return render_template('booking.html', data=data)


@app.route('/payment', methods=['POST', 'GET'])
def payment():
    price = request.get_data()
    price = price.decode()
    price = price[8:]
    if request.method == 'POST' and 'cardnumber' in request.form and 'cardname' in request.form:
        cardname = request.form['cardname']
        cardnumber = request.form['cardnumber']
        if cardname == '' or cardnumber == '':
            return render_template('payment.html', data=price)
        else:
            booking_id = hash(cardnumber)
            email = session['email']
            sql = f"insert into booking (bookingid, emailaddress) values ('{booking_id}', '{email}')"
            cursor = db.session.execute(sql)
            db.session.commit()
            return redirect(url_for('end', booking_id=booking_id))
    else:
        return render_template('payment.html', data=price)


@app.route('/end')
def end():
    booking_id = request.args.get('booking_id')
    return render_template('end.html', data=booking_id)


@app.route('/main', methods=['post'])
def submit():
    if request.method == 'post':
        email = request.form['Email Address']
        firstName = request.form['Fist Name']
        middleName = request.form['Middle Name']
        lastName = request.form['Last Name']
        line1 = request.form['Address: Line 1']
        line2 = request.form['Address: Line 2']
        city = request.form['Address: City']
        zipCode = request.form['Address: Zip Code']
        state = request.form['Address: State']
        country = request.form['Address: Country']
        cardNumber = request.form['Credit Card Number']
        cardName = request.form['Credit Card Name']

        if email == '' or firstName == '' or lastName == '':
            return render_template('index.html', message='Please enter required fields')
        if db.session.query(customer).filter(customer.email == email).count() == 0:
            data = customer(email, firstName, middleName,
                             lastName, line1, line2, city,
                             zipCode, state, country,
                             cardNumber, cardName)
            db.session.add(data)
            db.session.commit()

            return render_template('login.html')

        return render_template('login.html', message='User already exists')

if __name__ == '__main__':
    app.debug = True
    app.run()
