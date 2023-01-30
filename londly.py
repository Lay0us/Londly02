# 调用各类插件获取子域名信息

# -*- coding:utf-8 -*-

import sys
import os
# from gevent import monkey
# monkey.patch_all()
import urllib3
import xlrd
import openpyxl
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
from uuid import uuid4
import dns.resolver
import re
from threading import Thread
from IPy import IP
import shutil
from collections import Counter
from queue import Queue
from urllib.parse import urlparse
from termcolor import cprint
from optparse import OptionParser
import os
import platform
from uuid import uuid4
import csv
import time
import socket
import socks
import configparser
from tqdm import *
from colorama import Fore
import requests
def BruteDomain(domain):
    path=os.getcwd()
    if os.path.exists(path + r"/url.txt"):
        os.remove(path + r"/url.txt")
        os.remove(path + r"/ksubdomain.txt")
        # os.remove("url.txt")
        os.remove("nucleiresult.txt")
    cprint('-' * 50 + '正在调用oneforall，配置oneforall API效果更佳' + '-' * 50, 'green')
    print(os.system('python3 OneForAll/oneforall.py --target ' + domain + ' run'))
    outputFile=r"OneForAll/results/" + domain + ".csv"
    if not os.path.exists(outputFile):
        exit("Not found the OneForAll's output file ")
    return outputFile
def csvcheck(domain):
    path=os.getcwd()
    with open(path+r"/OneForAll/results/"+domain+".csv","r") as f:
        reader=csv.reader(f)
        for i in reader:
            read=i[5]
            file = open(path+r"/url.txt", "a")
            file.write(read + "\n")
def ksub(domain):
    path = os.getcwd()
    if os.path.exists(path + r"/ksubdomain.txt"):
        os.remove(path + r'/ksubdomain.txt')
    if os.path.exists(path + r"/d.txt"):
        os.remove(path + r'/d.txt')
    os.system('./ksubdomain/ksubdomain -d ' + domain + ' -full ' + r' -o ' + path + r'/d.txt')
    path = os.getcwd()
    dir = path + r"/d.txt"
    list = []
    with open(dir, encoding='utf-8') as dir:
        c = dir.readlines()
        for i in c:
            d = i.split(" => ")
            list.append(d[0])
    for i in list:
        file = open(path + r"/ksubdomain.txt", "a")
        file.write(i + "\n")
    if os.path.exists(path + r"/d.txt"):
        os.remove(path + r'/d.txt')
# 文件合并
def merge(domain):
    path = os.getcwd()
    file1 = path + r'/url.txt'
    file2 = path + r'/ksubdomain.txt'
    f1 = open(file1, 'a', encoding='utf-8')
    with open(file2, 'r', encoding='utf-8') as f2:
        f1.write('\n')
        for i in f2:
            f1.write(i)
    if os.path.exists(path + r"/.ksubdomain.txt"):
        os.remove(path + r'ksubdomain.txt')
def finger(domain):
    cprint('-' * 50 + '正在调用Finger进行重点资产和指纹识别!!' + '-' * 50, 'green')
    path=os.getcwd()
    print(os.system('python3 Finger/Finger.py -f ' + path+r"/url.txt"))
    output1 = os.getcwd()
    files = output1 + r"/Finger/output/"
    b = os.listdir(files)
    for j in b:
        # jiuwenjianjia
        new1 = output1 + r"/Finger/output/" + j
        # xin wenjianjia
        new2 = output1 + r"/result/onedomain/" + domain + '.xlsx'
    os.rename(new1, new2)
    new = output1 + r"/result/onedomain"
    c = os.listdir(files)
    for f in c:
        shutil.move(files + f, new)
    if os.path.exists(path+r"/url.txt"):
        os.remove(path+r'/url.txt')

def Observer(domain):
    cprint('-' * 50 + '正在对所有子域名进行指纹识别!!' + '-' * 50, 'green')
    path = os.getcwd()
    path1 = path + r'/result/onedomain/'+domain+'.xlsx'
    wb = xlrd.open_workbook(path1)
    sh = wb.sheet_by_name('Finger scan')
    lie = sh.col_values(colx=0, start_rowx=1, end_rowx=None)
    for i in lie:
        file = open(path + r"/url.txt", "a")
        file.write(i + "\n")
    os.system('./Observer/observer -f ' + path + r"/url.txt -c" + path + r'/result/onedomain/' + domain+'Observer.txt')
def xray_nuclei(domain):
    cprint('-' * 50 + '正在对所有子域名进行漏扫!!' + '-' * 50, 'green')
    if os.path.exists("url.txt"):
        os.system('./nuclei -l url.txt -s medium,high,critical -o nucleiresult.txt')
        os.system('./xray_linux_amd64 webscan -url-file url.txt --html-output xray.html')
        # os.remove("url.txt")
        # os.remove("ksubdomain.txt")
# 获取one 域名
def run_subdomain():
    OneForAll_File = BruteDomain(domain)
    csvcheck(domain)
    ksub(domain)
    merge(domain)
    finger(domain)
    Observer(domain)
    xray_nuclei(domain)

def banner():
    banner = '''   
                                                      
        __                                __  __           
|  \                              |  \|  \          
| $$      ______   _______    ____| $$| $$ __    __ 
| $$     /      \ |       \  /      $$| $$|  \  |  \
| $$    |  $$$$$$\| $$$$$$$\|  $$$$$$$| $$| $$  | $$
| $$    | $$  | $$| $$  | $$| $$  | $$| $$| $$  | $$
| $$____| $$__/ $$| $$  | $$| $$__| $$| $$| $$__/ $$
| $$     \$$    $$| $$  | $$ \$$    $$| $$ \$$    $$
 \$$$$$$$$\$$$$$$  \$$   \$$  \$$$$$$$ \$$ _\$$$$$$$
                                          |  \__| $$
                                           \$$    $$
                                            \$$$$$$ 
  `----'          `-'----'                       
                                                                                                 
                                                  
       
    
   
'''
    print(banner)
# 初始配置
def _init():
    global domain
    banner()
    usage = '\n\t' \
            'python3 %prog -d domain.com\n\t' \

    parse = OptionParser(usage=usage)
    parse.add_option('-d', '--domain', dest='domain', type='string', help='target domain')
    options, args = parse.parse_args()
    domain = options.domain

    if domain:
        cprint('-' * 50 + 'Start {} information collection'.format(domain) + '-' * 50, 'green')
        run_subdomain()

if __name__ == '__main__':
    _init()


