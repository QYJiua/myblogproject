from flask import Blueprint, render_template, request, url_for, redirect
from apps.user.models import User
from apps.goods.models import *
good_bp = Blueprint('goods', __name__)
# 用户买了哪些商品
@good_bp.route('/show_goods')
def show_goods():
    uid = request.args.get('uid')
    user = User.query.get(uid)
    return render_template('goods/showgoods.html', user=user)

# 根据商品找买该商品的用户
@good_bp.route('/find_user')
def find_user():
    gid = request.args.get('gid')
    goods = Goods.query.get(gid)
    return render_template('goods/finduser.html', goods=goods)

# 得到购物页面 进行商品挑选
@good_bp.route('/show')
def show():
    users = User.query.filter(User.isdelete == False).all()
    goods = Goods.query.all()
    return render_template('goods/buy.html', users=users, goods=goods)
# 实现购买功能
@good_bp.route('/buy')
def buy():
    good_id = request.args.get('gid')
    user_id = request.args.get('uid')
    ug = User_goods()
    ug.user_id = user_id
    ug.good_id = good_id
    db.session.add(ug)
    db.session.commit()
    return '购买成功'
# 添加过滤器
@good_bp.app_template_filter('sum_li')
def sum_li(li):

    return sum(li)
