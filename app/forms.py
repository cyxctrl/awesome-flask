from flask import flash
from flask.ext.wtf import Form
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, Regexp, EqualTo, InputRequired
from flask_pagedown.fields import PageDownField
from . import mongo

class LoginForm(Form):
    username = StringField(u'邮箱或用户名',validators=[
        DataRequired(message=u'必填字段')
        ])

    password = PasswordField(u'密码',validators=[
        DataRequired(message=u'必填字段')
        ])

    remember_me = BooleanField(u'记住我')

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

class PageDownForm(Form):
    content = PageDownField(u'Enjoy Markdown!')
    submit = SubmitField(u'保存')

class EditProfileForm(Form):
    email = StringField(u'邮箱',validators=[
        DataRequired(message=u'必填字段')
        ])

    username = StringField(u'用户名', validators=[
        DataRequired(message=u'必填字段')
        ])

    location = StringField(u'位置', validators=[
        Length(0, 64)
        ])

    about_me = TextAreaField(u'个人简介')

    submit = SubmitField(u'提交')

class EditPasswordForm(Form):
    old_password = PasswordField(u'旧密码',validators=[
        DataRequired(message=u'必填字段')
        ])

    new_password = PasswordField(u'密码',validators=[
        DataRequired(message=u'必填字段'),
        Length(min=6,message=u'密码的最小长度为6个字符'),
        EqualTo('new_password2',message=u'两次输入的密码不一致')
        ])

    new_password2 = PasswordField(u'确认新密码',validators=[
        DataRequired(message=u'必填字段')
        ])

    submit = SubmitField(u'修改密码')

class ArticleForm(Form):
    title = StringField(u'标题',validators=[
        DataRequired(message=u'必填字段')])
    content = TextAreaField(u'文章内容')
