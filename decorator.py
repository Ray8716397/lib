# -*- encoding: utf-8 -*-
'''
@File    :   decorator.py    
@Modify Time      @Author    @Version    @Desciption
------------      -------    --------    -----------
2023/1/6 上午10:14   ray      1.0         None
'''

# import lib
from functools import wraps
import time
import datetime


def how_much_time(method):
    @wraps(method)
    def wrapper(*args, **kwargs):
        start_time = datetime.datetime.now()
        res = method(*args, **kwargs)
        print(datetime.datetime.now() - start_time)
        return res

    return wrapper


@how_much_time
def test(k):
    time.sleep(1)
    k = k + 1
    return k


if __name__ == '__main__':
    test(22)
