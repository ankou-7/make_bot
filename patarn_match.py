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
#漫画ごとにクイズを作成
def bun_all_patarn(manga_list):
    pt_tapple={}
    bunlist=kuuhakujokyo(re.split('[\n。\t]', manga_list))
    for i in range(len(bunlist)):
        if ("による日本の少年漫画作品" in bunlist[i] and '『' in bunlist[i] and '』' in bunlist[i]):
            pt_tapple[0]=bunlist[i]
        if i < 4:
                if ("通称「" in bunlist[i] and '」' in bunlist[i]):
                    if len(bunlist[i]) < 10:
                        pt_tapple[1]=bunlist[i]
        if i < 5:
                if ("連載中" in bunlist[i] and '『' in bunlist[i] and '』' in bunlist[i]):
                    pt_tapple[2]=bunlist[i]
        if ("題材にした" in bunlist[i]):
            pt_tapple[3]=bunlist[i]
        if ("の新入生" in bunlist[i]):
            pt_tapple[4]=bunlist[i]
            
    return pt_tapple
    
def make_all_quize(pt_tapple,title,n):
    qui=[]
    ans=[]
    for i in pt_tapple.keys():
        if i == 0:
            bun=pt_tapple.get(0)
            a=bun.find("、")
            b=bun.find("による")
            ans.append(bun[a+1:b])
            c=len(qui)
            qui.append(bun.replace(ans[c], "誰")+"ですか？")
        elif i == 1:
            bun=pt_tapple.get(1)
            qui.append(title[n] + "は、" + bun + "と呼ばれているか？\n【はい/いいえ】")
            ans.append("はい")
            qui.append(title[n] + "は、通称何と呼ばれているか？")
            a=bun.replace('通称「', '').replace('」', '')
            ans.append(a)
        elif i == 2:
            bun=pt_tapple.get(2)
            a=bun.find("『")
            b=bun.find("』")
            ans.append(bun[a+1:b])
            qui.append(title[n] + "は何の雑誌で連載しているか？")
                
        elif i == 3:
            bun=pt_tapple.get(3)
            a=bun.find('（')
            ans.append(bun[:a])
            qui.append(title[n] + "は何を題材にした作品か？")
        elif i == 4:
            bun=pt_tapple.get(4)
            a=bun.find("・")
            b=bun.find("は")
            ans.append(bun[a+1:b])
            qui.append(title[n] + "の主人公の名前は？")
    return qui,ans
###############################################################################
    
def rensyu_patarn(kiji_list):
    pt_list={}
    for n in range(len(kiji_list)-1):
        bunlist=kuuhakujokyo(re.split('[\n。\t]', kiji_list[n]))
        for i in range(len(bunlist)):
            if ("の新入生" in bunlist[i]): #and '' in bunlist[i]
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

#if "あ" not in title:
#    print("aa")
#if "弱虫ペダル" in title:
#    print("bb")
#n = title.index("あ")
#kiji = kuuhakujokyo(re.split('[\n。\t]', kiji_list[n]))
#pt_tapple = bun_all_patarn(kiji_list[n])
#print(pt_tapple.get(4))
#print(len(pt_tapple))
#q,a = make_all_quize(pt_tapple,title,n)

#pt_list = rensyu_patarn(kiji_list)
#s="自転車競技（主にロードレース）を題材にした本格的なスポーツ漫画"
#print(s.find("（"))

###print(pt_list.keys())
###print(kiji_list[2327])
#bunlist=kuuhakujokyo(re.split('[\n。\t]', kiji_list[3485]))
##q,a = make_quize2(pt_list,title)
#q,a = make_quize(pt_list)
#Q,A = random_quize(make_quize(pt_list)[0],make_quize(pt_list)[1])
#hinto = make_hinto(A,a)
