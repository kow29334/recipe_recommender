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






def trueterral(endPage, startPage = 1, count = 1):
    '''
    爬取 https://trueterral.com/blog/ 網站
    endPage:爬取頁數
    startPage:開始頁數
    count:流水號起始
    '''

    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36'}

    fileName = 'trueterral'  # 路徑名稱

    count = int(count)  # 流水號

    # range(startPage,endPage加1)
    for p in range(int(startPage), int(endPage) + 1):

        print('爬網第%d頁，共%d頁' % (p, endPage))

        url = 'https://trueterral.com/blog/page/%d/' % p

        ss = requests.session()

        res = ss.get(url = url, headers=headers)

        # print(res)

        soup = BeautifulSoup(res.text,'html.parser')

        article = soup.select('article')

        #爬取每頁的文章
        for i in article:

            try:
                i_title = i.select('h2[class="entry-title"]')[0].text

                print(i_title)

                i_url = i.select('a')[0]['href']

                print(i_url)

                ss = requests.session()

                i_res = ss.get(url=i_url, headers=headers)

                # print(res)

                i_soup = BeautifulSoup(i_res.text, 'html.parser')

                i_time = i_soup.select('time[class="entry-date published"]')[0].text

                # print(i_date)

                i_author = i_soup.select('span[class="author vcard"]')[0].text

                # print(i_author)

                i_content = i_soup.select('div[id="tve_editor"]')[0].text

                iContentStr = str(i_content).lstrip('\n\n\n\n')

                # print(i_content)

                article_json = {'url': i_url, 'title': i_title, 'lesson': 0, 'strength': 0, 'lesson_time': 0,
                                'describe': i_content, 'time': i_time, 'author': i_author}

                # 轉成jason檔
                article_json = json.dumps(article_json, ensure_ascii = False)

                # 執行存檔
                saveFile(fileName, i_title, article_json, count)

                # 存完每篇文章隨機休息5~10秒
                y = random.randint(5, 10)

                time.sleep(y)

                print('休息', y, '秒')  # 印出休息秒數

                count += 1

            except:

                pass


if __name__ == '__main__':
    trueterral(10)










