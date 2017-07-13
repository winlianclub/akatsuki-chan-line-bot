# -*- coding: utf-8 -*-

#  Licensed under the Apache License, Version 2.0 (the "License"); you may
#  not use this file except in compliance with the License. You may obtain
#  a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#  WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#  License for the specific language governing permissions and limitations
#  under the License.

from __future__ import unicode_literals

import errno
import os
import sys
import tempfile
from var import *
from re import search
from random import choice
from argparse import ArgumentParser

from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
    SourceUser, SourceGroup, SourceRoom,
    TemplateSendMessage, ConfirmTemplate, MessageTemplateAction,
    ButtonsTemplate, URITemplateAction, PostbackTemplateAction,
    PostbackEvent,
    StickerMessage, StickerSendMessage, LocationMessage, LocationSendMessage,
    ImageMessage, VideoMessage, AudioMessage,
    ImageSendMessage, ImageSendMessage, VideoSendMessage, AudioSendMessage,
    UnfollowEvent, FollowEvent, JoinEvent, LeaveEvent, BeaconEvent
)

app = Flask(__name__)

channel_access_token = str(os.environ.get('CHANNEL_ACCESS_TOKEN'))
channel_secret = str(os.environ.get('CHANNEL_SECRET'))
master_id = str(os.environ.get('MASTER_ID'))
altia_id = str(os.environ.get('ALTIA_ID'))
line_bot_api = LineBotApi(channel_access_token)
handler = WebhookHandler(channel_secret)

img_url_tag_gab = img_url_tag.copy()
img_url_tag_gab.update(altia_id)

#static_tmp_path = os.path.join(os.path.dirname(__file__), 'static', 'tmp')#

"""
# function for create tmp dir for download content
def make_static_tmp_dir():
    try:
        os.makedirs(static_tmp_path)
    except OSError as exc:
        if exc.errno == errno.EEXIST and os.path.isdir(static_tmp_path):
            pass
        else:
            raise
"""

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

@handler.add(MessageEvent, message=TextMessage)
def handle_text_message(event):
    text = event.message.text
    if text[0] == '#':
        cmd = search(r'\#(\w*)\s*(.*)', text)
        #profile = line_bot_api.get_profile(event.source.user_id)
        if (cmd.group(1) == 'su') and (event.source.user_id == master_id):
            if cmd.group(2) == 'groupid':
                line_bot_api.reply_message(event.reply_token, TextMessage(text=event.source.group_id))
            elif cmd.group(2) == 'acchan':
                line_bot_api.reply_message(event.reply_token, TextMessage(text='Ya Master?'))
            elif cmd.group(2) == 'thanks':
                line_bot_api.reply_message(event.reply_token, TextMessage(text='Anytime Master'))
            else:
                line_bot_api.reply_message(event.reply_token, TextMessage(text='Kenapa Master?'))
        # bolehkah
        elif cmd.group(1) == 'bolehkah':
            pass
        # bye
        elif cmd.group() == '#bye':
            if isinstance(event.source, SourceGroup) or isinstance(event.source, SourceRoom):
                image_message = ImageSendMessage(
                    original_content_url=img_url_tag[cmd.group(1)][0],
                    preview_image_url=img_url_tag[cmd.group(1)][1])
                text_message1 = TextMessage(text='"There are things you can only learn by accepting your weakness."')
                text_message2 = TextMessage(text='Selamat tinggal ^_^')
                line_bot_api.reply_message(event.reply_token, [image_message, text_message1, text_message2])
                try:
                    line_bot_api.leave_group(event.source.group_id)
                except:
                    line_bot_api.leave_room(event.source.room_id)   
            else:
                line_bot_api.reply_message(
                    event.reply_token,
                    TextMessage(text="Mana bisa keluar dari personal chat qaqa ^-^"))
        # gombal
        elif cmd.group(1) == 'gombal':
            if cmd.group(2) != '':
                txt = 'eh ' + cmd.group(2) + ',\n' + choice(list_gombal)
            else:
                txt = choice(list_gombal)
            line_bot_api.reply_message(
                event.reply_token, TextSendMessage(text=txt))
        # help
        elif cmd.group(1) == 'help':
            if cmd.group() == '#help':
                srt = sorted(daftar_cmd)
                txt = """list perintah : """+ ', '.join(srt) + """\nGunakan '#' di awal perintah\n\nuntuk lebih jelas ketik '#help <perintah>'\ncontoh: #help jurus"""
                line_bot_api.reply_message(
                    event.reply_token, TextSendMessage(text=txt))
            elif cmd.group(2) in daftar_cmd:
                f = open('helps/'+cmd.group(2)+'.txt', 'r')
                help_text = f.read()
                txt = "Bantuan untuk : '#"+cmd.group(2)+"'"
                line_bot_api.reply_message(
                    event.reply_token, [TextSendMessage(text=txt), TextSendMessage(text=help_text)])
                f.close()
            else:
                txt = 'Berikut list perintah : '+', '.join(sorted(daftar_cmd))
                line_bot_api.reply_message(
                    event.reply_token, [
                    TextSendMessage(text='Mana ada perintah itu'),
                    TextSendMessage(text=txt)])
        # info
        elif cmd.group() == '#info':
            line_bot_api.reply_message(
                event.reply_token, TextSendMessage(text="""Dibuat sebagai project pembelajaran oleh: Ikraduya Edian(line:ikraduya) dan kontributor: Farisan, Radit, Ojan, Jodi, Altia
                                                        Kritik dan saran mohon dikirimkan lewat (line:ikraduya), terima kasih.                                                       
                                                        """))
        # jurus
        elif cmd.group(1) == 'jurus':
            if cmd.group(2) in daftar_jurus:
                f = open('statics/' + daftar_jurus[cmd.group(2)], 'r')
                txt = ('JURUS '+cmd.group(2)).upper() + '!'
                txt2 = str(f.read())
                line_bot_api.reply_message(
                    event.reply_token, [TextSendMessage(text=txt),
                                        TextSendMessage(text=txt2)])
                f.close()
            elif cmd.group(2) == '':
                line_bot_api.reply_message(
                    event.reply_token, TextSendMessage(text='Jurus apa qaqa??'))
            else:
                line_bot_api.reply_message(
                    event.reply_token, TextSendMessage(text="Mana ada jurus begitu.. untuk melihat list jurus ketik '#ougi'"))
        # tag
        elif cmd.group(1) == 'tag':
            if isinstance(event.source, SourceGroup):
                if event.source.group_id == altia_id:
                    pake_ini = img_url_tag_gab
                else:
                    pake_ini = img_url_tag
            if cmd.group(2) in img_url_tag:
                image_message = ImageSendMessage(
                    original_content_url=pake_ini[cmd.group(2)][0],
                    preview_image_url=pake_ini[cmd.group(2)][1])
                line_bot_api.reply_message(event.reply_token, image_message)
            else:
                line_bot_api.reply_message(
                    event.reply_token, TextSendMessage(text="Untuk melihat list tag ketik '#taglist'"))
        # taglist
        elif cmd.group() == '#taglist':
            if isinstance(event.source, SourceGroup):
                if event.source.group_id == altia_id:
                    pake_ini = img_url_tag_gab
                else:
                    pake_ini = img_url_tag
            srt = sorted(pake_ini)
            txt = 'Berikut list tag : '+', '.join(srt)
            line_bot_api.reply_message(
                    event.reply_token, TextSendMessage(text=txt))
        # so
        elif cmd.group(1) == 'so':
            txt = ' '.join((cmd.group(2).replace(" ","")).upper())
            line_bot_api.reply_message(
                    event.reply_token, TextSendMessage(text=txt))
        # ougi
        elif cmd.group() == '#ougi':
            srt = sorted(daftar_jurus)
            txt = 'Daftar jurus : '+', '.join(srt)
            line_bot_api.reply_message(
                    event.reply_token, TextSendMessage(text=txt))
        # panggil
        elif cmd.group() == '#panggil':
            line_bot_api.reply_message(
                event.reply_token, TextSendMessage(text="It's curry night!"))
        # profil
        elif cmd.group() == '#profil':
            if isinstance(event.source, SourceUser) or isinstance(event.source, SourceRoom) or isinstance(event.source, SourceGroup):
                profile = line_bot_api.get_profile(event.source.user_id)
                txt = 'Hai ' + profile.display_name
                txt2 = 'Status message mu: ' + profile.status_message
                line_bot_api.reply_message(
                    event.reply_token, [
                        TextSendMessage(
                            text=txt
                        ),
                        TextSendMessage(
                            text=txt2
                        )
                    ]
                )
        # need help?
        else:
            line_bot_api.reply_message(
                event.reply_token, TextSendMessage(text="butuh bantuan? ketik '#help'"))
    # shortcut tag
    elif (text[0] == '/') and (text[len(text)-1] == '/'):
        judul_tag = search(r'\/(.*)',text).group(1)[:-1]
        if isinstance(event.source, SourceGroup):
            if event.source.group_id == altia_id:
                pake_ini = img_url_tag_gab
            else:
                pake_ini = img_url_tag
        if judul_tag in pake_ini:
            image_message = ImageSendMessage(
                    original_content_url=pake_ini[judul_tag][0],
                    preview_image_url=pake_ini[judul_tag][1])
            line_bot_api.reply_message(event.reply_token, image_message)
        else:
            line_bot_api.reply_message(
                    event.reply_token, TextSendMessage(text="Untuk melihat list tag ketik '#taglist'"))
            

# handle join event
@handler.add(JoinEvent)
def handle_join(event):
    if event.source.type == 'group':
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text='Watashinonamaeha akatsukidesu ;-;')
            )


@handler.add(LeaveEvent)
def handle_leave():
    app.logger.info("Got leave event")


@handler.add(PostbackEvent)
def handle_postback(event):
    if event.postback.data == 'ping':
        line_bot_api.reply_message(
            event.reply_token, TextSendMessage(text='pong'))


@handler.add(BeaconEvent)
def handle_beacon(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(
            text='Got beacon event. hwid={}, device_message(hex string)={}'.format(
                event.beacon.hwid, event.beacon.dm)))



if __name__ == "__main__":
    
    # create tmp dir for download content
    #make_static_tmp_dir()
    
    port = int(os.environ.get("PORT", 33507))
    app.run(host='0.0.0.0', port=port)
