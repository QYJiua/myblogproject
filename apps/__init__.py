from flask import Flask
from exts import db, bootstrap
from settings import DevelopmentConfig
from apps.user.views import user_bp
from apps.article.views import article_bp
from apps.goods.view import good_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object(DevelopmentConfig)
    db.init_app(app)
    bootstrap.init_app(app=app)
    app.register_blueprint(user_bp)
    app.register_blueprint(article_bp)
    app.register_blueprint(good_bp)
    return app