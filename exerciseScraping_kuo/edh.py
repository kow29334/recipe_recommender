import requests, time ,random, os, json
from bs4 import BeautifulSoup





def saveFile(fileName, fileTitle, article_json, count):
    '''
    爬完網頁後以JASON格式存成text檔
    fileName:路徑名稱
    fileTiile:Jason的title當檔名
    article_json:要存的JASON
    count:如果檔名不符合格式以路徑名稱+流水號 流水號起始
    return:新的流水序號
    '''
    path = './%s' % fileName

    if not os.path.exists(path):

        os.mkdir(path)

    try:

        with open('%s/%s.txt' % (path, fileTitle), 'w', encoding='utf-8') as w:

            w.write(str(article_json))

    except:

        # 如果title有特殊字元改以網頁名稱+流水號方式儲存
        with open('%s/%s%s.txt' % (path, fileName, count), 'w', encoding='utf-8') as w:

            w.write(str(article_json))





#
def edh(count = 1):
    '''
    爬取 https://www.edh.tw/category/ 網站
    爬取一個以上的網頁，所以參數去掉起始頁與總頁數
    count:流水號起始
    '''

    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36'}

    count = int(count)  # 流水號

    fileName = 'edh'  # 路徑名稱

    # 兩篇以上的文章網址
    url_list = ['https://www.edh.tw/category/5/index/%d','https://www.edh.tw/category/212/index/%d',
                'https://www.edh.tw/tagging/article/2992/?p=%d',
                'https://www.edh.tw/category/211/index/%d']

    page_list = [112,8,13,30]

    them = ['運動','瘦身體操','享瘦下半身','輕盈上半身']

    #迴圈不同主題的網站
    for a in range(len(url_list)):

        print('================',them[a],'===============')

        # 迴圈網站裡不同頁數
        for p in range(1,page_list[a]):

            print(p)

            url = url_list[a] % p

            ss = requests.session()

            res = ss.get(url = url, headers = headers)

            #print(res)

            soup = BeautifulSoup(res.text,'html.parser')

            #print(soup.text)

            article = soup.select('div[class="grid calc-3"]')

            #print(each_article)

            #迴圈每篇文章
            for i in article:

                #print(i)

                title_list = i.select('div[class="grid-article"]')[0]

                #print(title_list)

                i_title = title_list.select('h3')[0].text

                print(i_title)

                i_url = 'https://www.edh.tw/' + title_list.select('a')[0]['href']

                print(i_url)

                i_res = ss.get(url=i_url, headers=headers)

                i_soup = BeautifulSoup(i_res.text, 'html.parser')

                i_time = i_soup.select('span[class="date"]')[0].text

                #print(i_time)

                i_content = i_soup.select('div[id="article_page"]')[0].text

                #print(i_content)

                i_author = i_soup.select('span[itemprop="author"]')[0].text

                # print(i_author)

                #部分文章有第二頁
                try :

                    button_url = i_soup.select('a[rel="next"]')[0]['href']

                    print(button_url)

                    i_res = ss.get(url=button_url, headers=headers)

                    i_soup = BeautifulSoup(i_res.text, 'html.parser')

                    i_content2 = i_soup.select('div[id="article_page"]')[0].text

                    i_content_list = [i_content, i_content2]

                    #print(i_content_list)

                except:

                    pass


                #如果有第二頁的Json
                try:

                    article_json = {'url': i_url, 'title': i_title, 'lesson': 0, 'strength': 0, 'lesson_time': 0,
                                'describe' : i_content_list, 'time' : i_time, 'author': i_author}

                except:

                    article_json = {'url': i_url, 'title': i_title, 'lesson': 0, 'strength': 0, 'lesson_time': 0,
                                'describe': i_content, 'time': i_time, 'author': i_author}

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
    edh(1)


