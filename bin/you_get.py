#!/usr/bin/python
# -*- coding:utf-8 -*-

from os import chdir, system
import subprocess

def get_u2b_info(url, debug = False):
    "使用you-get解析youtube页面并返回结果"

    cmd = "you-get --info " + url
    exec_cmd = subprocess.Popen(cmd, shell = True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    log = exec_cmd.communicate()
    if debug:
        print(log[0])
    return log[0]

def format_log(log):
    "格式化返回的log"

    lines = log.split("\n")
    List = [];
    trim = '';
    idx = 0;
    length = 4;
    i = 0;
    arrIndex = [];
    filterWord = ['-itag:','container:','quality:','size:'];
    for line in lines:
    	trim=''.join(line.split());
    	for fw in filterWord:
    		if fw in trim:
    			List.append(trim);
    for index,v in enumerate(List):
    	if '-itag' in v:
    		arrIndex.append(index);
    groups = [];
    for idx,v in enumerate(arrIndex):
    	i = arrIndex[idx];
    	if idx==len(arrIndex)-1:
    		j = len(List);
    	elif idx<len(arrIndex)-1:
    		j = arrIndex[idx+1]-1;
    	myslice=slice(i,j);
    	groups.append(List[myslice]);
    return groups

def dl_u2b(dir, itag, url):
    chdir(dir)
    print("正在将视频下载至" + dir + "目录...")
    system("you-get --itag=" + itag + " " + url)
    print("Finished")

def get_soundcloud_info(url):
    cmd = "you-get --info " + url
    exec_cmd = subprocess.Popen(cmd, shell = True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    log = exec_cmd.communicate()
    lines = log[0].split("\n")
    lines.pop(-1);lines.pop(-1)
    list = []
    for line in lines:
        list.append(line.split("      "))
    return list

def dl_soundcloud(dir, url):
    chdir(dir)
    info = get_soundcloud_info(url)
    print("正在下载" + info[1][1] + "至" + dir + "目录(" + info[3][1] + ")")
    system("you-get " + url)


if __name__ == "__main__": # debug, 会删除
    dl_u2b("/home/pi/Videos", "299", "https://www.youtube.com/watch?v=dX3m8HiL-5c")
