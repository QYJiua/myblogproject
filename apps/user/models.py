from exts import db
from datetime import datetime

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(20), nullable=False)
    password = db.Column(db.String(64), nullable=False)
    phone = db.Column(db.String(11), unique=True, nullable=False)
    email = db.Column(db.String(30))
    icon = db.Column(db.String(100))  # 头像地址
    isdelete = db.Column(db.Boolean, default=False)  # 逻辑删除
    rdatetime = db.Column(db.DateTime, default=datetime.now)

    # 在查找user的文章列表时使用user.articles;backref是反向引用
# 根据文章找文章的作者时通过该反向引用来实现，直接使用article.user得到作者对象
    articles = db.relationship('Article', backref='user')

    def __str__(self):
        return self.username

class Photo(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    photo_name = db.Column(db.String(50),nullable=False)
    photo_datetime = db.Column(db.DateTime, default=datetime.now)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'),nullable=False)

    def __str__(self):
        return self.photo_name