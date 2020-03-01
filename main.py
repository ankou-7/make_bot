# インポートするライブラリ
from flask import Flask, request, abort
from linebot import (
   LineBotApi, WebhookHandler
)
from linebot.exceptions import (
   InvalidSignatureError
)
from linebot.models import (
   FollowEvent, MessageEvent, TextMessage, TextSendMessage, ImageMessage, ImageSendMessage, TemplateSendMessage, ButtonsTemplate, PostbackTemplateAction, MessageTemplateAction, URITemplateAction,
       QuickReplyButton, MessageAction, QuickReply,
)
#from keras.models import load_model

import os
import wikipedia
import patarn_match as pat
import heroku_db as qui
import make_monogatari as mono
import pickle

# 軽量なウェブアプリケーションフレームワーク:Flask
app = Flask(__name__)
#環境変数からLINE Access Tokenを設定
LINE_CHANNEL_ACCESS_TOKEN = os.environ["LINE_CHANNEL_ACCESS_TOKEN"]
#環境変数からLINE Channel Secretを設定
LINE_CHANNEL_SECRET = os.environ["LINE_CHANNEL_SECRET"]
line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SECRET)

wikipedia.set_lang("ja") # 追加

@app.route("/callback", methods=['POST'])
def callback():
   # get X-Line-Signature header value
   signature = request.headers['X-Line-Signature']
   # get request body as text
   body = request.get_data(as_text=True)
   app.logger.info("Request body: " + body)
   # handle webhook body
   try:
       handler.handle(body, signature)
   except InvalidSignatureError:
       abort(400)
   return 'OK'

#漫画の記事を読み込んでkiji_listに格納
kiji_list = pat.make_kiji()
#漫画のタイトルを格納
title = pat.titlename(kiji_list)
#記事から特定の文を抽出
pt_list=pat.bun_patarn(kiji_list)

####################################
with open('make_monogatari/kana_chars_monogatari.pickle', mode='rb') as f:
    chars_list = pickle.load(f)

char_indices = {}
for i, char in enumerate(chars_list):
    char_indices[char] = i
indices_char = {}
for i, char in enumerate(chars_list):
    indices_char[i] = char
    
n_char = len(chars_list)
max_length_x = 128

#encoder_model = load_model('make_monogatari/model/encoder_model.h5')
#decoder_model = load_model('make_monogatari/model/decoder_model.h5')
###################################

# MessageEvent
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    
    activity=qui.get_db()[0]
    
    if activity == 'menu':
        if event.type == "message":
            if (event.message.text == "へいbot") or (event.message.text == "bot"):
                line_bot_api.reply_message(
                   event.reply_token,
                   [
                        TextSendMessage(text="お疲れ様です" + chr(0x10002D)),
                        TextSendMessage(text="メニューから選んでね！！\n1 : クイズをする\n2 : お話をする\n3 : 物語を作る\n4 : (漫画を)検索する"),
                    ]
                )
            elif (event.message.text == "ありがとう！") or (event.message.text == "ありがとう") or (event.message.text == "ありがと！") or (event.message.text == "ありがと"):
                line_bot_api.reply_message(
                    event.reply_token,
                    [
                        TextSendMessage(text="どういたしまして！またね" + chr(0x100033)),
                    ]
            )
            elif (event.message.text == "1") or (event.message.text == "クイズしようぜ"):
                q_list,a_list = pat.make_quize(pt_list) #問題と答えをリストにして格納
                Q,A = pat.random_quize(q_list,a_list) #格納したリストからランダムに１つ取り出す
                hinto = pat.make_hinto(A,a_list)
                qui.change_quize_db(Q,A,hinto[0],hinto[1],hinto[2],hinto[3])
                qui.change_db("quize","activity")
                line_bot_api.reply_message(
                        event.reply_token,
                        [
                            TextSendMessage(text="やりましょう"),
                            TextSendMessage(text="問題を出すので答えて下さい"),
                            TextSendMessage(text="【問題】\n" + Q),
                        ]
                )
            elif (event.message.text == "3"):
                qui.change_db("make_story","activity")
                #mono.make_story()
                line_bot_api.reply_message(
                        event.reply_token,
                        [
                            TextSendMessage(text="いきますよ"),
                        ]
                )
            elif (event.message.text == "4") or (event.message.text == "検索したい"):
                qui.change_db("wiki","activity")
                line_bot_api.reply_message(
                        event.reply_token,
                        [
                            TextSendMessage(text="検索したい語句を入力してね"),
                        ]
                )
            elif (event.message.text == "終了") or (event.message.text == "バイバイ"):
                qui.change_db("menu","activity")
                line_bot_api.reply_message(
                        event.reply_token,
                        [
                            TextSendMessage(text="またね"),
                        ]
                )
            else:
                line_bot_api.reply_message(
                    event.reply_token,
                    [
                        TextSendMessage(text="ちょっと何言ってるかわからないな"+ chr(0x100029) + chr(0x100098)),
                        TextSendMessage(text="もう一回いって"),
                    ]
                )
    if activity == 'quize':
        if event.type == "message":
            flag=int(qui.get_db()[1])
            answer=qui.get_quize_db()[1]
            h1,h2,h3,h4 = qui.get_quize_db()[2],qui.get_quize_db()[3],qui.get_quize_db()[4],qui.get_quize_db()[5]
            if (flag==0):
                if (event.message.text == answer):
                    qui.change_db("1","flag")
                    line_bot_api.reply_message(
                       event.reply_token,
                       [
                            TextSendMessage(text="正解です。\n素晴らしいですね！！"),
                            TextSendMessage(text="もう一問やりますか？\n【はい/いいえ】"),
                        ]
                    )
                elif (event.message.text == "ヒント"):
                    
                    line_bot_api.reply_message(
                       event.reply_token,
                       [
                            TextSendMessage(text="4択にしたよ。\n4つの中から選んでね！！"),
                            TextSendMessage(text="1 " + h1 + "\n2 " + h2 + "\n3 " + h3 + "\n4 " + h4),
                        ]
                    )
                elif (event.message.text != "ヒント") or (event.message.text != answer):
                    qui.change_db("1","flag")
                    line_bot_api.reply_message(
                       event.reply_token,
                       [
                            TextSendMessage(text="負正解です。\n正解は"+answer+"です"),
                            TextSendMessage(text="もう一問やりますか？\n【はい/いいえ】"),
                        ]
                    )
            elif(flag==1):
                if (event.message.text == "はい"):
                    q_list,a_list = pat.make_quize(pt_list) #問題と答えをリストにして格納
                    Q,A = pat.random_quize(q_list,a_list) #格納したリストからランダムに１つ取り出す
                    hinto = pat.make_hinto(A,a_list)
                    qui.change_quize_db(Q,A,hinto[0],hinto[1],hinto[2],hinto[3])
                    qui.change_db("0","flag")
                    line_bot_api.reply_message(
                            event.reply_token,
                            [
                                TextSendMessage(text="【問題】\n" + Q),
                            ]
                    )
                elif (event.message.text == "いいえ"):
                    qui.change_db("0","flag")
                    qui.change_db("menu","activity")
                    line_bot_api.reply_message(
                            event.reply_token,
                            [
                                TextSendMessage(text="またね"),
                            ]
                    )
                else:
                    line_bot_api.reply_message(
                            event.reply_token,
                            [
                                TextSendMessage(text="【はい/いいえ】で答えてね"),
                            ]
                    )
    if activity == 'make_story':
        if event.type == "message":
            if (event.message.text != "終了"):
                message = event.message.text #入力文
                if mono.is_invalid(message, chars_list):
                    line_bot_api.reply_message(
                            event.reply_token,
                            [
                                    TextSendMessage(text="ひらがなか、カタカナで入力してね。")
                            ]
                    )
                else:
                    line_bot_api.reply_message(
                            event.reply_token,
                            [
                                    TextSendMessage(text=mono.respond(message, max_length_x, n_char, char_indices, indices_char, encoder_model, decoder_model, beta=5))
                            ]
                    )
            elif (event.message.text == "終了"):
                qui.change_db("menu","activity")
                line_bot_api.reply_message(
                        event.reply_token,
                        [
                            TextSendMessage(text="またね"),
                        ]
            )
    if activity == 'wiki':
        if event.type == "message":
            if (event.message.text != "終了"):
                send_message = event.message.text
                #正常に検索結果が返った場合
                try:
                    wikipedia_page = wikipedia.page(send_message)
                    # wikipedia.page()の処理で、ページ情報が取得できれば、以下のようにタイトル、リンク、サマリーが取得できる。
                    wikipedia_title = wikipedia_page.title
                    wikipedia_url = wikipedia_page.url
                    wikipedia_summary = wikipedia.summary(send_message)
                    reply_message = '【' + wikipedia_title + '】\n' + wikipedia_summary + '\n\n' + '【詳しくはこちら】\n' + wikipedia_url
                # ページが見つからなかった場合
                except wikipedia.exceptions.PageError:
                    reply_message = '【' + send_message + '】\nについての情報は見つかりませんでした。'
                # 曖昧さ回避にひっかかった場合
                except wikipedia.exceptions.DisambiguationError as e:
                    disambiguation_list = e.options
                    reply_message = '複数の候補が返ってきました。以下の候補から、お探しの用語に近いものを再入力してください。\n\n'
                    for word in disambiguation_list:
                        reply_message += '・' + word + '\n'
                line_bot_api.reply_message(
                    event.reply_token,
                    TextSendMessage(text=reply_message)
                )
            elif (event.message.text == "終了"):
                qui.change_db("menu","activity")
                line_bot_api.reply_message(
                        event.reply_token,
                        [
                            TextSendMessage(text="またね"),
                        ]
            )
    #word = event.message.text
    #manga_title = pat.titlename(title_list)
    #text = manga_title[int(word)]
    
    #line_bot_api.reply_message(
       #event.reply_token,
       #TextSendMessage(text=text)
    #S)

#def response_message(event):
 #   language_list = ["Ruby", "Python", "PHP", "Java", "C"]

  #  items = [QuickReplyButton(action=MessageAction(label=f"{language}", text=f"{language}が好き")) for language in language_list]

   # messages = TextSendMessage(text="どの言語が好きですか？",
    #                           quick_reply=QuickReply(items=items))

    #line_bot_api.reply_message(event.reply_token, messages=messages)


if __name__ == "__main__":
   port = int(os.getenv("PORT"))
   app.run(host="0.0.0.0", port=port)
