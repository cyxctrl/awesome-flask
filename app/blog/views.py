#-*- coding: utf-8 -*-
from flask import render_template, request, redirect, url_for, session, flash
from . import blog
from .. import mongo
from ..models import Blog, Comment
import bson
import datetime
from flask.ext.login import login_required, current_user

@blog.route('/article/<string:blog_id>')
def article(blog_id):
    blog = mongo.db.blog.find_one({'_id':bson.ObjectId(blog_id)})
    comment_list = []
    for cid in blog['comments_id']:
        comment = mongo.db.comment.find_one({'_id':cid})
        comment_list.append(comment)
    return render_template(
        'article.html',
        blog = blog,
        comment_list = comment_list
    )

@blog.route('/blogs')
@login_required
def blogs():
    username = current_user.username
    blogs_id = mongo.db.user.find_one({'username':username})['blogs_id']
    blog_list = []
    for bid in blogs_id:
        bg = mongo.db.blog.find_one(bid)
        blog_list.append(bg)
    return render_template(
        'blogs.html',
        blog_list = blog_list[::-1]
    )


@blog.route('/editor')
@login_required
def editor_add():
    return render_template('editor.html')

@blog.route('/blogs/add',methods=['POST'])
@login_required
def blog_add():
    username = current_user.username
    blog     = Blog(
        author           = username,
        title            = request.form['title'],
        article          = request.form['article'],
        create_time      = datetime.datetime.utcnow(),
        last_modify_time = datetime.datetime.utcnow()
    )
    blog.save(username)
    return redirect(url_for('.blogs'))

@blog.route('/editor/<string:blog_id>')
@login_required
def editor_modify(blog_id):
    username = current_user.username
    blog = mongo.db.blog.find_one({'_id':bson.ObjectId(blog_id)})
    return render_template(
        'editor.html',
        blog = blog
    )

@blog.route('/blogs/modify/<string:blog_id>',methods=['POST'])
@login_required
def blog_modify(blog_id):
    username         = current_user.username
    title            = request.form['title']
    article          = request.form['article']
    last_modify_time = datetime.datetime.utcnow()
    mongo.db.blog.update(
        {'_id':bson.ObjectId(blog_id)},
        {'$set':
                {
                    'title':title,
                    'article':article,
                    'last_modify_time':last_modify_time
                }
        }
    )
    return redirect(url_for('.blogs',username=username))

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
