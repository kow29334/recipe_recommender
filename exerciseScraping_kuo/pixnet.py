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

        #如果title有特殊字元改以網頁名稱+流水號方式儲存
        with open('%s/%s%s.txt' % (path, fileName, count), 'w', encoding='utf-8') as w:

            w.write(str(article_json))






def pixnet(count = 1):
    '''
    爬取 .pixnet.net/blog 網站
    爬取一個以上的網頁，所以參數去掉起始頁與總頁數
    count:流水號起始
    '''

    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36'}

    count = int(count)  # 流水號

    fileName = 'pixnet'  # 路徑名稱

    #兩篇以上的部落格文章網址
    url = ['https://z8474newo.pixnet.net/blog',
           'https://a0976737702.pixnet.net/blog/post/317703954-%E3%80%90%E5%81%A5%E8%BA%AB%E5%B0%88%E9%A1%8C%E3%80%91%E9%81%A9%E5%90%88%E7%B5%A6%E5%88%9D%E5%AD%B8%E8%80%85%E7%9A%84%E9%87%8D%E8%A8%93%E5%85%A5%E9%96%80%E8%8F%9C%E5%96%AE',
            'https://nrghot.pixnet.net/blog/post/77152017-%E6%AF%8F%E5%A4%A915%E5%88%86%E9%90%98-%E6%9B%B2%E7%B7%9A%E8%AE%8A%E5%A5%BD%E7%9A%844%E7%A8%AE%E5%8B%95%E4%BD%9C%2B7%E5%88%86%E9%90%98%E7%9A%84%E9%AB%98%E5%BC%B7%E5%BA%A6']



    for u in url:

        ss = requests.session()

        res = ss.get(url = u, headers=headers)

        #網頁需要特別設定編碼
        res.encoding = 'utf-8'

        # print(res)

        soup = BeautifulSoup(res.text,'html.parser')


        article = soup.select('div[class="article"]')

        #爬取每頁的文章
        for i in article:

            i_title = i.select('li[class="title"]')[0].text

            print(i_title)

            i_time = i.select('li[class="publish"]')[0].text

            # print(i_date)

            url = i.select('li[class="title"]')[0]

            i_url = url.select('a')[0]['href']

            print(i_url)

            ss = requests.session()

            res = ss.get(url = i_url, headers=headers)

            # 網頁需要特別設定編碼
            res.encoding = 'utf-8'

            soup = BeautifulSoup(res.text, 'html.parser')

            i_content = soup.select('div[class="article-content-inner"]')[0].text

            # print(i_content)

            i_author = soup.select('p[class="author-profile__info"]')[0].text

            # print(i_author)

            article_json = {'url':i_url, 'title':i_title, 'lesson' : 0, 'strength' : 0, 'lesson_time' : 0, 'describe' : i_content, 'time' : i_time, 'author' : i_author}

            #轉成jason檔
            article_json = json.dumps(article_json, ensure_ascii = False)

            #執行存檔
            saveFile(fileName, i_title, article_json, count)

            #存完每篇文章隨機休息5~10秒
            y = random.randint(5, 10)

            time.sleep(y)

            print('休息', y, '秒')

            count += 1






if __name__ == '__main__':
    pixnet(1)
