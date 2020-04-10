from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey, Text, DateTime
from datetime import datetime
from flask_bootstrap import Bootstrap

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

engine = create_engine('sqlite:///database.db', echo=False)
metadata = MetaData()
tfstate = Table('tfstate', metadata,
                Column('id', Integer, primary_key=True),
                Column('name', String),
                Column('json', Text),
                Column('date_created', DateTime, default=datetime.utcnow())
                )
metadata.create_all(engine)


class Tfstate(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    json = db.Column(db.Text, default='{}')
    date_created = db.Column(db.DateTime, default=datetime.utcnow())

    def __repr__(self):
        return '<tfstate %r>' % self.tfstate_name


@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        if request.form['content'] == '':
            return redirect('/')
        tfstate_content = request.form['content']
        new_tfstate = Tfstate(name=tfstate_content)
        try:
            db.session.add(new_tfstate)
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue adding your task'

    else:
        tasks = Tfstate.query.order_by(Tfstate.date_created).all()
        return render_template('index.html', tasks=tasks)


if __name__ == "__main__":
    # app.run(debug=True, host='0.0.0.0', port='80')
    app.run(debug=True)
