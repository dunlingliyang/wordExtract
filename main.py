""" GET the offline interpretation of a word"""

import os
import re
from cache import *
from nltk.stem.wordnet import WordNetLemmatizer
import requests
from xml.dom.minidom import parse, parseString

fileList = os.listdir('.')
# fileList = [xx for xx in fileList if re.search('.*txt$', xx)]
fileList = ['data.txt']


def get_node_text(nodes):
    for node in nodes:
        if node.nodeType == node.TEXT_NODE:
            return(node.data)
    return ''


def get_rank_id(word, content):
    word_rank = -1
    for line in content.splitlines():
        if line.startswith(word.upper()):
            return round(word_rank / 10000)
        else:
            word_rank += 1
    return word_rank


for file in fileList:
    with open(file, encoding='utf8') as fid:
        content = fid.read()
        content = content.lower()
        prog = re.compile(r'[a-z\-]+')
        wordList = prog.findall(content)
        wordList = list(set(wordList))
        print("The length of word list is %d" % len(wordList))
    # get the interpretation of for each word
    notFound = 0
    wordDict = dict()

    with open('count.txt', 'r') as fid1:
        rank = fid1.read()

    with open(r'dict.txt', 'r', encoding='gbk') as fid:
        content = fid.read()
        for word in wordList:
            if word in wordDict.keys():
                continue
            else:
                line = re.search("{0}.*".format(word), content)
                if line is not None:
                    line = line.group()

                if line is None:
                    wordnet_lemmatizer = WordNetLemmatizer()
                    if word.endswith('ing|ed'):
                        word = wordnet_lemmatizer.lemmatize(word, pos='v')
                    elif word.endswith('s'):
                        word = wordnet_lemmatizer.lemmatize(word, pos='n')
                    else:
                        word = wordnet_lemmatizer.lemmatize(word)

                    line = re.search("{0}.*".format(word), content)
                    if line is not None:
                        line = line.group()

                if line is None:
                    url = r'http://dict-co.iciba.com/api/dictionary.php?w={0}&key=EA52AF8E6088B1E32B16603A488E3F9D&type=xml'.format(
                        word)
                    response = requests.get(url)
                    xmldom = parseString(response.text)
                    pos = xmldom.getElementsByTagName('pos')
                    acceptation = xmldom.getElementsByTagName('acceptation')
                    line = ''
                    for ii in range(len(pos)):
                        line = line + get_node_text(pos[ii].childNodes) + get_node_text(acceptation[ii].childNodes)

                word_rank = get_rank_id(word, rank)
                wordDict[word] = (line, word_rank)

    # print some useful info
    print('Total %d words are not found' % notFound)
    print('The ratio is %i' % (notFound / len(wordList)))
