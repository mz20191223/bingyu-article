from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()


class SysUser(db.Model):
    __tablename__ = 'sys_user'

    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(50), unique=True, nullable=False, index=True)
    password = db.Column(db.String(32), nullable=False)
    nickname = db.Column(db.String(50))
    phone = db.Column(db.String(20))
    email = db.Column(db.String(100))
    avatar = db.Column(db.String(255))
    status = db.Column(db.Integer, default=0)
    dept_id = db.Column(db.Integer)
    post_id = db.Column(db.Integer)
    remark = db.Column(db.String(500))
    create_time = db.Column(db.DateTime, default=datetime.now)
    update_time = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)


class SysRole(db.Model):
    __tablename__ = 'sys_role'

    role_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    role_name = db.Column(db.String(50), nullable=False)
    role_code = db.Column(db.String(50), unique=True, nullable=False)
    role_sort = db.Column(db.Integer, default=0)
    status = db.Column(db.Integer, default=0)
    remark = db.Column(db.String(500))
    create_time = db.Column(db.DateTime, default=datetime.now)
    update_time = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)


class SysDept(db.Model):
    __tablename__ = 'sys_dept'

    dept_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    parent_id = db.Column(db.Integer, default=0)
    dept_name = db.Column(db.String(50), nullable=False)
    dept_sort = db.Column(db.Integer, default=0)
    leader = db.Column(db.String(50))
    phone = db.Column(db.String(20))
    email = db.Column(db.String(100))
    status = db.Column(db.Integer, default=0)
    create_time = db.Column(db.DateTime, default=datetime.now)
    update_time = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)


class SysPost(db.Model):
    __tablename__ = 'sys_post'

    post_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    post_code = db.Column(db.String(50), unique=True, nullable=False)
    post_name = db.Column(db.String(50), nullable=False)
    post_sort = db.Column(db.Integer, default=0)
    status = db.Column(db.Integer, default=0)
    remark = db.Column(db.String(500))
    create_time = db.Column(db.DateTime, default=datetime.now)
    update_time = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)


class SysMenu(db.Model):
    __tablename__ = 'sys_menu'

    menu_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    menu_name = db.Column(db.String(50), nullable=False)
    parent_id = db.Column(db.Integer, default=0)
    order_num = db.Column(db.Integer, default=0)
    menu_sort = db.Column(db.Integer, default=0)
    path = db.Column(db.String(200))
    component = db.Column(db.String(255))
    is_frame = db.Column(db.Integer, default=1)
    menu_type = db.Column(db.String(1))
    visible = db.Column(db.String(1), default='0')
    status = db.Column(db.String(1), default='0')
    perms = db.Column(db.String(100))
    icon = db.Column(db.String(100))
    create_time = db.Column(db.DateTime, default=datetime.now)
    update_time = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)


class SysUserRole(db.Model):
    __tablename__ = 'sys_user_role'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, nullable=False)
    role_id = db.Column(db.Integer, nullable=False)


class SysRoleMenu(db.Model):
    __tablename__ = 'sys_role_menu'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    role_id = db.Column(db.Integer, nullable=False)
    menu_id = db.Column(db.Integer, nullable=False)


class SysOperLog(db.Model):
    __tablename__ = 'sys_oper_log'

    oper_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(50))
    business_type = db.Column(db.Integer)
    method = db.Column(db.String(100))
    request_method = db.Column(db.String(10))
    operator_type = db.Column(db.Integer)
    oper_name = db.Column(db.String(50))
    dept_name = db.Column(db.String(50))
    oper_url = db.Column(db.String(255))
    oper_ip = db.Column(db.String(50))
    oper_location = db.Column(db.String(255))
    oper_param = db.Column(db.Text)
    json_result = db.Column(db.Text)
    status = db.Column(db.Integer, default=0)
    error_msg = db.Column(db.Text)
    oper_time = db.Column(db.DateTime, default=datetime.now)


class SysLoginLog(db.Model):
    __tablename__ = 'sys_login_log'

    info_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_name = db.Column(db.String(50))
    ipaddr = db.Column(db.String(50))
    login_location = db.Column(db.String(255))
    browser = db.Column(db.String(50))
    os = db.Column(db.String(50))
    status = db.Column(db.String(5))
    msg = db.Column(db.String(255))
    login_time = db.Column(db.DateTime, default=datetime.now)


class Product(db.Model):
    __tablename__ = 'products'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(200), nullable=False)
    url = db.Column(db.String(500))
    description = db.Column(db.Text)
    status = db.Column(db.Integer, default=0)
    is_default = db.Column(db.Integer, default=0)
    create_time = db.Column(db.DateTime, default=datetime.now)
    update_time = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)


image_product = db.Table('image_product',
    db.Column('image_id', db.Integer, db.ForeignKey('images.id'), primary_key=True),
    db.Column('product_id', db.Integer, db.ForeignKey('products.id'), primary_key=True)
)


class Image(db.Model):
    __tablename__ = 'images'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    url = db.Column(db.String(500), nullable=False)
    position_type = db.Column(db.String(20), default='auto')
    position_value = db.Column(db.Integer, default=0)
    position_mode = db.Column(db.String(20), default='before')
    status = db.Column(db.Integer, default=0)
    create_time = db.Column(db.DateTime, default=datetime.now)
    update_time = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)

    products = db.relationship('Product', secondary=image_product, backref=db.backref('images', lazy='dynamic'))


class Keyword(db.Model):
    __tablename__ = 'keywords'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    keyword = db.Column(db.String(100), nullable=False)
    status = db.Column(db.Integer, default=0)
    create_time = db.Column(db.DateTime, default=datetime.now)
    update_time = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)


content_template_product = db.Table('content_template_product',
    db.Column('template_id', db.Integer, db.ForeignKey('content_prompt_templates.id'), primary_key=True),
    db.Column('product_id', db.Integer, db.ForeignKey('products.id'), primary_key=True)
)

title_template_product = db.Table('title_template_product',
    db.Column('template_id', db.Integer, db.ForeignKey('title_prompt_templates.id'), primary_key=True),
    db.Column('product_id', db.Integer, db.ForeignKey('products.id'), primary_key=True)
)

template_product = db.Table('template_product',
    db.Column('template_id', db.Integer, db.ForeignKey('prompt_templates.id'), primary_key=True),
    db.Column('product_id', db.Integer, db.ForeignKey('products.id'), primary_key=True)
)


class PromptTemplate(db.Model):
    __tablename__ = 'prompt_templates'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    prompt_content = db.Column(db.Text, nullable=False)
    required_paragraphs = db.Column(db.Integer, default=5)
    business_type = db.Column(db.String(50))
    conclusion_text = db.Column(db.Text)
    is_default = db.Column(db.Integer, default=0)
    status = db.Column(db.Integer, default=0)
    create_time = db.Column(db.DateTime, default=datetime.now)
    update_time = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)

    products = db.relationship('Product', secondary=template_product, backref=db.backref('prompt_templates', lazy='dynamic'))


class ContentPromptTemplate(db.Model):
    __tablename__ = 'content_prompt_templates'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    business_type = db.Column(db.String(50))
    meta_title = db.Column(db.String(200))
    meta_description = db.Column(db.Text)
    keyword_prompt = db.Column(db.Text)
    content_prompt = db.Column(db.Text, nullable=False)
    conclusion_prompt = db.Column(db.Text)
    is_default = db.Column(db.Integer, default=0)
    status = db.Column(db.Integer, default=0)
    create_time = db.Column(db.DateTime, default=datetime.now)
    update_time = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)

    products = db.relationship('Product', secondary=content_template_product, backref=db.backref('content_templates', lazy='dynamic'))


class TitlePromptTemplate(db.Model):
    __tablename__ = 'title_prompt_templates'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    business_type = db.Column(db.String(50))
    title_prompt = db.Column(db.Text, nullable=False)
    is_default = db.Column(db.Integer, default=0)
    status = db.Column(db.Integer, default=0)
    create_time = db.Column(db.DateTime, default=datetime.now)
    update_time = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)

    products = db.relationship('Product', secondary=title_template_product, backref=db.backref('title_templates', lazy='dynamic'))


class AIModel(db.Model):
    __tablename__ = 'models'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    provider = db.Column(db.String(50), nullable=False)
    api_key = db.Column(db.String(500))
    api_url = db.Column(db.String(500))
    model_name = db.Column(db.String(100))
    parameters = db.Column(db.Text)
    is_default = db.Column(db.Integer, default=0)
    status = db.Column(db.Integer, default=0)
    create_time = db.Column(db.DateTime, default=datetime.now)
    update_time = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)


class Website(db.Model):
    __tablename__ = 'websites'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    code = db.Column(db.String(50), unique=True, nullable=False)
    login_url = db.Column(db.String(500))
    publish_url = db.Column(db.String(500))
    username = db.Column(db.String(100))
    password = db.Column(db.String(200))
    cookie = db.Column(db.Text)
    username_selector = db.Column(db.String(200))
    password_selector = db.Column(db.String(200))
    login_button_selector = db.Column(db.String(200))
    title_selector = db.Column(db.String(200))
    content_selector = db.Column(db.String(200))
    category_selector = db.Column(db.String(200))
    publish_button_selector = db.Column(db.String(200))
    status = db.Column(db.Integer, default=0)
    is_default = db.Column(db.Integer, default=0)
    create_time = db.Column(db.DateTime, default=datetime.now)
    update_time = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)


class PublishRecord(db.Model):
    __tablename__ = 'publish_records'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    product_id = db.Column(db.Integer)
    product_name = db.Column(db.String(200))
    website_id = db.Column(db.Integer)
    website_name = db.Column(db.String(100))
    title = db.Column(db.String(200))
    content = db.Column(db.Text)
    status = db.Column(db.String(20), default='pending')
    result_url = db.Column(db.String(500))
    error_msg = db.Column(db.Text)
    publish_time = db.Column(db.DateTime, default=datetime.now)
    create_time = db.Column(db.DateTime, default=datetime.now)
    update_time = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)


class Draft(db.Model):
    __tablename__ = 'drafts'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(200), nullable=False)
    data = db.Column(db.Text, nullable=False)
    create_by = db.Column(db.Integer)
    status = db.Column(db.Integer, default=0)
    create_time = db.Column(db.DateTime, default=datetime.now)
    update_time = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
