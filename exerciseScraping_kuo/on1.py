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

        #如果title有特殊字元改以網頁名稱+流水號方式儲存
        with open('%s/%s%s.txt' % (path, fileName, count), 'w', encoding='utf-8') as w:

            w.write(str(article_json))






def on1(endPage, startPage = 1, count = 1):
    '''
    爬取 https://1on1.today/blog/category/zh-blog/zh-articles/zh-fitness-knowledge 網站
    endPage:爬取頁數
    startPage:開始頁數
    count:流水號起始
    '''

    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36'}

    count = int(count)  # 流水號

    fileName = 'on1'  # 路徑名稱

    #range(startPage,endPage加1)
    for p in range(int(startPage), int(endPage)+1):

        print('爬網第%d頁，共%d頁'%(p,endPage))

        url ='https://1on1.today/blog/category/zh-blog/zh-articles/zh-fitness-knowledge/page/%d' % p

        #print(p)

        ss = requests.session()

        res =ss.get(url = url, headers = headers)

        soup = BeautifulSoup(res.text,'html.parser')

        article = soup.select('article')

        # 爬取每頁的文章
        for i in article:

            # print(i)

            i_title =i.select('h2')[0].text

            print(i_title)

            i_url = i.select('a')[0]['href']

            print(i_url)

            i_res = requests.get(url =i_url, headers=headers)

            i_soup = BeautifulSoup(i_res.text, 'html.parser')

            i_time = i_soup.select('time[class="post-modified"]')[0].text

            # print(i_time)

            i_author = i_soup.select('span[class="screen-reader-text"]')[0].text

            #print(i_author)

            i_content = i_soup.select('div[class="entry content-box"]')[0].text

            iContentStr = str(i_content).split('延伸閱讀')

            i_content = iContentStr[0]

            #print(i_content)

            article_json = {'url':i_url, 'title':i_title, 'lesson' : 0, 'strength' : 0, 'lesson_time' : 0, 'describe' : i_content, 'time' : i_time, 'author' : i_author}

            # 轉成jason檔
            article_json = json.dumps(article_json, ensure_ascii = False)

            #執行存檔
            saveFile(fileName, i_title, article_json, count)
            # 存完每篇文章隨機休息5~10秒
            y = random.randint(5, 10)

            time.sleep(y)

            print('休息', y, '秒')

            count += 1






if __name__ == '__main__':
    on1(3)