#! user/bin/env python
# -*- coding: utf-8 -*-

from urllib.request import build_opener, HTTPCookieProcessor
from urllib.parse import urlencode, parse_qs
from http.cookiejar import CookieJar
from lxml.html import fromstring
from settings import mail_tel, password
# settings.pyというファイルを作ってそこにmail_tel,passwordを記述すること.
# 例えばmail_tel='hogehoge@gmail.com',password='hogehoge1111'と記述する.

"""
opener:Cookieを利用するためのもの.
"""
opener = build_opener(HTTPCookieProcessor(CookieJar()))

def Parser(data):
    """
    htmlを解析するメソッド.
    data:Cookieを使ったニコニコユーザのIDとPwを納めたもの.
    response:openerと引数のdataを使い実際にログインする時に返ってくるレスポンス.
    """
    response = opener.open('https://secure.nicovideo.jp/secure/login',data)

    response.close()

def data():
    """
    ログイン情報を納めるためのメソッド.
    return: ポストデータ.
    """

    post = {
        'mail_tel':mail_tel,
        'password':password
    }

    return urlencode(post).encode('utf-8')

def getVideo():
    """
    実際にニコニコ動画のデータをダウンロードするメソッド.
    url:動画のIDを入力させた後,ニコニコのapiを用いて動画のurlを取得する.
    getVideoAndTitle:タイトルと動画の情報を得る.
    flv_url:このデータは配列で,urlの中の先頭に動画データがあるためそれを指定.
    title:htmlのheadにあるtitleから取得.
    """
    encoding = 'utf_8'
    
    video_id = input("ダウンロードしたい動画のIDを入力してください(ex:sm999): ")
    
    with opener.open('http://www.nicovideo.jp/api/getflv?v=' + video_id) as url:
        flv_url = parse_qs(url.read().decode(encoding),encoding = encoding)['url'][0]
    url.close()    

    with opener.open('http://www.nicovideo.jp/watch/'+ video_id) as getVideoAndTitle:
        """
        doc:fromstringを利用して,htmlを取得している.
        ちなみにfromstrningはlxml.htmlの中にあってlxmlはc言語で高速なのでこれを使った方がいいらしい.
        """
        doc = fromstring(getVideoAndTitle.read().decode(encoding))
        title = doc.head.find('title').text.split(' - ')[0]
        # ファイル名に使えない記号をreplaceを使って削除している.
        for c in '\/?:*"><|':
            title = title.replace(c, '')
    getVideoAndTitle.close()

    print('Now, ',title,' is downloading.')
    with open(title + '.mp4','wb') as f:
        with opener.open(flv_url) as response:
            f.write(response.read())
        response.close()
    f.close()
    print('Done!')

def main():
    """
    mainメソッド.
    """
    Parser(data())
    getVideo()

if __name__ == '__main__':
    main()    