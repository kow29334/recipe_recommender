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







def businessweekiy(endPage, startPage = 1, count = 1):
    '''
    爬取 https://health.businessweekly.com.tw/ 網站
    endPage:爬取頁數
    startPage:開始頁數
    count:流水號起始
    '''

    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36'}

    count = int(count)  # 流水號

    fileName = 'businessweekiydef'  # 路徑名稱

    # range(startPage,endPage加1)
    for p in range(int(startPage), int(endPage) + 1):

        print('爬網第%d頁，共%d頁' % (p, endPage))

        url = 'https://health.businessweekly.com.tw/BChannel.aspx?Channel_no=0002&s=1&v=1&p=%d' % p

        ss = requests.session()

        res = ss.get(url = url, headers=headers)

        #print(res)

        soup = BeautifulSoup(res.text,'html.parser')

        #print(soup.text)

        article = soup.select('div[id="viewcontent"]')[0]

        article = article.select('article')

        #爬取每頁的文章
        for i in article:

            #print(i)

            title = i.select('div[class="headline"]')[0]

            i_title = title.select('a')[0].text

            i_title = str(i_title).split('\r\n')

            i_title = i_title[0]

            print(i_title)

            i_url = title.select('a')[0]['href']

            print(i_url)

            headers = {
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36',
                'Referer': 'https://health.businessweekly.com.tw/AArticle.aspx?id=ARTL003003019'} #網站要求要referer

            ss = requests.session()

            i_res = ss.get(url=i_url, headers=headers)

            i_soup = BeautifulSoup(i_res.text, 'html.parser')

            i_author = i_soup.select('em[class="authorname"]')[0].text

            i_author = str(i_author).lstrip('撰文者')

            # print(i_author)

            i_time = i_soup.select('div[class="detail_info right"]')[0].text

            i_time = str(i_time).split('瀏覽數')

            i_time = i_time[0]

            # print(i_time)

            i_content = i_soup.select('section[id="articleBlock"]')[0].text

            # print(i_content)

            article_json = {'url': i_url, 'title': i_title, 'lesson': 0, 'strength': 0, 'lesson_time': 0, 'describe': i_content,
                            'time': i_time, 'author': i_author}

            #轉成jason檔
            article_json = json.dumps(article_json, ensure_ascii=False)

            fileName = 'businessweekiy'

            #執行存檔
            saveFile(fileName, i_title, article_json, count)

            #存完每篇文章隨機休息5~10秒
            y = random.randint(5, 10)

            time.sleep(y)

            print('休息', y, '秒')

            count += 1





if __name__ == '__main__':
    businessweekiy(292)





