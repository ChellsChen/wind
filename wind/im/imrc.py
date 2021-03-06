# -*- coding:utf-8 -*-
#    author    :   丁雪峰
#    time      :   2015-03-10 18:15:29
#    email     :   fengidri@yeah.net
#    version   :   1.0.1


import os
import string
import pyvim
from pyvim import log
import rc

count = 0  #
_feedkeys = None
SwitchWubi = True

#---------------------------------- event ------------------------------------
__event_cb = {}
def emit_event(event):
    cblist = __event_cb.get(event)
    if not cblist:
        return
    for cb in cblist:
        cb()

def hook(event):
    def fun(h):
        add_hook(event, h)
        return h
    return fun

def add_hook(event, cb):
    cblist = __event_cb.get(event)
    if not cblist:
        __event_cb[event] = [cb]
    else:
        cblist.append(cb)

def rm_hook(event, cb):
    cblist = __event_cb.get(event, [])
    while True:
        if cb in cblist:
            cblist.remove(cb)
        else:
            return

#---------------------------------- hook ------------------------------------
@hook('start')
def start():
    global _feedkeys
    global count
    _feedkeys = Feedkeys()
    count += 1
    rc.IM_KeyIndex += 1

@hook('stop')
def stop():
    _feedkeys.feed()

#---------------------------------- feedkeys----------------------------------

class IMRedirectStop(Exception):
    pass

class Feedkeys(object):
    def __new__(cls, *args, **kw):
        "单例模式"
        if not hasattr(cls, '_instance'):
            orig = super(Feedkeys, cls)
            cls._instance = orig.__new__(cls, *args, **kw)
            Feedkeys._feed_ = []
        return cls._instance
    def __init__(self):
        del Feedkeys._feed_[:]

    def append(self, k):
        Feedkeys._feed_.append(k)

    def feed(self):
        pyvim.feedkeys(Feedkeys._feed_)

def feedkeys(k):
    _feedkeys.append(k)


