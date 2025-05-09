from flask import Flask, send_from_directory
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from config import Config
from routes.auth import auth_bp
from routes.tours import tours_bp
from routes.bookings import bookings_bp
from routes.reviews import reviews_bp
from models.user import db

app = Flask(__name__, static_folder='static', template_folder='templates')
app.config.from_object(Config)
CORS(app)
db.init_app(app)
JWTManager(app)

# Регистрация blueprints
app.register_blueprint(auth_bp, url_prefix='/api')
app.register_blueprint(tours_bp, url_prefix='/api')
app.register_blueprint(bookings_bp, url_prefix='/api')
app.register_blueprint(reviews_bp, url_prefix='/api')

# Создание таблиц
with app.app_context():
    db.create_all()

# Отдача index.html для всех не-API маршрутов
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    return send_from_directory(app.static_folder, 'index.html')

if __name__ == '__main__':
    app.run(debug=True)