# -*- coding:utf-8 -*-
#    author    :   丁雪峰
#    time      :   2015-03-31 11:15:36
#    email     :   fengidri@yeah.net
#    version   :   1.0.1
from node import Node, Leaf
from listwin import LIST
import logging
import utils

def inputstream(key):
    logging.error('inputstream: %s' % key)

def handle(name, ev):
    # 目前这种 UI 事件的方式并不好.
    # 后期应该通过判断用户在哪一个 ui object 里输入, 即把输入流引入到这个
    # ui object. 由这个 object 自己完成对于 key event 的处理.
    """
        @paser: name ui object name
        @ev:    method of the object
    """
    obj = utils.Objects.get(name)
    if not obj:
        return

    if not hasattr(obj, ev):
        return

    getattr(obj, ev)()
