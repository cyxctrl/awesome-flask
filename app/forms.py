from flask import flash
from flask.ext.wtf import Form
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, Email, Regexp, EqualTo, InputRequired
from . import mongo

class LoginForm(Form):
    username = StringField(u'邮箱或用户名',validators=[
        DataRequired(message=u'必填字段')
        ])

    password = PasswordField(u'密码',validators=[
        DataRequired(message=u'必填字段')
        ])

    submit = SubmitField(u'登录')

class RegisterForm(Form):
    email = StringField(u'邮箱',validators=[
        DataRequired(message=u'必填字段'),
        Length(min=1,max=64,message=u'邮箱由1到64个字符组成'),
        Email(u'请输入有效的邮箱')
        ])

    username = StringField(u'用户名',validators=[
        DataRequired(message=u'必填字段'),
        Length(min=3,max=15,message=u'用户名由3到15个字符组成'),
        Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
               u'用户名只能由字母、数字、下划线组成，并且不能以数字开头')
        ])

    password = PasswordField(u'密码',validators=[
        DataRequired(message=u'必填字段'),
        Length(min=6,message=u'密码的最小长度为6个字符'),
        EqualTo('password2',message=u'两次输入的密码不一致')
        ])

    password2 = PasswordField(u'确认密码',validators=[
        DataRequired(message=u'必填字段'),
        Length(min=6,message=u'密码的最小长度为6个字符')
        ])

    submit = SubmitField(u'注册')

    def validate_email(self,field):
        if mongo.db.user.find_one({'email':field.data}):
            flash(u'邮箱已被注册。')

    def validate_username(self,field):
        if mongo.db.user.find_one({'username':field.data}):
            flash(u'用户名已被使用。')


