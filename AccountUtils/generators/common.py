# coding=utf-8
"""通用小工具。"""
import time


def calendar_time():
    """当前日期字符串 YYYY-MM-DD"""
    return time.strftime("%Y-%m-%d", time.localtime())
