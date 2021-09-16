from exts import db

class Goods(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    gname = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    # 添加secondary 增加relationship 使得可以访问关系表中的外键 实现关系的建立
    users = db.relationship('User', backref='goodslist', secondary='user_goods')

    def __str__(self):
        return self.gname

# tags = db.Table('tags',
#                 db.Column('tag_id', db.Integer, db.ForeignKey('tag.id')),
#                 db.Column('page_id',db.Integer, db.ForeignKey('page.id'))
#                 )

# 关系表 多对多 user和goods之间的关系
class User_goods(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    good_id = db.Column(db.Integer, db.ForeignKey('goods.id'))
    number = db.Column(db.Integer, default=1)