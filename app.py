from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)


@app.route('/')
def index():
    return 'hello'


if __name__ == "__main__":
   # app.run(debug=True, host='0.0.0.0', port='80')
    app.run(debug=True)