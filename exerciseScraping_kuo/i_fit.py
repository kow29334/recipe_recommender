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






def ifit(endPage, startPage = 1, count = 1):
    '''
    爬取 https://www.i-fit.com.tw 網站
    endPage:爬取頁數
    startPage:開始頁數
    count:流水號起始
    '''

    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36',
                'referer': 'https://www.i-fit.com.tw/'
                }#網站要求要referer

    count = int(count)  # 流水號

    fileName = 'ifit' # 路徑名稱

    #range(startPage,endPage加1)
    for p in range(int(startPage), int(endPage)+1):

        print('爬網第%d頁，共%d頁' % (p, endPage))

        url = 'https://www.i-fit.com.tw/post/sport?page={:d}'.format(p)

        ss = requests.session()

        res = ss.get(url = url, headers=headers)

        soup = BeautifulSoup(res.text, 'html.parser')

        article = soup.select('div[class="post-list-item type-sport"]')


        #爬取每頁的文章
        for i in article:
            title = i.select('h3')[0].text

            print(title)

            i_url = i.select('a')[0]['href']

            print(i_url)

            i_headers = {
                            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36',
                            'referer': 'https://www.i-fit.com.tw/tag/%20%E9%81%8B%E5%8B%95?page={:d}'.format(p)
                        }#網站要求要referer

            ss = requests.session()

            res = ss.get(url=i_url, headers=i_headers)

            soup = BeautifulSoup(res.text, 'html.parser')

            i_title = soup.select('div[class="post-title"]')[0].text

            i_title =str(i_title).lstrip('\n\n')

            i_title = i_title.rstrip('\n')

            i_title = str(i_title)

            # print(i_title)

            i_time = soup.select('span[class="date"]')[0].text

            # print(i_date)

            i_content = soup.select('div[class="article"]')[0].text

            i_content = str(i_content).split('點擊加入 LINE 好友！得知更多瘦身新訊')[0]

            i_content = i_content.lstrip('\n\n\n\n\n\n\n\n\n\n')

            # print(i_content)

            i_author = 0 #本篇沒有作者

            article_json = {'url':i_url, 'title':i_title, 'lesson' : 0, 'strength' : 0, 'lesson_time' : 0, 'describe' : i_content, 'time' : i_time, 'author' : i_author}

            #轉成jason檔
            article_json = json.dumps(article_json, ensure_ascii = False)



            #執行存檔
            saveFile(fileName, i_title, article_json, count)

            #存完每篇文章隨機休息5~10秒
            y = random.randint(5, 10)

            time.sleep(y)

            print('休息', y, '秒')  # 印出休息秒數

            count += 1


if __name__ == '__main__':
    ifit(14)