#-*- coding: utf-8 -*-
from flask import flash
from flask.ext.wtf import Form
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, Regexp, EqualTo, InputRequired
from flask_pagedown.fields import PageDownField
from . import mongo

class LoginForm(Form):
    username = StringField('用户名或邮箱',validators=[
        DataRequired(message='请填写用户名或邮箱。')
        ])

    password = PasswordField('密码',validators=[
        DataRequired(message='请填写密码。')
        ])

    remember_me = BooleanField('记住我')

    submit = SubmitField('登录')

class RegisterForm(Form):
    username = StringField('用户名',validators=[
        DataRequired(message='请填写用户名。'),
        Length(min=3,max=15,message='用户名由3到15个字符组成。'),
        Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
               '用户名只能由字母、数字、下划线组成，并且不能以数字开头。')
        ])

    email = StringField('邮箱',validators=[
        DataRequired(message='请填写邮箱。'),
        Length(min=1,max=64,message='邮箱由1到64个字符组成。'),
        Email('请输入有效的邮箱')
        ])

    password = PasswordField('密码',validators=[
        DataRequired(message='请填写密码。'),
        Length(min=6,message='密码的最小长度为6个字符。'),
        EqualTo('password2',message='两次输入的密码不一致。')
        ])

    password2 = PasswordField('确认密码',validators=[
        DataRequired(message='请填写确认密码。'),
        Length(min=6,message='密码的最小长度为6个字符。')
        ])

    submit = SubmitField('注册')

class PageDownForm(Form):
    content = PageDownField('Enjoy Markdown!')

    submit = SubmitField('保存')

class EditProfileForm(Form):
    username = StringField('用户名', validators=[
        DataRequired(message='请填写用户名。')
        ])

    email = StringField('邮箱',validators=[
        DataRequired(message='请填写邮箱。')
        ])

    location = StringField('位置', validators=[
        Length(0, 64)
        ])

    about_me = TextAreaField('个人简介')

    submit = SubmitField('提交')

class ValidatePasswordForm(Form):
    password = PasswordField('密码',validators=[
        DataRequired(message='请填写密码。'),
        Length(min=6,message='密码的最小长度为6个字符。'),
        EqualTo('password2',message='两次输入的密码不一致。')
        ])

    password2 = PasswordField('确认密码',validators=[
        DataRequired(message='请填写确认密码。'),
        Length(min=6,message='密码的最小长度为6个字符。')
        ])

    submit = SubmitField('提交')

class EditPasswordForm(Form):
    password = PasswordField('新密码',validators=[
        DataRequired(message='请填写新密码。'),
        Length(min=6,message='密码的最小长度为6个字符。'),
        EqualTo('password2',message='两次输入的密码不一致。')
        ])

    password2 = PasswordField('确认新密码',validators=[
        DataRequired(message='请填写确认新密码。')
        ])

    submit = SubmitField('修改密码')

class EditPasswordQuestionsForm(Form):
    question1 = StringField('自定义密保问题1',validators=[
        DataRequired(message='请填写自定义密保问题1')])

    answer1 = StringField('答案1',validators=[
        DataRequired(message='请填写密保答案1')])

    question2 = StringField('自定义密保问题2',validators=[
        DataRequired(message='请填写自定义密保问题2')])

    answer2 = StringField('答案2',validators=[
        DataRequired(message='请填写密保答案2')])

    submit = SubmitField('修改密保')

class ValidateUserForm(Form):
    username = StringField('用户名',validators=[
        DataRequired(message='请填写用户名。'),
        Length(min=3,max=15,message='用户名由3到15个字符组成。'),
        Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
               '用户名只能由字母、数字、下划线组成，并且不能以数字开头。')
        ])

    email = StringField('邮箱',validators=[
        DataRequired(message='请填写邮箱。'),
        Length(min=1,max=64,message='邮箱由1到64个字符组成。'),
        Email('请输入有效的邮箱。')
        ])

    submit = SubmitField('提交')

class ValidatePasswordQuestionsForm(Form):
    username = StringField('用户名', validators=[
        DataRequired(message='请填写用户名。')
        ])

    email = StringField('邮箱',validators=[
        DataRequired(message='请填写邮箱。')
        ])

    answer1 = StringField('答案1',validators=[
        DataRequired(message='请填写密保答案1')])

    answer2 = StringField('答案2',validators=[
        DataRequired(message='请填写密保答案2')])

    submit = SubmitField('提交')

class ArticleForm(Form):
    title = StringField('标题',validators=[
        DataRequired(message='请填写标题。')])

    permission = StringField(validators=[
        DataRequired(message='请设置文章权限。')])

    submit = SubmitField()

class TodoForm(Form):
    content = StringField('最多输入100个字符。',validators=[
        DataRequired(message='请填写内容。'),
        Length(max=100,message='最多输入100个字符。')])

    submit = SubmitField('增加')

class AdminManageProfileForm(Form):
    username = StringField('用户名',validators=[
        DataRequired(message='请填写用户名')
        ])

    email = StringField('邮箱',validators=[
        DataRequired(message='请填写邮箱。'),
        Email('请输入有效的邮箱')
        ])

    question1 = StringField('自定义密保问题1')

    answer1 = StringField('答案1')

    question2 = StringField('自定义密保问题2')

    answer2 = StringField('答案2')

    permission = StringField('权限')

    register_time = StringField('注册时间')

    following = StringField('关注的人')

    location = StringField('位置')

    about_me = TextAreaField('个人简介')

    submit = SubmitField('修改')

