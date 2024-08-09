from flask import Flask
from blueprints.home import home_bp
from db import db

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///dados.db'
db.init_app(app)

app.register_blueprint(home_bp)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()

    app.run(debug=True)