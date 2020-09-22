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






def worldGym(count = 1):
    '''
    爬取 https://blog.worldgymtaiwan.com/ 網站
    爬取一個以上的網頁，所以參數去掉起始頁與總頁數
    count:流水號起始
    '''

    count = int(count)  # 流水號

    fileName = 'worldGym' # 路徑名稱

    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36',
                'referer':'https://blog.worldgymtaiwan.com/'
                }#網站要求要referer

    url_list =[ 'https://blog.worldgymtaiwan.com/tag/%E9%81%8B%E5%8B%95',
                'https://blog.worldgymtaiwan.com/tag/%E7%98%A6%E8%BA%AB%E9%81%8B%E5%8B%95']

    them =['運動','瘦身運動']

    for a in range(len(url_list)):

        print('================', them[a], '===============')

        url = url_list[a]

        ss = requests.session()

        res = ss.get(url = url, headers=headers)

        soup = BeautifulSoup(res.text, 'html.parser')

        article = soup.select('div[class="post-item fullwidth"]')

        #爬取每頁的文章
        for i in article:

            i_title = i.select('h2')[0].text

            print(i_title)

            i_url = i.select('a')[0]['href']

            print(i_url)

            ss = requests.session()

            res = ss.get(url=i_url, headers=headers)

            soup = BeautifulSoup(res.text, 'html.parser')

            i_time = soup.select('div[class="post-date fullwidth"]')[0].text

            i_time = str(i_time).split('更新日期')

            i_time = i_time[0].lstrip(':')

            #print(i_time)

            i_author = soup.select('a[class="author-link"]')[0].text

            #print(i_author)

            i_content = soup.select('div[class="section post-body fullwidth"]')[0].text

            i_content = str(i_content).split('喜歡這篇文章嗎？或是想要知道那些更多資訊呢？')

            i_content = i_content[0]

            #print(i_content)

            article_json = {'url': i_url, 'title': i_title, 'lesson': 0, 'strength': 0, 'lesson_time': 0,
                            'describe': i_content, 'time': i_time, 'author': i_author}

            # 轉成jason檔
            #article_json = json.dumps(article_json, ensure_ascii = False)

            # 執行存檔
            saveFile(fileName, i_title, article_json, count)

            # 存完每篇文章隨機休息5~10秒
            y = random.randint(5, 10)

            time.sleep(y)

            print('休息', y, '秒')  # 印出休息秒數

            count += 1






if __name__ == '__main__':
    worldGym(1)
