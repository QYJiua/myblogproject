# from flask import Blueprint, render_template, request
# from apps.user.models import User
# from apps.article.models import Article
# from exts import db
#
# # article_bp = Blueprint('article', __name__)
#
# # 用户发表文章
# @article_bp.route('/publish', methods=['POST','GET'])
# def article_publish():
#     if request.method == 'POST':
#         print('++++++++++++++post')
#         title = request.form.get('title')
#         content = request.form.get('content')
#         user_id = request.form.get('uid')
#         article = Article()
#         article.title = title
#         article.content = content
#         article.user_id = user_id
#         db.session.add(article)
#         db.session.commit()
#         return '添加成功'
#     else:
#         users = User.query.filter(User.isdelete == False).all()
#         print(users)
#         return render_template('article/add_article.html', users=users)
#
# # 显示发表的文章
# @article_bp.route('/show')
# def show_all():
#     articles = Article.query.all()
#     return render_template('article/all.html', articles=articles)
#
# # 显示某用户发表的文章
# @article_bp.route('/show1')
# def show_all1():
#     user_id = request.args.get('id')
#     user = User.query.get(user_id)
#     return render_template('article/all1.html', user=user)
#
#
