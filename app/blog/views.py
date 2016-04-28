#-*- coding: utf-8 -*-
from flask import render_template, request, redirect, url_for, session, flash
from . import blog
from .. import mongo
from ..models import Blog, Comment
import bson
import datetime

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
def blogs():
    if session.get('logged_in'):
        username = session.get('user')
        blogs_id = mongo.db.user.find_one({'username':username})['blogs_id']
        blog_list = []
        for bid in blogs_id:
            bg = mongo.db.blog.find_one(bid)
            blog_list.append(bg)
        return render_template(
            'blogs.html',
            blog_list = blog_list[::-1]
        )
    else:
        flash('请登录先！')
        return redirect(url_for('main.index'))

@blog.route('/editor')
def editor_add():
    if session.get('logged_in'):
        return render_template('editor.html')
    else:
        flash('请登录先！')
        return redirect(url_for('main.index'))

@blog.route('/blogs/add',methods=['POST'])
def blog_add():
    if session.get('logged_in'):
        username = session.get('user')
        blog     = Blog(
            author           = username,
            title            = request.form['title'],
            article          = request.form['article'],
            create_time      = datetime.datetime.utcnow(),
            last_modify_time = '-'
        )
        blog.save(username)
        return redirect(url_for('.blogs'))
    else:
        flash('请登录先！')
        return redirect(url_for('main.index'))

@blog.route('/editor/<string:blog_id>')
def editor_modify(blog_id):
    if session.get('logged_in'):
        username = session.get('user')
        blog = mongo.db.blog.find_one({'_id':bson.ObjectId(blog_id)})
        return render_template(
            'editor.html',
            blog = blog
        )
    else:
        flash('请登录先！')
        return redirect(url_for('main.index'))

@blog.route('/blogs/modify/<string:blog_id>',methods=['POST'])
def blog_modify(blog_id):
    if session.get('logged_in'):
        username         = session.get('user')
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
    else:
        flash('请登录先！')
        return redirect(url_for('main.index'))

@blog.route('/blogs/delete/<string:blog_id>')
def blog_delete(blog_id):
    if session.get('logged_in'):
        username = session.get('user')
        mongo.db.blog.remove({'_id':bson.ObjectId(blog_id)})
        mongo.db.user.update(
            {'username':username},
            {'$pull':
                {'blogs_id':bson.ObjectId(blog_id)}
            }
        )
        return redirect(url_for('.blogs'))
    else:
        flash('请登录先！')
        return redirect(url_for('main.index'))

@blog.route('/article/<string:blog_id>/add_comment',methods=['POST'])
def blog_add_comment(blog_id):
    if session.get('logged_in'):
        username = session.get('user')
        comment  = Comment(
            author      = username,
            content     = request.form['content'],
            create_time = datetime.datetime.utcnow()
        )
        comment.save(bson.ObjectId(blog_id))
        flash('评论成功！')
        return redirect(url_for('.article',blog_id=blog_id))
    else:
        flash('请登录先！')
        return redirect(url_for('.article',blog_id=blog_id))

@blog.route('/article/<string:blog_id>/del_comment/<string:comment_id>')
def blog_del_comment(blog_id,comment_id):
    if session.get('logged_in'):
        mongo.db.comment.remove({'_id':bson.ObjectId(comment_id)})
        mongo.db.blog.update(
            {'_id':bson.ObjectId(blog_id)},
            {'$pull':
                {'comments_id':bson.ObjectId(comment_id)}
            }
        )
        flash('评论删除成功！')
        return redirect(url_for('.article',blog_id=blog_id))
    else:
        flash('请登录先！')
        return redirect(url_for('.article',blog_id=blog_id))