# -*- coding: utf-8 -*-
import os
import random
import requests
import re
import time
from bs4 import BeautifulSoup

__author__ = 'admin'

print(os.getcwd())
fileList = os.listdir('../../data')
print(fileList)
for file in fileList:
    s = requests.session()
    s.keep_alive = False
    fid = open(r"../../data/data.txt", encoding='utf8')
    content = fid.read()
    content = content.lower()
    # print(content)
    prog = re.compile(r'[a-z\-]+')
    wordList = prog.findall(content)
    wordList = list(set(wordList))
    print(len(wordList))
    fid.close()
    error = 0
    with open(r'./word_list.txt', 'w+', encoding='utf8') as fid:
        wordDict = dict()
        for word in wordList:
            # fid.write('%s \n' % str(word).encode('utf8'))
            url = r'http://www.iciba.com/'
            requestURL = url + str(word)
            # requestURL = requestURL.replace('-','_')
            for ii in range(4):
                response = requests.get(requestURL, timeout=100)
                if response.status_code == 404:
                    print("error in loading page, retry")
                    print('the request url is %s' % requestURL)
                    print('current word is %s' % word)
                    time.sleep(5)
                else:
                    break
            if response.status_code == 404:
                continue
            soup = BeautifulSoup(response.text, 'html.parser')
            headword = soup.find('h1', attrs={'class': 'keyword'}).string

            # base_speak = soup.find('div',attrs={'class':'base-speak'})
            # pronounce = base_speak.text
            # print(pronounce)
            wordRate = len(soup.findAll('i', attrs={'class': 'light'}))
            print(wordRate)

            # fid.write('\n Pronounce %s \n' % str(pronounce).encode('utf8'))
            base_list = soup.find('ul', attrs={'class': 'base-list switch_part'})
            interpret = ''
            for xx in base_list.findAll('span'):
                for yy in base_list.findAll('p'):
                    interpret += xx.string + yy.string
            # interpret = [x.string + y.string for (x,y) in (base_list.findAll('span'), base_list.findAll('p'))]
            interpret = re.sub('[\s+]', '', interpret)
            print(interpret)
            if re.search('名词复数|第三人称单数|过去式|过去分词|现在分词|三单形式', interpret) != None:
                print('This word is ignored!\n')
                match = re.search('[a-z]{2,}.*(名词复数|第三人称单数|过去式|过去分词|现在分词|三单形式)', interpret)
                word = re.findall('[a-z]+', match.group())
                print(word)
                wordList.append(max(word, key=len))
                print('This word is added to list: %s' % max(word, key=len))
            else:
                fid.write(headword)
                fid.write('\n word rate: %d \n' % wordRate)
                fid.write('\n %s \n\n' % interpret)

            wordDict[headword] = {'wordRate': wordRate, 'pronounce:': None, 'interpret:': interpret}
            # time.sleep(random.random() * 10)
            # with open('dumpfile.pk', 'wb') as f:
            #     pickle.dump(wordDict, f)
