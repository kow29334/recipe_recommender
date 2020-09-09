from urllib.request import urlopen
import json, time, random, jieba
import requests
import os
import numpy as np
import pandas as pd
import pymongo
from bs4 import BeautifulSoup
import ssl
ssl._create_default_https_context = ssl._create_unverified_context
pd.set_option('display.max_columns', 20)

user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36"
headers = {'User-agent' : user_agent}
cookpad_url = 'https://cookpad.com/tw/搜尋/{}'

client = pymongo.MongoClient(host='localhost', port=27017)


def getRecipeList(keyword, page):
    '''
    Extracting a list of recipe titles and URLs.
    :param keyword: A string, the searching keyword
    :param page: An integer, number of pages to be extracted
    :return: A list, listing recipe titles and URLs
    '''

    try:
        os.mkdir('./cookpad_{}'.format(keyword))
    except:
        pass

    recipe_list = []
    main_url = cookpad_url.format(keyword)
    ss = requests.session()
    response = ss.get(main_url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find total amount of result
    first = soup.select('div#main_contents')
    for second in first:
        third = second.select('span.results-header__count.text-tertiary')
        for content in third:
            result_count = content.text
            print('There are {} recipes found'.format(result_count))
    total_page_num = int(result_count) // 20
    print(total_page_num, 'pages')
    # Determine the number of searching pages
    if page > total_page_num:
        search_page = total_page_num
        print('Warning!! There are only {} pages of result.'.format(search_page))
    else:
        search_page = page

    # Extracting all recipe URLs
    for i in range(search_page):
        time.sleep(random.randrange(8,17))
        iter_url = main_url + '?page={}'.format(i+1)
        response_2 = ss.get(iter_url, headers=headers)
        soup2 = BeautifulSoup(response_2.text, 'html.parser')
        layer_1 = soup2.select('div.flex-grow.overflow-hidden')
        # E#xtracting recipe Name & URL
        for n, layer_2 in enumerate(layer_1):
            recipe_name_tags = layer_2.select('span')
            recipe_urls = layer_2.select('a.flex.items-center')
            for recipe_name in recipe_name_tags:
                recipe_title = recipe_name.text
            for url in recipe_urls:
                recipe_url = 'https://cookpad.com' + url['href']

            recipe_list.append(recipe_title + '|' + recipe_url)
            #print(n + 1)
    print('Recipe_list completed, there are {} items'.format(len(recipe_list)))

    # Create a cach file recording recipe ID
    try:
        with open('./cookpad_search_cach.txt'.format(keyword), 'a+', encoding='utf-8') as file:
            file.close()
    except:
        pass

    return recipe_list

def getRecipeContent(keyword, recipe_list):
    '''
    Scraping ingredients from each recipe
    :param recipe_list: Input a list, containing all recipe titles and urls
    :param keyword: A string,
    :return: No returning object, saving recipe into txt file.
    '''
    total_recipe_list = []
    print('Starting scraping ingredient...')
    # Scraping ingredients & steps
    for each_item in recipe_list:

        web_url = each_item.split('|')[1] # recipe url
        recipe_id = ((web_url.split('/')[5]).split('-')[0])

        #First, refering to cach
        with open('./cookpad_search_cach.txt'.format(keyword), 'r') as check_cach:
            cach_content = check_cach.read()
        # checking if the recipe has already been in files
        if recipe_id in cach_content:
            print('Recipe {} has been saved before !!..'.format(recipe_id))
            pass

        else:
            time.sleep(random.randrange(9, 15))
            title = each_item.split('|')[0] # recipe title
            ss = requests.session()
            response = ss.get(web_url, headers=headers)
            soup = BeautifulSoup(response.text, 'html.parser')

            # Scraping recipe ingredient
            layer_1 = soup.select('div.ingredient-list')
            ingredient_str = ''
            recipe_dict = {}
            for layer_2 in layer_1:
                layer_3 = layer_2.select('li')
                for layer_4 in layer_3:
                    ingredient = layer_4.text
                    ingredient_str = ingredient_str + ingredient.strip() + ','

            # Scraping cooking steps
            steps_layer1 = soup.select('ol.numbered-list')
            steps_str = ''
            for steps_layer2 in steps_layer1:
                steps = steps_layer2.select('p.mb-2.inline')
                for step in steps:
                    #print(step.text)
                    steps_str = steps_str + step.text.strip() + '|'

            # Find timestamp
            profile = soup.select('div#author_profile')
            for timestamp in profile:
                find_time = timestamp.select('time')
                post_time = find_time[0].text

            # Find author
            author_info = soup.select('div.recipe-media')
            for info in author_info:
                author = info.select('span.text-primary.text-cookpad-20.font-extrabold.leading-snug')
                for username in author:
                    author_name = username.text
            # Find comment
            comments = soup.select('div.recipe-show__story.prose.break-words')
            for insdie_comment in comments:
                wording = insdie_comment.select('p.mb-2')
                for comment in wording:
                    comment_content = comment.text
            try:
                recipe_dict["url"] = web_url
                recipe_dict["title"] = title
                recipe_dict["time"] = post_time
                recipe_dict["author"] = author_name
                recipe_dict["ingredient"] = ingredient_str
                recipe_dict["steps"] = steps_str
                recipe_dict["comment"] = comment_content
                recipe_dict["category"] = keyword
            except:
                pass


            #Save all dictionaries of recipes into one list
            #total_recipe_list.append(recipe_dict)

            # Insert into Mongodb
            try:
                db = client.tibame
                collection = db.recipe_raw
                insert_item = recipe_dict
                insert_result = db.recipe_raw.insert_one(insert_item)
                print(insert_result)

                # save file
                saveFile(recipe_dict, keyword, recipe_id)
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
        with open('./cookpad_{}/{}.txt'.format(directory, item_no), 'w', encoding='utf-8') as file:
            file.write(str(content_dict))
        # writing recipe_id into cach
        with open('./cookpad_search_cach.txt'.format(directory), 'a+', encoding='utf-8') as cach:
            cach.write(item_no+'\n')
        print('Recipe {} saved !'.format(item_no))
    except Exception as error_name:
        print(error_name)
        pass




if __name__ == '__main__':

    searching_list = ['健身','增肌','低卡','低碳','減脂','生酮','健康']

    #searching_list = ['西式','日式','歐式','中式','快速','三明治']
    for item in searching_list:
        result_list = getRecipeList(item,50)
        getRecipeContent(item, result_list)



