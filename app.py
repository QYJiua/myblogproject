from apps import create_app
from flask_migrate import Migrate,MigrateCommand
from flask_script import Manager
from exts import db
from apps.article.models import *
from apps.user.models import *
from apps.goods.models import *

app = create_app()
# 让python支持命令行工作
manager = Manager(app=app)
# #使用migrate绑定app和db
migrate = Migrate(app=app, db=db)
# 添加迁移脚本的命令到manager中
manager.add_command('db', MigrateCommand)

# print(app.url_map)
if __name__ == '__main__':
    manager.run()
