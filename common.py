# -*- encoding: utf-8 -*-
'''
@File    :   common.py    
@Modify Time      @Author    @Version    @Desciption
------------      -------    --------    -----------
2022/12/13 下午2:55   ray      1.0         None
'''

# import lib
import re
import os

# 去重
re.sub(r'(\n)\1+', r'\1', para['context']).split('\n')

# 遍历文件夹
def walkFile(file):
    for root, dirs, files in os.walk(file):

        # root 表示当前正在访问的文件夹路径
        # dirs 表示该文件夹下的子目录名list
        # files 表示该文件夹下的文件list

        # 遍历文件
        for f in files:
            print(os.path.join(root, f))

        # 遍历所有的文件夹
        for d in dirs:
            print(os.path.join(root, d))
