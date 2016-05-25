#-*- coding: utf-8 -*-
import random

def BackgroundColor():
    from .source import colors
    backgroundColor = colors[random.randint(0,len(colors)-1)]
    return backgroundColor

def MakePoem():
    from .source import templates, words
    template = templates[random.randint(0,len(templates)-1)]
    num = random.randint(0,len(words['B'])-1)
    sentenceList = []
    for sentence in template:
        for word in sentence.split('/'):
            if word[0] is 'A':
                wordList = words[word[0]][word[1]][word[2]]
                sentenceList.append(wordList[random.randint(0,len(wordList)-1)])
            elif word[0] is 'B':
                wordList = words[word[0]][num][word[1]][word[2]]
                sentenceList.append(wordList[random.randint(0,len(wordList)-1)])
            else:
                sentenceList.append(word)
    poem = ''.join(sentenceList)
    return poem