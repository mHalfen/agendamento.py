from flask import Flask
from blueprints.home import home_bp
from blueprints.login import login_bp, lm
from db import db
import os

app = Flask(__name__)

app.secret_key = '52a906839076c0f76b8811a3caaf3e38288e41d8e54ec252d844c9c2d3b04772'
lm.login_view = 'login'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///dados.db'
app.config['UPLOAD_FOLDER'] = os.path.join(app.root_path, 'static', 'files')

lm.init_app(app)
db.init_app(app)

app.register_blueprint(home_bp)
app.register_blueprint(login_bp)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()

    app.run(debug=True)