from exts import db
from datetime import datetime

class Article_type(db.Model):
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    type_name = db.Column(db.String(20), nullable=False)

    # relationship
    articles = db.relationship('Article', backref='article_type')

class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(50), nullable=False) # 标题
    content = db.Column(db.Text, nullable=False)     # 内容
    pdatetime = db.Column(db.DateTime, default=datetime.now) # 发表时间
    click_num = db.Column(db.Integer, default=0)  # 阅读量
    save_num = db.Column(db.Integer, default=0)   # 收藏数
    love_num = db.Column(db.Integer, default=0)   # 点赞数
    # 外键   外键在多这一侧定义 同步到数据库
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    type_id = db.Column(db.Integer, db.ForeignKey('article_type.id'))
    # relationship
    comments = db.relationship('Comment', backref='article')
# 评论
class Comment(db.Model):
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    article_id = db.Column(db.Integer, db.ForeignKey('article.id'))
    comment = db.Column(db.String(255), nullable=False)
    cdatetime = db.Column(db.DateTime, default=datetime.now)