import requests, time ,random, os, json
from bs4 import BeautifulSoup
import pandas as pd






def saveFile(fileName, fileTitle, article_json, count):
    '''
    爬完網頁後以JASON格式存成text檔
    fileName:路徑名稱
    fileTiile:Jason的title當檔名
    article_json:要存的JASON
    count:如果檔名不符合格式以路徑名稱+流水號 流水號起始
    '''
    path = './%s' % fileName

    if not os.path.exists(path):
        os.mkdir(path)

    try:

        with open('%s/%s.txt' % (path, fileTitle), 'w', encoding='utf-8') as w:

            w.write(str(article_json))

    except:

        #如果title有特殊字元改以網頁名稱+流水號方式儲存
        with open('%s/%s%s.txt' % (path, fileName, count), 'w', encoding='utf-8') as w:

            w.write(str(article_json))






def peeta(endPage, startPage = 1, count = 1):
    '''
    爬取https://www.peeta.tw/all 網站
    endPage:爬取頁數
    startPage:開始頁數
    count:流水號起始
    '''

    headers = {
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36'}

    # range(第一頁,頁數加1)

    count = int(count)  # 流水號

    fileName = 'peeta' #路徑名稱

    # range(startPage,endPage加1)
    for p in range(int(startPage), int(endPage) + 1):

        print('爬網第%d頁，共%d頁' % (p, endPage))

        url = 'https://www.peeta.tw/all/page/%d/' % p

        ss = requests.session()

        res = ss.get(url = url, headers=headers)

        soup = BeautifulSoup(res.text,'html.parser')

        #print(soup.text)

        article = soup.select('article')

        #print(article)

        #爬取每頁的文章
        for i in article:

            title_list = i.select('div[class="elementor-post__text"]')[0]

            i_title = title_list.select('a')[0].text

            i_title = str(i_title).lstrip('\n\t\t\t\t')

            i_title = str(i_title).rstrip('\t\t\t')

            i_url = title_list.select('a')[0]['href']

            print(i_title)

            print(i_url)

            i_res = ss.get(url=i_url, headers=headers)

            i_soup = BeautifulSoup(i_res.text, 'html.parser')

            article_information = i_soup.select('div[class="elementor-element elementor-element-e6a7d0c elementor-column elementor-col-50 elementor-inner-column"]')[0].text

            article_information_split = str(article_information).split('\n')

            i_time = article_information_split[14]

            i_time = str(i_time).lstrip('\t\t\t\t\t\t\t\t\t\t')

            i_time = str(i_time).rstrip('\t\t\t\t\t')

            #print(i_time)

            i_content = i_soup.select('div[class="elementor-element elementor-element-38d4bc69 elementor-widget elementor-widget-theme-post-content"]')[0].text

            #print(i_content)

            i_author = i_soup.select('span[class="elementor-icon-list-text elementor-post-info__item elementor-post-info__item--type-author"]')[0].text

            i_author = str(i_author).split('\n')

            i_author = i_author[2]

            i_author = i_author.strip('\t')

            # print(i_author)

            article_json = {'url':i_url, 'title':i_title, 'lesson' : 0, 'strength' : 0, 'lesson_time' : 0, 'describe' : i_content, 'time' : i_time, 'author' : i_author}

            #轉成jason檔
            article_json = json.dumps(article_json, ensure_ascii = False)

            #執行存檔
            saveFile(fileName, i_title, article_json, count)

            # 存完每篇文章隨機休息5~10秒
            y = random.randint(5, 10)

            time.sleep(y)

            print('休息', y, '秒')

            count += 1






if __name__ == '__main__':
    peeta(5)