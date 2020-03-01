#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar  2 02:47:27 2020

@author: yasuekouki
"""

import numpy as np
#import pickle
#from keras.models import load_model
import os

os.environ ['KMP_DUPLICATE_LIB_OK'] = 'True'

#with open('make_monogatari/kana_chars_monogatari.pickle', mode='rb') as f:
#    chars_list = pickle.load(f)

#辞書に廃いていなければTrueを返す
def is_invalid(message, chars_list):
    is_invalid =False
    for char in message:
        if char not in chars_list:
            is_invalid = True
    return is_invalid

# インデックスと文字で辞書を作成
#char_indices = {}
#for i, char in enumerate(chars_list):
#    char_indices[char] = i
#indices_char = {}
#for i, char in enumerate(chars_list):
#    indices_char[i] = char
#    
#n_char = len(chars_list)
#max_length_x = 128

# 文章をone-hot表現に変換する関数
def sentence_to_vector(sentence,max_length_x,n_char,char_indices):
    vector = np.zeros((1, max_length_x, n_char), dtype=np.bool)
    for j, char in enumerate(sentence):
        vector[0][j][char_indices[char]] = 1
    return vector

#encoder_model = load_model('make_monogatari/model/encoder_model.h5')
#decoder_model = load_model('make_monogatari/model/decoder_model.h5')

def respond(message, max_length_x, n_char, char_indices, indices_char, encoder_model, decoder_model, beta=5):
    vec = sentence_to_vector(message,max_length_x,n_char,char_indices)  # 文字列をone-hot表現に変換
    state_value = encoder_model.predict(vec)
    y_decoder = np.zeros((1, 1, n_char))  # decoderの出力を格納する配列
    y_decoder[0][0][char_indices['\t']] = 1  # decoderの最初の入力はタブ。one-hot表現にする。

    respond_sentence = ""  # 返答の文字列
    while True:
        y, h = decoder_model.predict([y_decoder, state_value])
        p_power = y[0][0] ** beta  # 確率分布の調整
        next_index = np.random.choice(len(p_power), p=p_power/np.sum(p_power)) 
        next_char = indices_char[next_index]  # 次の文字
        
        if (next_char == "\n" or len(respond_sentence) >= max_length_x):
            break  # 次の文字が改行のとき、もしくは最大文字数を超えたときは終了
            
        respond_sentence += next_char
        y_decoder = np.zeros((1, 1, n_char))  # 次の時刻の入力
        y_decoder[0][0][next_index] = 1

        state_value = h  # 次の時刻の状態

    return respond_sentence

def make_story():

    bot_name = "物語bot"
    your_name = input("おなまえをおしえてください。:")
    print()
    
    print(bot_name + ": " + "こんにちは、" + your_name + "さん。")
    message = ""
    while message != "さようなら。":
        
        while True:
            message = input(your_name + ": ")
            if not is_invalid(message):
                break
            else:
                print(bot_name + ": ひらがなか、カタカナをつかってください。")
                
        response = respond(message)
        print(bot_name + ": " + response)
        
#make_story()