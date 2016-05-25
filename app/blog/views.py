#-*- coding: utf-8 -*-
from flask import render_template, request, redirect, url_for, session, flash, abort
from . import blog
from .. import mongo
from ..models import Blog, Comment
from ..forms import ArticleForm
import bson
import datetime
import math
from flask.ext.login import login_required, current_user

@blog.route('/article/<string:blog_id>')
def article(blog_id):
    blog = mongo.db.blog.find_one({'_id':bson.ObjectId(blog_id)})
    if blog['permission'] == 'private':
        if blog['author'] == current_user.username:
            comment_list = []
            for cid in blog['comments_id']:
                comment = mongo.db.comment.find_one({'_id':cid})
                comment_list.append(comment)
            return render_template('blog/article.html',blog=blog,comment_list=comment_list)
        else:
            abort(404)
    else:
        comment_list = []
        for cid in blog['comments_id']:
            comment = mongo.db.comment.find_one({'_id':cid})
            comment_list.append(comment)
        return render_template('blog/article.html',blog=blog,comment_list=comment_list)

@blog.route('/blogs', defaults={'page': 1})
@blog.route('/blogs/<int:page>')
@login_required
def blogs(page):
    username = current_user.username
    blogs_id = mongo.db.user.find_one({'username':username})['blogs_id']
    blog_list = []
    for bid in blogs_id:
        bg = mongo.db.blog.find_one(bid)
        blog_list.append(bg)
    blogsTotalPages = math.ceil(len(blog_list)/5)
    blog_list = sorted(blog_list,key=lambda e:e['last_modify_time'],reverse=True)[(page-1)*5:page*5]
    return render_template('blog/blogs.html',blog_list=blog_list,blogsTotalPages=blogsTotalPages,page=page)

@blog.route('/article-add',methods=['GET','POST'])
@login_required
def article_add():
    form = ArticleForm()
    if request.method == 'POST' and form.validate_on_submit():
        username = current_user.username
        blog = Blog(
            author = username,
            title = form.title.data,
            article = request.form['article'],
            permission = form.permission.data,
            create_time = datetime.datetime.utcnow(),
            last_modify_time = datetime.datetime.utcnow()
        )
        blog_id = blog.save(username)
        flash('文章添加成功！')
        return redirect(url_for('.article',blog_id=blog_id))
    form.submit.label.text = '添加'
    return render_template('blog/article_edit.html',form=form)

@blog.route('/article-modify/<string:blog_id>',methods=['GET','POST'])
@login_required
def article_modify(blog_id):
    form = ArticleForm()
    if request.method == 'POST' and form.validate_on_submit():
        username = current_user.username
        title = form.title.data
        article = request.form['article']
        permission = form.permission.data
        last_modify_time = datetime.datetime.utcnow()
        mongo.db.blog.update(
            {'_id':bson.ObjectId(blog_id)},
            {'$set':
                {
                    'title':title,
                    'article':article,
                    'permission':permission,
                    'last_modify_time':last_modify_time
                }
            }
        )
        flash('文章修改成功！')
        return redirect(url_for('.article',blog_id=blog_id))
    blog = mongo.db.blog.find_one({'_id':bson.ObjectId(blog_id)})
    form.title.data = blog['title']
    form.submit.label.text = '修改'
    return render_template('blog/article_edit.html',form=form,blog=blog)

@blog.route('/blogs/delete/<string:blog_id>')
@login_required
def blog_delete(blog_id):
    username = current_user.username
    mongo.db.blog.remove({'_id':bson.ObjectId(blog_id)})
    mongo.db.user.update(
        {'username':username},
        {'$pull':
            {'blogs_id':bson.ObjectId(blog_id)}
        }
    )
    flash('文章删除成功！')
    return redirect(url_for('.blogs'))

@blog.route('/article/<string:blog_id>/add_comment',methods=['POST'])
@login_required
def blog_add_comment(blog_id):
    username = current_user.username
    comment  = Comment(
        author      = username,
        content     = request.form['content'],
        create_time = datetime.datetime.utcnow()
    )
    comment.save(bson.ObjectId(blog_id))
    flash('评论成功！')
    return redirect(url_for('.article',blog_id=blog_id))

@blog.route('/article/<string:blog_id>/del_comment/<string:comment_id>')
@login_required
def blog_del_comment(blog_id,comment_id):
    mongo.db.comment.remove({'_id':bson.ObjectId(comment_id)})
    mongo.db.blog.update(
        {'_id':bson.ObjectId(blog_id)},
        {'$pull':
            {'comments_id':bson.ObjectId(comment_id)}
        }
    )
    flash('评论删除成功！')
    return redirect(url_for('.article',blog_id=blog_id))
