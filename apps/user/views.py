from flask import Blueprint, render_template, url_for, redirect, request, jsonify, session, g
from .models import *
from exts import db
import os
from .smssend import SmsSendAPIDemo
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from settings import Config
from apps.article.models import Article_type, Article
from apps.utils.util import upload_qiniu

user_bp = Blueprint('user', __name__, url_prefix='/user')
required_login_list = ['/user/center', '/user/edit', '/article/publish','/user/upload_photo']

@user_bp.route('/')
def index():
    # cookie获取方式
    # uid = request.cookies.get('uid', None)
    # session的获取,session底层默认获取
    uid = session.get('uid')
    page = int(request.args.get('page', 1))
    # 无论是否登录都要显示文章列表和文章分类列表
    types = Article_type.query.all()
    # 分页
    # articles = Article.query.order_by(-Article.pdatetime).all()
    pagination = Article.query.order_by(-Article.pdatetime).paginate(page=page, per_page=2)

    # Pagination对象属性
    # pagination.items 当前页面中的记录
    # pagination.page 当前页数
    # pagination.prev_num # 上一页的页码数
    # pagination.next_num # 下一页的页码数
    # pagination.has_prev # 是否有上一页
    # pagination.has_next # 是否有下一页
    # pagination.pages  # 总页数
    # pagination.total  # 总的记录数

    if uid:
        user = User.query.get(uid)
        return render_template('user/index.html', user=user, types=types, pagination=pagination)
    else:
        return render_template('user/index.html', types=types, pagination=pagination)
# 用户注册
@user_bp.route('/register', methods=['POST','GET'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        repassword = request.form.get('repassword')
        phone = request.form.get('phone')
        email = request.form.get('email')
        if password == repassword:
            user =User()
            user.username = username
            user.password = generate_password_hash(password)
            user.phone = phone
            user.email = email
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('user.index'))
    return  render_template('user/register.html')

# 手机号码验证
@user_bp.route('/checkphone')
def check_phone():
    phone = request.args.get('phone')
    user = User.query.filter(User.phone==phone).all()
    # code:400 不能用  200 ：能用
    if len(user) > 0:
        print(user)
        return jsonify(code=400, msg='此号码已被注册')   # ajax必须返回json格式
    else:
        return jsonify(code=200, msg='此号码可用')

# 用户登录
@user_bp.route('/login', methods=['POST','GET'])
def login():
    if request.method == 'POST':
        # 判断是用户名登录f=1 还是手机号登录f=2
        f = request.args.get('f')
        if f == '1':
            username = request.form.get('username')
            password = request.form.get('password')
            users = User.query.filter(User.username == username).all()
            print(len(users))
            for user in users:
                flag = check_password_hash(user.password, password)
                if flag:
                    # cookie机制实现
                    # response = redirect(url_for('user.index'))
                    # response.set_cookie('uid', str(user.id),max_age=1800) # expires 过期时间
                    # return response
                    # session实现，session当成字典使用
                    session['uid'] = user.id
                    return redirect(url_for('user.index'))

                else:
                    return render_template('user/login.html', msg='用户名或者密码有误')
        elif f == '2': #手机号码登录
            code = request.form.get('code')
            phone = request.form.get('phone')
            # 验证码 先验证是否正确
            valid_code = session.get(phone)
            if code == valid_code:
                user = User.query.filter(User.phone == phone).first()
                if user:
                    # 登录成功 使用session机制
                    session['uid'] = user.id
                    return redirect(url_for('user.index'))
                else:
                    return render_template('user/login.html', msg='此号码未注册')
            else:
                return render_template('user/login.html', msg='验证码有误')

    else:
        return render_template('user/login.html')

# 退出
@user_bp.route('/logout')
def logout():
    # 1. cookie删除方式
    # response = redirect(url_for('user.index'))
    # 通过response对象的delete_cookie(key), key就是要删除的cookie的key
    # response.delete_cookie('uid')
    # 2. session的方式
    # del session['uid']
    session.clear()
    return redirect(url_for('user.index'))

# 发送短信息
@user_bp.route('/sendMsg', methods=['POST', 'GET'])
def send_message():
    phone = request.args.get('phone')
    # 补充 验证手机号码 是否注册，去数据库查询 ，若手机号码注册过则进行验证码的发送，否则返回此号码未注册
    SECRET_ID = "your_secret_id"  # 产品密钥ID，产品标识
    SECRET_KEY = "your_secret_key"  # 产品私有密钥，服务端生成签名信息使用，请严格保管，避免泄露
    BUSINESS_ID = "your_business_id"  # 业务ID，易盾根据产品业务特点分配
    api = SmsSendAPIDemo(SECRET_ID, SECRET_KEY, BUSINESS_ID)
    params = {
        "mobile": phone,
        "templateId": "10084",
        "paramType": "json",
        "params": "json格式字符串"
    }
    ret = api.send(params)
    session[phone] = '189075'  # 得到的验证码  将其放入session中，因为谁请求就会为谁分配一个session空间
    return jsonify(code=200, msg='短信发送成功')
    # if ret is not None:
    #     if ret["code"] == 200:
    #         taskId = ret["data"]["taskId"]
    #         print("taskId = %s" % taskId)
    #         session[phone] = '189075'
    #         return jsonify(code=200, msg='短信发送成功')
    #     else:
    #         print ("ERROR: ret.code=%s,msg=%s" % (ret['code'], ret['msg']))
    #         return jsonify(code=400, msg='短信发送失败')

# 用户中心
@user_bp.route('/center')
def user_center():
    # id = session.get('uid')
    # user = User.query.get(id)
    # return render_template('user/center.html',user=user)
    types = Article_type.query.all()
    photos = Photo.query.filter(Photo.user_id == g.user.id).all()
    return render_template('user/center.html', user=g.user, types=types,photos=photos)

@user_bp.before_app_request
def before_request():
    print('before request', request.path)
    if request.path in required_login_list:
        id = session.get('uid')
        if not id:
            return render_template('user/login.html')
        else:
            user = User.query.get(id)  #
            g.user = user  # g对象 是在本次请求中产生的对象
# 图片的扩展名
ALLOWED_EXTENSIONS = ['jpg','png','gif','bmp']
# 用户信息修改
@user_bp.route('/edit', methods=['POST', 'GET'])
def user_edit():
    if request.method == 'POST':
        username = request.form.get('username')
        phone = request.form.get('phone')
        email = request.form.get('email')
        # print(email)
        # 只要有文件(图片)， 获取方式必须使用request.files.get(name)
        icon = request.files.get('icon')

        # print('================>',icon)
        # FileStorage对象
        # 属性：filename 用户获取文件（图片）的名字
        # 方法：save(保存路径)
        icon_name = icon.filename
        print('+++++++++++++++++++++', icon_name)
        suffix = icon_name.rsplit('.')[-1]
        if suffix in ALLOWED_EXTENSIONS:
            icon_name = secure_filename(icon_name) #保证文件名符合python命名规则
            file_path = os.path.join(Config.UPLOAD_ICON_DIR, icon_name)
            icon.save(file_path)
            # 保存成功
            # 存数据库时 icon存相对路径
            user = g.user
            user.username = username
            user.phone = phone
            user.email = email
            path = 'upload/icon'
            user.icon = path + '/' + icon_name
            # print(os.path.join(path, icon_name))
            db.session.commit()
            # print('+++++++++++++',user.icon)
            # print(url_for('static', filename=user.icon ))
            return redirect(url_for('user.user_center'))
        else:
            return render_template('user/center.html', user=g.user, msg='必须扩展名是png,jpg,gif,bmp')
        # print(icon_name)
        # 查询 手机号码 如果已有该手机号码，则提示
        # 使用ajax 当失去焦点blur时间 验证手机号 采用该种方式时，就不必从数据库中
        # users = User.query.all()
        # for user in users:
        #     if user.phone == phone:
        #         return render_template('user/center.html', msg='此号码已被注册')

    return render_template('user/center.html', user=g.user)

# 自定义过滤器 过滤
@user_bp.app_template_filter('decode')
def content_cdecode(content):
    content = content.decode('utf-8')
    return content[:200]

@user_bp.route('/upload_photo', methods=['POST','GET'])
def upload_photo():
    # 获取上传的内容
    photo = request.form.get('photo') # FileStorage
    # photo.filename,   photo.save(path) 保存到本地
    ret, info = upload_qiniu(photo)
    if info.status_code == 200:
        photo = Photo()
        photo.photo_name = ret['key']
        photo.user_id = g.user.id
        db.session.add(photo)
        db.session.commit()
        return '上传成功'
    return '上传失败'