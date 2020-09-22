import requests, time ,random, os, json
from bs4 import BeautifulSoup





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

        # 如果title有特殊字元改以網頁名稱+流水號方式儲存
        with open('%s/%s%s.txt' % (path, fileName, count), 'w', encoding='utf-8') as w:

            w.write(str(article_json))






def sportsplanetmag(count = 1):
    '''
    爬取 https://www.sportsplanetmag.com 網站
    爬取一個以上的網頁，所以參數去掉起始頁與總頁數
    count:流水號起始
    '''

    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36'}

    count = int(count)  # 流水號

    fileName = 'sportsplanetmag'  # 路徑名稱

    # 兩篇以上的文章網址
    url_list = ['https://www.sportsplanetmag.com/tag/%E5%81%A5%E8%BA%AB/page/{:d}/',
                'https://www.sportsplanetmag.com/tag/%E8%A8%93%E7%B7%B4%E5%8B%95%E4%BD%9C/page/{:d}',
                'https://www.sportsplanetmag.com/tag/%E6%B8%9B%E8%84%82/page/{:d}/',
                'https://www.sportsplanetmag.com/tag/%E8%B7%91%E6%AD%A5/page/{:d}/',
                'https://www.sportsplanetmag.com/tag/%E5%BE%92%E6%89%8B%E8%A8%93%E7%B7%B4/page/{:d}',
                'https://www.sportsplanetmag.com/tag/%E7%91%9C%E4%BC%BD/page/{:d}',
                'https://www.sportsplanetmag.com/tag/%E6%A0%B8%E5%BF%83%E8%A8%93%E7%B7%B4/page/{:d}/',
                'https://www.sportsplanetmag.com/tag/%E7%98%A6%E8%BA%AB/page/{:d}/',
                'https://www.sportsplanetmag.com/tag/%E5%A2%9E%E8%82%8C/page/{:d}/',
                'https://www.sportsplanetmag.com/tag/%E5%95%9E%E9%88%B4/page/{:d}',
                'https://www.sportsplanetmag.com/tag/%E7%91%9C%E4%BC%BD%E5%8B%95%E4%BD%9C/page/{:d}']

    page_list = [89,48,25,111,12,29,16,32,17,4,21]

    them =['健身','訓練動作','減酯','跑步','徒手訓練','瑜珈','核心訓練','瘦身','增肌','啞鈴','瑜珈動作']

    #迴圈不同主題的網站
    for a in range(len(url_list)):
        print('================',them[a],'===============')

        # 迴圈網站裡不同頁數
        for p in range(1,page_list[a]):

            print(p)

            url = url_list[a].format(p)

            ss = requests.session()

            res = ss.get(url = url, headers = headers)

            # print(res)

            soup = BeautifulSoup(res.text,'html.parser')

            article = soup.select('div[class="col col-sm-1"]')

            # print(article)

            #迴圈每篇文章
            for i in article:

                i_url = i.select('a')[0]['href']

                i_title = i.select('a')[0].text

                i_title_split = str(i_title).split('\n')

                i_title = i_title_split[9]

                #部分文章去除特殊自元
                try:

                    i_title = str(i_title).rstrip('\r')

                except:

                    pass

                print(i_title)

                print(i_url)

                i_res = ss.get(url=i_url, headers=headers)

                i_soup = BeautifulSoup(i_res.text, 'html.parser')

                i_time = i_soup.select('div[class ="time"]')[0].text

                # print(i_time)

                article_content = i_soup.select('div[class="article-main"]')[0]

                article_content1 = article_content.select('div[class="article-info"]')[0].text

                i_content = article_content1

                i_content = str(i_content).strip('\n')

                #部分文章沒有作者
                try:

                    i_author = i_soup.select('span[style="color: #808080;"]')[0].text

                except:

                    i_author = 0

                # print(i_author)

                article_json = {'url': i_url, 'title': i_title, 'lesson': 0, 'strength': 0, 'lesson_time': 0,
                                'describe': i_content, 'time': i_time, 'author': i_author}

                # 執行存檔
                saveFile(fileName, i_title, article_json, count)

                # 存完每篇文章隨機休息5~10秒
                y = random.randint(5, 10)

                time.sleep(y)

                print('休息', y, '秒')

                count += 1






if __name__ == '__main__':
    sportsplanetmag(1)


