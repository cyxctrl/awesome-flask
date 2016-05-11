#-*- coding: utf-8 -*-
from flask import render_template, request, redirect, url_for, session, flash
from . import markdownpage
from ..forms import PageDownForm
from .. import mongo
from flask.ext.login import current_user

@markdownpage.route('/markdown')
def markdown():
    form = PageDownForm()
    if current_user.is_authenticated:
        markdown_id = mongo.db.user.find_one({'username':current_user.username})['markdown_id'][0]
        text = mongo.db.markdown.find_one({'_id':markdown_id})['text']
        form.content.data = text
    return render_template('markdown.html',form=form)

@markdownpage.route('/markdown/update',methods=['POST'])
def markdown_update():
    form = PageDownForm()
    if current_user.is_authenticated:
        markdown_id = mongo.db.user.find_one({'username':current_user.username})['markdown_id'][0]
        text = form.content.data
        mongo.db.markdown.update({'_id':markdown_id},{'text':text})
    else:
        flash('请先登录！')
    return redirect(url_for('markdownpage.markdown'))

@markdownpage.route('/markdown/introduction')
def markdown_introduction():
    form = PageDownForm()
    text = "#标题\r\nMarkdown 支持两种标题的语法，类 Setext 和类 atx 形式。\r\n\r\n类 Setext 形式是用底线的形式，利用 = （最高阶标题）和 - （第二阶标题），例如：\r\nThis is an H1\r\n=============\r\n\r\nThis is an H2\r\n-------------\r\n任何数量的 = 和 - 都可以有效果。\r\n\r\n类 Atx 形式则是在行首插入 1 到 6 个 # ，对应到标题 1 到 6 阶，例如：\r\n# 这是 H1\r\n\r\n## 这是 H2\r\n\r\n###### 这是 H6\r\n\r\n#区块引用\r\nMarkdown 标记区块引用是使用类似 email 中用 > 的引用方式。\r\n可以这样：\r\n> This is a blockquote with two paragraphs. Lorem ipsum dolor sit amet,\r\n> consectetuer adipiscing elit. Aliquam hendrerit mi posuere lectus.\r\n> Vestibulum enim wisi, viverra nec, fringilla in, laoreet vitae, risus.\r\n> \r\n> Donec sit amet nisl. Aliquam semper ipsum sit amet velit. Suspendisse\r\n> id sem consectetuer libero luctus adipiscing.\r\n\r\n也可以这样偷懒：\r\n> This is a blockquote with two paragraphs. Lorem ipsum dolor sit amet,\r\nconsectetuer adipiscing elit. Aliquam hendrerit mi posuere lectus.\r\nVestibulum enim wisi, viverra nec, fringilla in, laoreet vitae, risus.\r\n\r\n> Donec sit amet nisl. Aliquam semper ipsum sit amet velit. Suspendisse\r\nid sem consectetuer libero luctus adipiscing.\r\n\r\n区块引用可以嵌套（例如：引用内的引用），只要根据层次加上不同数量的 > ：\r\n> This is the first level of quoting.\r\n>\r\n> > This is nested blockquote.\r\n>\r\n> Back to the first level.\r\n\r\n引用的区块内也可以使用其他的 Markdown 语法，包括标题、列表、代码区块等：\r\n> ## 这是一个标题。\r\n> \r\n> 1.   这是第一行列表项。\r\n> 2.   这是第二行列表项。\r\n> \r\n> 给出一些例子代码：\r\n> \r\n>     return shell_exec(\"echo $input | $markdown_script\");\r\n\r\n#列表\r\nMarkdown 支持有序列表和无序列表。无序列表使用星号、加号或是减号作为列表标记：\r\n\r\n* Red\r\n* Green\r\n* Blue\r\n\r\n等同于：\r\n\r\n+ Red\r\n+ Green\r\n+ Blue\r\n\r\n也等同于：\r\n\r\n- Red\r\n- Green\r\n- Blue\r\n\r\n有序列表则使用数字接着一个英文句点：\r\n\r\n1. Bird\r\n2. McHale\r\n3. Parish\r\n\r\n列表项目标记通常是放在最左边，但是其实也可以缩进，最多 3 个空格，项目标记后面则一定要接着至少一个空格或制表符。\r\n\r\n*   Lorem ipsum dolor sit amet, consectetuer adipiscing elit.\r\n    Aliquam hendrerit mi posuere lectus. Vestibulum enim wisi,\r\n    viverra nec, fringilla in, laoreet vitae, risus.\r\n*   Donec sit amet nisl. Aliquam semper ipsum sit amet velit.\r\n    Suspendisse id sem consectetuer libero luctus adipiscing.\r\n\r\n*   Lorem ipsum dolor sit amet, consectetuer adipiscing elit.\r\nAliquam hendrerit mi posuere lectus. Vestibulum enim wisi,\r\nviverra nec, fringilla in, laoreet vitae, risus.\r\n*   Donec sit amet nisl. Aliquam semper ipsum sit amet velit.\r\nSuspendisse id sem consectetuer libero luctus adipiscing.\r\n\r\n这是一个普通段落。\r\n\r\n    这是一个代码区块。\r\n\r\n这个每行一阶的缩进（4 个空格或是 1 个制表符），都会被移除，例如：\r\n\r\nHere is an example of AppleScript:\r\n\r\n    tell application \"Foo\"\r\n        beep\r\n    end tell\r\n\r\n#分隔线\r\n\r\n* * *\r\n\r\n***\r\n\r\n*****\r\n\r\n- - -\r\n\r\n---------------------------------------\r\n\r\n#区段元素\r\n\r\n##链接\r\n\r\nThis is [an example](http://example.com/ \"Title\") inline link.\r\n\r\n[This link](http://example.net/) has no title attribute.\r\n\r\nI get 10 times more traffic from [Google](http://google.com/ \"Google\")\r\nthan from [Yahoo](http://search.yahoo.com/ \"Yahoo Search\") or\r\n[MSN](http://search.msn.com/ \"MSN Search\").\r\n\r\n##强调\r\n*single asterisks*\r\n\r\n_single underscores_\r\n\r\n**double asterisks**\r\n\r\n__double underscores__\r\n\r\n如果要在文字前后直接插入普通的星号或底线，你可以用反斜线：\r\n\r\n\\*this text is surrounded by literal asterisks\\*\r\n\r\n##代码\r\n\r\n如果要标记一小段行内代码，你可以用反引号把它包起来（`），例如：\r\n\r\nUse the `printf()` function.\r\n\r\n如果要在代码区段内插入反引号，你可以用多个反引号来开启和结束代码区段：\r\n\r\n``There is a literal backtick (`) here.``\r\n\r\n代码区段的起始和结束端都可以放入一个空白，起始端后面一个，结束端前面一个，这样你就可以在区段的一开始就插入反引号：\r\n\r\nA single backtick in a code span: `` ` ``\r\n\r\nA backtick-delimited string in a code span: `` `foo` ``\r\n\r\n##图片\r\n\r\n![Pic](/static/index3.jpg)\r\n\r\n##自动链接\r\n\r\n<http://example.com/>"
    form.content.data = text
    return render_template('markdown_introduction.html',form=form)