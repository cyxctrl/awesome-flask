#-*- coding: utf-8 -*-
import random

text = 'Life is short, and you need Python.'

def backgroundPicture():
    num = random.random()
    name = int(num * 10)
    bgname = str(name) + '.jpg'
    return bgname