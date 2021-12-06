from flask import Flask,render_template,request,redirect,url_for,flash
#from flask import MySql
from flask_sqlalchemy import SQLAlchemy



app = Flask(__name__)
app.secret_key = "Secret_key"

#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///bloodbank.db'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:Shantanu_.003@localhost/bloodbank'
app.config['SQLALCHEMY_TRACK_MODOFICATIONS'] = False

db = SQLAlchemy(app)

class Data(db.Model):
    id = db.Column(db.Integer,primary_key = True)
    name = db.Column(db.String(25))
    email = db.Column(db.String(25))
    phone = db.Column(db.String(25))
    bloodgrp = db.Column(db.String(10))

    def __init__ (self,name,email,phone,bloodgrp):
        self.name = name
        self.email = email
        self.phone = phone
        self.bloodgrp = bloodgrp


@app.route('/')
def Index():

    all_data = Data.query.all()

    # return "Hello Flask Application"
    return render_template("index.html",donors = all_data)

@app.route('/insert' , methods = ['POST'])
def insert():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        bloodgrp = request.form['bloodgrp']

        my_data = Data(name,email,phone,bloodgrp)
        db.session.add(my_data)
        db.session.commit()

        flash("Donor Added Successfully")

        return redirect(url_for('Index'))


@app.route('/update', methods = ['GET','POST'])
def update():

    if request.method == 'POST':
        my_data = Data.query.get(request.form.get('id'))

        my_data.name = request.form['name']
        my_data.email = request.form['email']
        my_data.phone = request.form['phone']
        my_data.bloodgrp = request.form['bloodgrp']

        db.session.commit()

        flash("Donor Updated Successfully")

        return redirect(url_for('Index'))


@app.route('/delete/<id>/', methods = ['Get','POST'])
def delete(id):

    my_data = Data.query.get(id)
    db.session.delete(my_data)
    db.session.commit()

    flash("Donor Deleted Successfully")

    return redirect(url_for('Index'))




if __name__ == "__main__":
    app.run(debug=True)