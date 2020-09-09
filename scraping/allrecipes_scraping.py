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


user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36"
headers = {'User-agent' : user_agent}
allrecipe_rul = 'https://www.allrecipes.com/search/results/?wt={}&sort=re&page={}'

def getRecipeList(keyword, page):

    init_url = allrecipe_rul.format(keyword, 1)
    ss = requests.session()
    response = ss.get(init_url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    url_list = []

    # Determine total result pages number
    result_content = soup.select('div.results-container')
    for content in result_content:
        result_number = content.select('span.subtext')
        result = int(result_number[0].text.split(' ')[0])
    available_pages = result / 20

    # Check if user input valid page number
    if page > available_pages:
        print('There are only {} pages of result'.format(available_pages))
        searching_page = available_pages
    else:
        searching_page = page
    time.sleep(random.randrange(3,7))
    # Extracting recipes URLs
    for n in range(searching_page):
        searching_url = allrecipe_rul.format(keyword, n+1)
        response_2 = ss.get(searching_url, headers=headers)
        soup_2 = BeautifulSoup(response_2.text, 'html.parser')
        all_urls = soup_2.select('div.fixed-recipe-card__info')
        for content in all_urls:
            find_url = content.select('a')
            url = find_url[0]['href']
            url_list.append(url)
    return url_list



def getRecipeIngredient(recipe_list):
    for url in recipe_list[:2]:  ################################################
        ss = requests.session()
        response = ss.get(url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')

        # Extracting ingredients
        ingredient_section = soup.select('ul.ingredients-section')
        for item in ingredient_section:
            ingredient_item = item.select('li.ingredients-item')
            for ingredient in ingredient_item:
                name = ingredient.select('span.ingredients-item-name')
                print(name[0].text.strip())








result_list = getRecipeList('protein', 1)
getRecipeIngredient(result_list)


