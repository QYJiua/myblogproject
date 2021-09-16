from flask import Blueprint, render_template, request, g, redirect, url_for,jsonify,session
from apps.user.models import User
from apps.article.models import *
from exts import db

article_bp = Blueprint('article', __name__, url_prefix='/article')


# 自定义过滤器 过滤
@article_bp.app_template_filter('cdecode')
def content_cdecode(content):
    content = content.decode('utf-8')
    return content

@article_bp.route('/publish', methods=['POST','GET'])
def publish_article():
    if request.method == 'POST':
        title = request.form.get('title')
        type_id = request.form.get('type')
        content = request.form.get('content')
        article = Article()
        article.title = title
        article.type_id = type_id
        article.content = content
        article.user_id = g.user.id
        db.session.add(article)
        db.session.commit()
        return redirect(url_for('user.index'))
# 文章详情
@article_bp.route('/detail')
def article_detail():
    article_id =  request.args.get('aid')
    article = Article.query.get(article_id)
    types = Article_type.query.all()
     # 登录用户
    user = None
    user_id = session.get('uid',None)
    if user_id:
        user = User.query.get(user_id)
    return render_template('article/detail.html',article=article, types=types, user=user)

@article_bp.route('/save')
def article_save():
    article_id = request.args.get('aid')
    article = Article.query.get(article_id)
    tag = request.args.get('tag')
    if (tag == '0'):
        article.save_num += 1
    else:
        article.save_num -= 1
    db.session.commit()
    return jsonify(num=article.save_num)


@article_bp.route('/love')
def article_love():
    article_id = request.args.get('aid')
    article = Article.query.get(article_id)
    tag = request.args.get('tag')
    if (tag == '0'):
        article.love_num += 1
    else:
        article.love_num -= 1
    db.session.commit()
    return jsonify(num=article.love_num)

@article_bp.route('/article_comment',methods=['GET','POST'])
def article_comment():
    if request.method == 'POST':
        pass

