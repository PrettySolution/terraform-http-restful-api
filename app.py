from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey, Text, DateTime
from datetime import datetime
from flask_bootstrap import Bootstrap

app = Flask(__name__)
Bootstrap(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

engine = create_engine('sqlite:///database.db', echo=False)
metadata = MetaData()
tfstate = Table('tfstate', metadata,
                Column('id', Integer, primary_key=True),
                Column('name', String),
                Column('state', Text),
                Column('date_created', DateTime, default=datetime.utcnow())
                )
metadata.create_all(engine)


class Tfstate(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    state = db.Column(db.Text, default='{}')
    date_created = db.Column(db.DateTime, default=datetime.utcnow())

    def __repr__(self):
        return '<tfstate %r>' % self.tfstate_name


@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        if request.form['name'] == '':
            return redirect('/')
        state_name = request.form['name']
        new_state = Tfstate(name=state_name)
        try:
            db.session.add(new_state)
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue adding your task'

    else:
        states = Tfstate.query.order_by(Tfstate.date_created).all()
        return render_template('index.html', states=states)


@app.route('/delete/<int:id>')
def delete(id):
    state_to_delete = Tfstate.query.get_or_404(id)

    try:
        db.session.delete(state_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return 'There was a problem deleting that state'


@app.route('/rename/<int:id>', methods=['GET', 'POST'])
def rename(id):
    state = Tfstate.query.get_or_404(id)

    if request.method == 'POST':
        state.name = request.form['name']

        try:
            db.session.commit()
            return redirect('/')
        except:
            return 'There was a problem renaming that state'
    else:
        return render_template('rename.html', state=state)


@app.route('/api/<str:name>', methods=['GET', 'POST'])
def rename(name):
    state = Tfstate.query.get_or_404(name)

    if request.method == 'POST':
        state.name = request.form['name']

        try:
            db.session.commit()
            return redirect('/')
        except:
            return 'There was a problem renaming that state'
    else:
        return render_template('rename.html', state=state)

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port='80')
    # app.run(debug=True)
