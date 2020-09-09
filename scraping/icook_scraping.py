from urllib.request import urlopen
import json, time, random, jieba
import requests
import os
import numpy as np
import pandas as pd
from bs4 import BeautifulSoup
import ssl
ssl._create_default_https_context = ssl._create_unverified_context
pd.set_option('display.max_columns', 20)

# header_dict = {}
# header_str = ''':authority| icook.tw
# :method| GET
# :path| /search/%E5%81%A5%E8%BA%AB/
# :scheme| https
# accept| text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9
# accept-encoding| gzip, deflate, br
# accept-language| zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7
# cookie| __cfduid=df05791dae8f3f53bd7f928f7bfa579411597837937; segments=; CF-IPCountry=TW; prevent_auto_login=true; visitor=13403636102263958864; _gcl_au=1.1.1555051540.1597837940; __auc=dc686331174069017578f07dcc2; _fbp=fb.1.1597837940637.818477277; _gaexp=GAX1.2.WokL82CyQsCeFiDqyUpAgQ.18584.1; __gads=ID=ef7fc8373a410904:T=1597837941:S=ALNI_MbT7t4tAmIj7NpHtAqnVdXrfFWy2w; truvid_protected={"val":"c","level":1,"geo":"TW","timestamp":1597837958}; GED_PLAYLIST_ACTIVITY=W3sidSI6InNtVUEiLCJ0c2wiOjE1OTc4Mzc5NzcsIm52IjoxLCJ1cHQiOjE1OTc4Mzc5NjcsImx0IjoxNTk3ODM3OTc2fSx7InUiOiIyZWFnIiwidHNsIjoxNTk3ODM3OTY3LCJudiI6MSwidXB0IjoxNTk3ODM3OTU0LCJsdCI6MTU5NzgzNzk2NH1d; __asc=6963e6351740c202bc625a7f7e0; AMP_TOKEN=%24NOT_FOUND; _gid=GA1.2.1261953932.1597931269; sent-cid=1597931269; latested-vip-feature=undefined/undefined/undefined; _ga=GA1.1.1867804998.1597837941; _ga_ZKZX6M179R=GS1.1.1597931268.2.1.1597931305.23; _ga_Q65WJCEHK3=GS1.1.1597931268.2.1.1597931316.12; CSRF-TOKEN=vhpHwkaVllY8UD%2BI8D7PTv3YPU93iicmlBuqvFM%2B4a0up1bJ2tCF8b79nC1p69esugqy4GK1AJN1iMH8HqK%2BRw%3D%3D; _icook_sess=M1J6Wi9pYjBBNU5rTGNmQzdlVENscWh6Tm13Z2lQRTl5OFk5WEJkcWwyWEE1a3R5UnViSzJVOHUyTTNsMTcvNElBZGNtdWpXWFoxdU96Tm1WTkRuTG0vMjZTLzlZOS9lejRVYnZaQlF0amlZbGNDWklkc2tjeEM5amRLUWZNenlQR0JrR05oVXhuQUlZZHVsNStWcW9yZEVFZjc2b1NIeFUxNndYZkdpdUNIa0J3K1d2WWpreHl3ZndPUHdyQmlla080ckJEbmxUeGJmS1hybUJxTmZyWXpJSGM1Rm9PcU1iYUJhTjNFaDJyU2JkTWN3Vkt3VnlYNVRibG9KdGttMGxQcmtzMlQ2SDMySUdLZ0tmTmhaMHFlVEk5LzdwZzJuUllMN1RwYW9YOVcwY3dLeWdrcmVGR3lzZi9nRkV4bFBqdDh2SmU2ZmNnZFFNMmtpM0FsQVkrazlxL1dQWTN2clNmZEJDU0xTQnNZPS0tV3hyOGVUWi9HajQ5d25TZ1h2NzMydz09--d57faf14f3457173c25e80bf60ff516091aaea4f
# referer| https://icook.tw/search/%E5%81%A5%E8%BA%AB/
# sec-fetch-dest| document
# sec-fetch-mode| navigate
# sec-fetch-site| same-origin
# sec-fetch-user| ?1
# upgrade-insecure-requests| 1
# user-agent| Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36'''
# for each_line in [lines for lines in header_str.split('\n')]:
#     header_dict[each_line.split('|')[0]] = each_line.split('|')[1]



user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36"
headers = {'User-agent' : user_agent}

def getRecipeList(keyword):
    '''
    Extracting list of total searched recipes with URLs
    :param keyword: A string, specified the searching keyword
    :return: A dictionary, with url as key and recipe title as the value
    '''
    icook_url = 'https://icook.tw/search/{}/'.format(keyword)
    ss = requests.session()
    response = ss.get(icook_url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    try:
        os.mkdir('./icook_{}/'.format(keyword))
    except:
        print("The directory is already exist")
        pass

    #checking total result pages
    result_number = soup.select('span.search-result-refine-count')[0]
    available_pages = int(result_number.text.replace(',','')) // 18
    print('Total search pages {}'.format(available_pages))

    recipe_dict = {}
    for i in range(2):
        time.sleep(random.randint(2,4))
        iter_searching_url = 'https://icook.tw/search/{}/?page={}'.format(keyword, i+1)
        response_2 = ss.get(iter_searching_url, headers=headers)
        soup_2 = BeautifulSoup(response_2.text, 'html.parser')

    # Extracting recipe titles and URLs
        title_list = []
        url_list = []

        all_titles = soup_2.select('div.browse-recipe-preview')
        all_urls = soup_2.select('a.browse-recipe-link')
        for content in all_titles:
            titles = content.select('span')
            title_list.append(titles[0].text.strip())

        for links in all_urls:
            url_list.append('https://icook.tw' + links['href'])

        # Constructing the returning dict
        for n, link in enumerate(url_list):
            recipe_dict[link] = title_list[n]

    return recipe_dict



def getRecipeContent(keyword, recipe_dict):

    for url in list(recipe_dict.keys())[:2]:  ###################################
        ss = requests.session()
        response = ss.get(url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')

        ingredient_group = soup.select("div.ingredients-groups")
        for each_group in ingredient_group:
            each_ingredient = each_group.select('div.')











result_dict = getRecipeList('健身')
print(result_dict)
print('Totle recipes: ', len(result_dict.keys()))

getRecipeContent('健身', result_dict)


