# Awesome-Flask

**Awesome-Flask** is a Blog by Flask, It will update with learing.

#Requirements

- Ubuntu 15.10
- Sublime Text 3
- FLask 0.10.1
- Python 3.4.3
- virtualenv 1.11.6


#Install

```c
$ git clone https://github.com/cyxctrl/awesome-flask.git
```

or

```c

$ git clone git@github.com:cyxctrl/awesome-flask.git
```

#Usage

You can use the blog simply, just to do below:

```c
$ cd awesome-flask
$ pip install -r requirements.txt   #install all tools
$ python manage.py runserver
'''

or use virtual environment:

'''c
#based on Ubuntu 15.10
$ sudo apt-get install virtualenv   #install virtual environment
$ cd awesome-flask
$ virtualenv -p python3 py3venv   #create virtual environment 'py3venv'
$ source py3venv/bin/activate   #startup virtual environment
$ pip install -r requirements.txt   #install all tools
$ python manage.py runserver
'''

'''c
open the website(chrome best) and input
http://127.0.0.1:5000/
```

That's all.