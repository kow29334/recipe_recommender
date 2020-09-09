from urllib.request import urlopen
import json, time, random, jieba
import requests
import os
import numpy as np
import pymongo
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

client = pymongo.MongoClient(host='localhost', port=27017)

def getRecipeList(keyword, page):
    '''
    Extracting list of total searched recipes with URLs
    :param keyword: A string, specified the searching keyword
    :return: A dictionary, with url as key and recipe title as the value
    '''
    icook_url = 'https://icook.tw/search/{}/'.format(keyword)
    ss = requests.session()
    response = ss.get(icook_url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Creating working folder
    try:
        os.mkdir('./icook_{}/'.format(keyword))
    except:
        print("The directory is already exist")
        pass

    #checking total result pages
    result_number = soup.select('span.search-result-refine-count')[0]
    available_pages = int(result_number.text.replace(',','')) // 18
    print('Total search pages {}'.format(available_pages))

    # Determine the number of searching pages
    if page > available_pages:
        search_page = available_pages
        print('Warning!! There are only {} pages of result.'.format(search_page))
    else:
        search_page = page

    recipe_dict = {}
    #for i in range(search_page):
    for i in range(search_page):
        try:
            time.sleep(random.randint(4,10))
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
        except:
            pass
    # Creating cach file
    try:
        with open('./icook_search_cach.txt'.format(keyword), 'a+', encoding='utf-8') as file:
            file.close()
    except:
        pass

    return recipe_dict



def getRecipeContent(keyword, recipe_dict):

    for url in list(recipe_dict.keys()):

        content_dict = {}
        title = recipe_dict[url]
        recipe_id = url.split('/')[-1]

        # First, refering to cach
        with open('./icook_search_cach.txt'.format(keyword), 'r') as check_cach:
            cach_content = check_cach.read()
        # checking if the recipe has already been in files
        if recipe_id in cach_content:
            print('Recipe {} has been saved before !!..'.format(recipe_id))
            pass

        else:
            try:
                ss = requests.session()
                response = ss.get(url, headers=headers)
                soup = BeautifulSoup(response.text, 'html.parser')

                # Extracting ingredients
                ingredient_group = soup.select("div.ingredients-groups")
                ingredient_str = ''
                for each_group in ingredient_group:
                    each_ingredient = each_group.select('div.ingredient')
                    for ingredient in each_ingredient:
                        ingredient_str = ingredient_str + ingredient.text.strip('\r\n') + ','

                # Extracting steps
                steps_group = soup.select('div.recipe-details-howto')
                steps_str = ''
                for each_group in steps_group:
                    steps = each_group.select('li.recipe-details-step-item')
                    for step in steps:
                        steps_str = steps_str + step.text.strip('\n') + '|'


                # Extracting comment
                comments = soup.select('div.header-row.description')
                comment_str = ''
                for comment in comments:
                    comment_str = comment_str + comment.text


                # Extracting time
                times_group = soup.select('div.recipe-details-howto')
                for times in times_group:
                    find_time = times.select('div.recipe-detail-metas')
                    for post_time in find_time:
                        meta_items = post_time.select('time.recipe-detail-meta-item')
                        for item in meta_items:
                            timestamp = item['datetime']

                # Find author
                username = soup.select('div.author-name')
                for user in username:
                    user_name = user.text
            except:
                pass
            
            try:
                content_dict["url"] = url
                content_dict["title"] = title
                content_dict["time"] = timestamp
                content_dict["author"] = user_name.strip()
                content_dict["ingredient"] = ingredient_str
                content_dict["steps"] = steps_str
                content_dict["comment"] = comment_str
                content_dict["category"] = keyword

            except:
                pass

            # Insert into Mongodb
            try:
                db = client.tibame
                collection = db.recipe_raw
                insert_item = content_dict
                insert_result = db.recipe_raw.insert_one(insert_item)
                print(insert_result)

                saveFile(content_dict, keyword, recipe_id)
            except:
                pass

def saveFile(content_dict, directory, item_no):
    '''
    Output recipe as txt file, with json format
    :param content_dict: A dictionary, containing each recipe
    :param directory: A string, specifying working directory for file saving
    :param item_no: A string, specifying file name in accordance with recipe web_id
    :return: No returning object, saving into text file instead
    '''

    # with open('./cookpad_{}/search_cach.txt'.format(directory), 'r') as content:
    #     caching = content.read()
    # # checking if the recipe has already been saved
    # if item_no in caching:
    #     pass
    # else:
    try:
        # Save recipe into file
        with open('./icook_{}/{}.txt'.format(directory, item_no), 'w', encoding='utf-8') as file:
            file.write(str(content_dict))
        # writing recipe_id into cach
        with open('./icook_search_cach.txt'.format(directory), 'a+', encoding='utf-8') as cach:
            cach.write(item_no+'\n')
        print('Recipe {} saved !'.format(item_no))
    except Exception as error_name:
        print(error_name)
        pass







if __name__ == '__main__':
    #searching_list = ['健身','增肌','低卡','低碳','減脂','生酮','健康']
    #searching_list = ['西式', '日式', '歐式', '中式', '快速']
    #searching_list = ['沙拉','素食','牛肉']
    searching_list = ['三明治']
    for item in searching_list:

        result_dict = getRecipeList(item,555)
        print('Totle recipes: ', len(result_dict.keys()))
        getRecipeContent(item, result_dict)


