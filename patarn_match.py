#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb 21 03:04:00 2020

@author: yasuekouki
"""

import re
import random

def kuuhakujokyo(list):
    count=0;
    list.pop(0);
    for i in range(len(list)):
        if len(list[count])==0:
            list.pop(count);
            count=count-1;
        count=count+1;
    
    list.pop(len(list)-1);
    return list;

#漫画タイトルを取り出して格納
def titlename(list):
    titlelist=[]
    for i in range(len(list)):
        count=0
        flag=0
        for m in re.finditer('"', list[i]):
            title = m.span()
            count=count+1
            if count==5:
                title_first=title[0]
                flag=1
            elif count==6:
                title_end=title[0]
        if flag==1:
            titlelist.append(list[i][title_first+1:title_end])
            flag=0

    return titlelist

#漫画記事を読み込む
def make_kiji():
    kiji1='wikimanga.txt'
    f = open(kiji1,'r',encoding='utf-8')
    list = f.read().split('</doc>')# ファイル終端まで全て読んだデータを返す
    f.close()
    #title=titlename(list)
    
    return list

###############################################################################
    
def bun_patarn(kiji_list):
    pt_list={}
    patarn="による日本の少年漫画作品"
    for n in range(len(kiji_list)-1):
        bunlist=kuuhakujokyo(re.split('[\n。\t]', kiji_list[n]))
        for i in range(len(bunlist)):
            if (patarn in bunlist[i] and '『' in bunlist[i] and '』' in bunlist[i]):
                pt_list[n]=bunlist[i]
                #print("番号%d : %s" % (n,bunlist[i]))
    return pt_list
                
def make_quize(pt_list):
    qui=[]
    ans=[]
    bunlist=list(pt_list.values())
    for i in range(len(bunlist)):
        if i==5:
            continue
        c=len(qui)
        k=bunlist[i].find("による")
        j=bunlist[i].find("、")
        ans.append(bunlist[i][j+1:k])
        q=bunlist[i].replace(ans[c], "誰")
        qui.append(q+"ですか？")
    return qui,ans

###############################################################################
    
def bun_patarn2(kiji_list):
    pt_list={}
    patarn="通称「"
    for n in range(len(kiji_list)-1):
        bunlist=kuuhakujokyo(re.split('[\n。\t]', kiji_list[n]))
        for i in range(len(bunlist)):
            if i < 4:
                if (patarn in bunlist[i] and '」' in bunlist[i]):
                    if len(bunlist[i]) < 10:
                        pt_list[n]=bunlist[i]
                        print("番号%d : %s" % (n,bunlist[i]))
    return pt_list

def make_quize2(pt_list,title):
    qui=[]
    ans=[]
    bunlist=list(pt_list.values())
    title_num = list(pt_list.keys())
    for i in range(len(bunlist)):
        qui.append(title[title_num[i]] + "は、" + bunlist[i] + "と呼ばれているか？\n【はい/いいえ】")
        ans.append("はい")
        qui.append(title[title_num[i]] + "は、通称何と呼ばれているか？")
        a=bunlist[i].replace('通称「', '').replace('」', '')
        ans.append(a)
    return qui,ans

###############################################################################
def bun_patarn3(kiji_list):
    pt_list={}
    patarn="連載中"
    for n in range(len(kiji_list)-1):
        bunlist=kuuhakujokyo(re.split('[\n。\t]', kiji_list[n]))
        for i in range(len(bunlist)):
            if i < 5:
                if (patarn in bunlist[i] and '『' in bunlist[i] and '』' in bunlist[i]):
                    pt_list[n]=bunlist[i]
                    print("番号%d : %s" % (n,bunlist[i]))
    return pt_list

def make_quize3(pt_list,title):
    qui=[]
    ans=[]
    bunlist=list(pt_list.values())
    title_num = list(pt_list.keys())
    for i in range(len(bunlist)):
        qui.append(title[title_num[i]] + "は、" + bunlist[i] + "と呼ばれているか？\n【はい/いいえ】")
        ans.append("はい")
        qui.append(title[title_num[i]] + "は、通称何と呼ばれているか？")
        a=bunlist[i].replace('通称「', '').replace('」', '')
        ans.append(a)
    return qui,ans
    
###############################################################################
    
def rensyu_patarn(kiji_list):
    pt_list={}
    for n in range(len(kiji_list)-1):
        bunlist=kuuhakujokyo(re.split('[\n。\t]', kiji_list[n]))
        for i in range(len(bunlist)):
            if ("主人公" in bunlist[i]): #and '' in bunlist[i]
                pt_list[n]=bunlist[i]
                print("番号%d : %s" % (n,bunlist[i]))
    return pt_list
    
###############################################################################
    
def random_quize(qui,ans):
    n = random.randrange(len(qui))
    return qui[n], ans[n]
    
def make_hinto(ans,ans_list):
    hinto=[]
    a = ans_list.index(ans) #答えが格納されているインデックスクを返す
    while len(hinto) < 3:
        n = random.randrange(len(ans_list))
        if n != a:
            hinto.append(ans_list[n])
    hinto.append(ans)
    random.shuffle(hinto)
    return hinto

#kiji_list = make_kiji()
#title = titlename(kiji_list)
#pt_list=bun_patarn3(kiji_list)
###pt_list = rensyu_patarn(kiji_list)
###print(pt_list.keys())
###print(kiji_list[2327])
#bunlist=kuuhakujokyo(re.split('[\n。\t]', kiji_list[3485]))
##q,a = make_quize2(pt_list,title)
#q,a = make_quize(pt_list)
#Q,A = random_quize(make_quize(pt_list)[0],make_quize(pt_list)[1])
#hinto = make_hinto(A,a)
