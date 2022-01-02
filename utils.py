import os

from linebot import LineBotApi, WebhookParser
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
    SourceUser, SourceGroup, SourceRoom,
    TemplateSendMessage, ConfirmTemplate, MessageAction,
    ButtonsTemplate, ImageCarouselTemplate, ImageCarouselColumn, URIAction,
    PostbackAction, DatetimePickerAction,
    CameraAction, CameraRollAction, LocationAction,
    CarouselTemplate, CarouselColumn, PostbackEvent,
    StickerMessage, StickerSendMessage, LocationMessage, LocationSendMessage,
    ImageMessage, VideoMessage, AudioMessage, FileMessage,
    UnfollowEvent, FollowEvent, JoinEvent, LeaveEvent, BeaconEvent,
    FlexSendMessage, BubbleContainer, ImageComponent, BoxComponent,
    TextComponent, SpacerComponent, IconComponent, ButtonComponent,
    SeparatorComponent, QuickReply, QuickReplyButton
)

from bs4 import BeautifulSoup
import urllib.request as req

channel_access_token = os.getenv("LINE_CHANNEL_ACCESS_TOKEN", None)


def send_text_message(event, text):
    line_bot_api = LineBotApi(channel_access_token)
    line_bot_api.push_message(event.source.user_id, TextSendMessage(text=text))

    return "OK"
"""
def SwitchMenuTo(MenuName, event):
    line_bot_api = LineBotApi(channel_access_token)
    rich_menu_list = line_bot_api.get_rich_menu_list()
    for rich_menu in rich_menu_list:
        if rich_menu.name == MenuName:
            line_bot_api.link_rich_menu_to_user(event.source.user_id, rich_menu.rich_menu_id)
            return True

    return False
"""
def send_template_message(event, template):
    line_bot_api = LineBotApi(channel_access_token)
    line_bot_api.push_message(event.source.user_id, template)
# 本週新片
def show_movie_thisweek(event):
    movies_link = [] # 電影連結
    movies_title = [] # 電影中文標題
    movies_title_en = [] # 電影英文標題
    movies_expectation = [] # 網友期待度
    movies_releasedate = [] # 電影上映日期
    movies_intro = [] # 電影介紹
    movies_img = [] # 電影照片
    movies_trailer = [] # 電影預告片連結
    movies_photos = [] # 電影劇照連結
    movies_timetable = [] # 電影時刻表連結

    carousel_group = []
    url = 'https://movies.yahoo.com.tw/movie_thisweek.html'
    request = req.Request(
        url,
        headers={
            "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36"
        }
    )
    with req.urlopen(request) as response:
        data = response.read().decode("utf-8")
    
    root = BeautifulSoup(data, "html.parser")
    
    for index, data in enumerate(root.select('ul.release_list li')): # ul 為 class 屬性 releasr_list 為 class 名稱 所需資料在li內
        
        if index == 10:
            break
        movies_info = data.find('div', 'release_info_text')
        movies_info_2 = data.find('div', 'release_btn')
        movies_link.append(movies_info.find('a')['href'])
        movies_title.append(movies_info.find('a').text.lstrip())
        movies_title_en.append(movies_info.find('div', 'en').a.text.lstrip())
        movies_expectation.append(movies_info.find('dl', 'levelbox').dt.span.text)
        movies_releasedate.append(movies_info.find('div', 'release_movie_time').text)
        movies_intro.append(movies_info.find('div', 'release_text').span.text.lstrip())
        movies_img.append(data.find('img')['src'])
        trailer_link = movies_info_2.find_all('a')[1].get('href')
        photos_link = movies_info_2.find_all('a')[2].get('href')
        timetable_link = movies_info_2.find_all('a')[3].get('href')
        if trailer_link != None:
            movies_trailer.append(trailer_link)
        else:
            movies_trailer.append('https://movies.yahoo.com.tw/movie_thisweek.html')
        if photos_link != None:
            movies_photos.append(photos_link)
        else:
            movies_photos.append('https://movies.yahoo.com.tw/movie_thisweek.html')
        if timetable_link != None:
            movies_timetable.append(timetable_link)
        else:
            movies_timetable.append('https://movies.yahoo.com.tw/movie_thisweek.html')

    # 製作回覆訊息
    x = ['info', 'title', 'title_en', 'expectation', 'releasedate', 'intro', 'img', 'trailer', 'photos', 'timetable']
    movies = []
    movies.append(movies_link)
    movies.append(movies_title)
    movies.append(movies_title_en)
    movies.append(movies_expectation)
    movies.append(movies_releasedate)
    movies.append(movies_intro)
    movies.append(movies_img)
    movies.append(movies_trailer)
    movies.append(movies_photos)
    movies.append(movies_timetable)
    movies_dic = dict(zip(x, movies))

    for i in range(len(movies_title)):
        detail = movies_dic['releasedate'][i] + '\n' + '期待度 : ' + movies_dic['expectation'][i] + '\n' + '電影簡介 : ' + movies_dic['intro'][i]
        carousel_data = CarouselColumn(
            thumbnail_image_url = movies_dic['img'][i],
            title = movies_dic['title'][i][0:20] + movies_dic['title_en'][i][0:20],
            text = detail[0:60],
            actions = [
                URIAction(label = '電影介紹', uri = movies_dic['info'][i]),
                URIAction(label = '預告片', uri = movies_dic['trailer'][i]),
                #URIAction(label = '劇照', uri = movies_dic['photos'][i]),
                URIAction(label = '時刻表', uri = movies_dic['timetable'][i])
            ]
        )
        carousel_group.append(carousel_data)

    carousel_template = CarouselTemplate(columns = carousel_group, image_aspect_ratio = 'square', image_size = 'cover')
    template_message = TemplateSendMessage(alt_text = 'Carousel alt text', template = carousel_template)
    send_template_message(event, template_message)
    return True

def show_movie_intheaters(event):
    movies_link = [] # 電影連結
    movies_title = [] # 電影中文標題
    movies_title_en = [] # 電影英文標題
    movies_expectation = [] # 網友期待度
    movies_releasedate = [] # 電影上映日期
    movies_intro = [] # 電影介紹
    movies_img = [] # 電影照片
    movies_trailer = [] # 電影預告片連結
    movies_photos = [] # 電影劇照連結
    movies_timetable = [] # 電影時刻表連結

    carousel_group = []
    url = 'https://movies.yahoo.com.tw/movie_intheaters.html'
    request = req.Request(
        url,
        headers={
            "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36"
        }
    )
    with req.urlopen(request) as response:
        data = response.read().decode("utf-8")
    
    root = BeautifulSoup(data, "html.parser")
    
    for index, data in enumerate(root.select('ul.release_list li')): # ul 為 class 屬性 releasr_list 為 class 名稱 所需資料在li內
        
        if index == 10:
            break
        movies_info = data.find('div', 'release_info_text')
        movies_info_2 = data.find('div', 'release_btn')
        movies_link.append(movies_info.find('a')['href'])
        movies_title.append(movies_info.find('a').text.lstrip())
        movies_title_en.append(movies_info.find('div', 'en').a.text.lstrip())
        movies_expectation.append(movies_info.find('dl', 'levelbox').dt.span.text)
        movies_releasedate.append(movies_info.find('div', 'release_movie_time').text)
        movies_intro.append(movies_info.find('div', 'release_text').span.text.lstrip())
        movies_img.append(data.find('img')['src'])
        trailer_link = movies_info_2.find_all('a')[1].get('href')
        photos_link = movies_info_2.find_all('a')[2].get('href')
        timetable_link = movies_info_2.find_all('a')[3].get('href')
        if trailer_link != None:
            movies_trailer.append(trailer_link)
        else:
            movies_trailer.append('https://movies.yahoo.com.tw/movie_intheaters.html')
        if photos_link != None:
            movies_photos.append(photos_link)
        else:
            movies_photos.append('https://movies.yahoo.com.tw/movie_intheaters.html')
        if timetable_link != None:
            movies_timetable.append(timetable_link)
        else:
            movies_timetable.append('https://movies.yahoo.com.tw/movie_intheaters.html')

    # 製作回覆訊息
    x = ['info', 'title', 'title_en', 'expectation', 'releasedate', 'intro', 'img', 'trailer', 'photos', 'timetable']
    movies = []
    movies.append(movies_link)
    movies.append(movies_title)
    movies.append(movies_title_en)
    movies.append(movies_expectation)
    movies.append(movies_releasedate)
    movies.append(movies_intro)
    movies.append(movies_img)
    movies.append(movies_trailer)
    movies.append(movies_photos)
    movies.append(movies_timetable)
    movies_dic = dict(zip(x, movies))

    for i in range(len(movies_title)):
        detail = movies_dic['releasedate'][i] + '\n' + '期待度 : ' + movies_dic['expectation'][i] + '\n' + '電影簡介 : ' + movies_dic['intro'][i]
        carousel_data = CarouselColumn(
            thumbnail_image_url = movies_dic['img'][i],
            title = movies_dic['title'][i][0:20] + movies_dic['title_en'][i][0:20],
            text = detail[0:60],
            actions = [
                URIAction(label = '電影介紹', uri = movies_dic['info'][i]),
                URIAction(label = '預告片', uri = movies_dic['trailer'][i]),
                #URIAction(label = '劇照', uri = movies_dic['photos'][i]),
                URIAction(label = '時刻表', uri = movies_dic['timetable'][i])
            ]
        )
        carousel_group.append(carousel_data)

    carousel_template = CarouselTemplate(columns = carousel_group, image_aspect_ratio = 'square', image_size = 'cover')
    template_message = TemplateSendMessage(alt_text = 'Carousel alt text', template = carousel_template)
    send_template_message(event, template_message)
    return True

def show_movie_leaderboard(event):
    url = 'https://movies.yahoo.com.tw/movie_comingsoon.html'
    request = req.Request(
        url,
        headers={
            "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36"
        }
    )
    with req.urlopen(request) as response:
        data = response.read().decode("utf-8")
    
    root = BeautifulSoup(data, "html.parser")
    image = root.select_one('div.ranking_top_info_img_r img')['src']
    button_template = ButtonsTemplate(
        image_aspect_ratio = 'square',
        image_size = 'cover',
        thumbnail_image_url = image,
        title = '排行榜',
        text = '請選擇想要看的排行榜',
        actions = [
            URIAction(label = '台北票房榜', uri = 'https://movies.yahoo.com.tw/chart.html'),
            URIAction(label = '全美票房榜', uri = 'https://movies.yahoo.com.tw/chart.html?cate=us'),
            URIAction(label = '年度票房榜', uri = 'https://movies.yahoo.com.tw/chart.html?cate=year'),
            URIAction(label = '預告片榜', uri = 'https://movies.yahoo.com.tw/chart.html?cate=trailer')
        ]
    )
    template_message = TemplateSendMessage(alt_text = 'Buttons alt text', template = button_template)
    send_template_message(event, template_message)
    return True


def show_movie_comingsoon(event):
    movies_link = [] # 電影連結
    movies_title = [] # 電影中文標題
    movies_title_en = [] # 電影英文標題
    movies_expectation = [] # 網友期待度
    movies_releasedate = [] # 電影上映日期
    movies_intro = [] # 電影介紹
    movies_img = [] # 電影照片
    movies_trailer = [] # 電影預告片連結
    movies_photos = [] # 電影劇照連結
    movies_timetable = [] # 電影時刻表連結

    carousel_group = []
    url = 'https://movies.yahoo.com.tw/movie_comingsoon.html'
    request = req.Request(
        url,
        headers={
            "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36"
        }
    )
    with req.urlopen(request) as response:
        data = response.read().decode("utf-8")
    
    root = BeautifulSoup(data, "html.parser")
    
    for index, data in enumerate(root.select('ul.release_list li')): # ul 為 class 屬性 releasr_list 為 class 名稱 所需資料在li內
        
        if index == 10:
            break
        movies_info = data.find('div', 'release_info_text')
        movies_info_2 = data.find('div', 'release_btn')
        movies_link.append(movies_info.find('a')['href'])
        movies_title.append(movies_info.find('a').text.lstrip())
        movies_title_en.append(movies_info.find('div', 'en').a.text.lstrip())
        movies_expectation.append(movies_info.find('dl', 'levelbox').dt.span.text)
        movies_releasedate.append(movies_info.find('div', 'release_movie_time').text)
        movies_intro.append(movies_info.find('div', 'release_text').span.text.lstrip())
        movies_img.append(data.find('img')['src'])
        trailer_link = movies_info_2.find_all('a')[1].get('href')
        photos_link = movies_info_2.find_all('a')[2].get('href')
        timetable_link = movies_info_2.find_all('a')[3].get('href')
        if trailer_link != None:
            movies_trailer.append(trailer_link)
        else:
            movies_trailer.append('https://movies.yahoo.com.tw/movie_comingsoon.html')
        if photos_link != None:
            movies_photos.append(photos_link)
        else:
            movies_photos.append('https://movies.yahoo.com.tw/movie_comingsoon.html')
        if timetable_link != None:
            movies_timetable.append(timetable_link)
        else:
            movies_timetable.append('https://movies.yahoo.com.tw/movie_comingsoon.html')

    # 製作回覆訊息
    x = ['info', 'title', 'title_en', 'expectation', 'releasedate', 'intro', 'img', 'trailer', 'photos', 'timetable']
    movies = []
    movies.append(movies_link)
    movies.append(movies_title)
    movies.append(movies_title_en)
    movies.append(movies_expectation)
    movies.append(movies_releasedate)
    movies.append(movies_intro)
    movies.append(movies_img)
    movies.append(movies_trailer)
    movies.append(movies_photos)
    movies.append(movies_timetable)
    movies_dic = dict(zip(x, movies))

    for i in range(len(movies_title)):
        detail = movies_dic['releasedate'][i] + '\n' + '期待度 : ' + movies_dic['expectation'][i] + '\n' + '電影簡介 : ' + movies_dic['intro'][i]
        carousel_data = CarouselColumn(
            thumbnail_image_url = movies_dic['img'][i],
            title = movies_dic['title'][i][0:20] + movies_dic['title_en'][i][0:20],
            text = detail[0:60],
            actions = [
                URIAction(label = '電影介紹', uri = movies_dic['info'][i]),
                URIAction(label = '預告片', uri = movies_dic['trailer'][i]),
                URIAction(label = '劇照', uri = movies_dic['photos'][i]),
                #URIAction(label = '時刻表', uri = movies_dic['timetable'][i])
            ]
        )
        carousel_group.append(carousel_data)

    carousel_template = CarouselTemplate(columns = carousel_group, image_aspect_ratio = 'square', image_size = 'cover')
    template_message = TemplateSendMessage(alt_text = 'Carousel alt text', template = carousel_template)
    send_template_message(event, template_message)
    return True


