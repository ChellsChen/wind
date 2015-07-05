# -*- coding:utf-8 -*-
#    author    :   丁雪峰
#    time      :   2015-02-16 14:49:41
#    email     :   fengidri@yeah.net
#    version   :   1.0.1
import urllib2
import json

import pyvim
import im.imrc as imrc
from im.imrc import feedkeys

from im.handle_base import IM_Base
from pyvim import log as logging

from im.imutils import SelMenu
from im.prompt import abuild

cache={  }

def search_from_db(patten):
    try:
        r = urllib2.urlopen("http://localhost/wubi/search?patten=%s" %
            patten)
        w = json.loads(r.read())
        cache[patten] = w
        return w
    except Exception, e:
        pyvim.echoline(str(e))
        return ([], [])

def search(patten):
    '得到备选的字词'
    words= cache.get( patten )

    if  words:
        return words

    return search_from_db(patten)

def setcount(patten, num):
    w, ass = cache.pop(patten)
    if len(w) -1 < num:
        return
    ww = w[num]
    url = "http://localhost/wubi/setcount?patten=%s&word=%s" % (patten,
            ww.encode('utf8'))
    try:
        urllib2.urlopen(url)
    except Exception, e:
        pyvim.echoline(str(e))

def wubi(patten):
    words, associate = search(''.join(patten))

    abuild(" ", "%s                  " %  patten)

    i = 0
    for w in words:
        abuild(w, "%s.%s" % (i, w))

    for w, k, c  in associate:
        i += 1
        abuild( w, "%s.%s %s"%(i, w, k)})


class IM_Wubi(IM_Base):
    def __init__(self):
        IM_Base.__init__(self)

        self.buffer=[]
        self.index = 0
        self.pmenu = SelMenu()





    def im_lower(self, key ):
        if imrc.count - self.index != 1:  # 保证连续输入
            del self.buffer[:]
        self.index = imrc.count

        self.buffer.append(key)
        self.pmenu.show(self.wubi(self.buffer), 0)

    def cb_backspace(self):
        if not pyvim.pumvisible():
            pyvim.feedkeys('\<bs>', 'n')
            return 0

        if len( self.buffer ) > 1:
            self.buffer.pop()
            self.patten = ''.join(self.buffer)
            self.pmenu.show(self.wubi(self.patten), 0)
        else:
            del self.buffer[:]
            self.pmenu.cencel( )


    def cb_enter(self):
        if pyvim.pumvisible():
            bs = pyvim.str_before_cursor()
            if len(bs) > 0:
                if ord(bs[-1]) > 178:
                    pyvim.feedkeys(r'\<space>', 'n')
            pyvim.feedkeys(r'%s\<C-e>' % self.patten,'n')
            del self.buffer[ : ]
            return 0
        pyvim.feedkeys(r'\<cr>' ,'n')

    def cb_space(self):
        del self.buffer[:]
        if pyvim.pumvisible():
            word = self.pmenu.getselect(1).get('word')
            bs = pyvim.str_before_cursor()
            if len(bs) > 0:
                c = bs[-1]
                o = ord(c)
                if c in ',.!:;?' or \
                       65<= o <=90 or \
                       97<= o <=122 :
                       #48<= o <=57 or\
                    pyvim.feedkeys('\<space>', 'n')
            pyvim.feedkeys(word, 'n')
            return 0
        pyvim.feedkeys('\<space>', 'n')


if __name__ == "__main__":
    pass
