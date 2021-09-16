import os

class Config:
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:root@localhost:3306/flaskblog'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = True
    SECRET_KEY = 'DLAJFOAJGHOJPJSDOFP'
    # 项目路径 __file__当前文件  即settings.py文件的绝对路径的文件夹
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    # 静态文件夹的路径
    APPS_DIR = os.path.join(BASE_DIR, 'apps')
    STATIC_DIR = os.path.join(APPS_DIR, 'static')
    TEMPLATES_DIR = os.path.join(APPS_DIR, 'templates')
    # 头像的上传目录
    UPLOAD_ICON_DIR = os.path.join(STATIC_DIR, 'upload\icon')
    # 相册的上传目录
    UPLOAD_PHOTO_DIR = os.path.join(STATIC_DIR, 'upload\photo')

class DevelopmentConfig(Config):
    ENV = 'development'

class ProductionConfig(Config):
    ENV = 'productin'
    DEBUG = False

if __name__ == '__main__':
    print(Config.BASE_DIR)
    print(Config.UPLOAD_ICON_DIR)