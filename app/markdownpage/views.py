#-*- coding: utf-8 -*-
from flask import render_template, request, redirect, url_for, session, flash
from . import markdownpage
from ..forms import PageDownForm
from .. import mongo

@markdownpage.route('/markdown')
def markdown():
    pagedownform = PageDownForm()
    if session.get('logged_in'):
        markdown_id = mongo.db.user.find_one({'username':session.get('user')})['markdown_id'][0]
        text = mongo.db.markdown.find_one({'_id':markdown_id})['text']
        pagedownform.content.data = text
    return render_template('markdown.html',pagedownform=pagedownform)

@markdownpage.route('/markdown/update',methods=['POST'])
def markdown_update():
    pagedownform = PageDownForm()
    if session.get('logged_in'):
        markdown_id = mongo.db.user.find_one({'username':session.get('user')})['markdown_id'][0]
        text = pagedownform.content.data
        mongo.db.markdown.update({'_id':markdown_id},{'text':text})
    else:
        flash('请登录先！')
    return redirect(url_for('markdownpage.markdown'))
