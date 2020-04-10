from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
# from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey

app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
# db = SQLAlchemy(app)
#
# engine = create_engine('sqlite:///database.db', echo=False)
# metadata = MetaData()
# historical_data = Table('historical_data', metadata,
#                         Column('id', Integer, primary_key=True),
#                         Column('reqId', String),
#                         Column('bar_date', String)
#                         )
# metadata.create_all(engine)


@app.route('/')
def index():
    return 'hello'


if __name__ == "__main__":
   # app.run(debug=True, host='0.0.0.0', port='80')
    app.run(debug=True)