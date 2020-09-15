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






def joFitness(endPage, startPage = 1, count = 1):
    '''
    爬取 https://jo-fitness.com 網站
    endPage:爬取頁數
    startPage:開始頁數
    count:流水號起始
    '''

    headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36'}

    fileName = 'joFitness'  # 路徑名稱

    count = int(count)  # 流水號

    #range(startPage,endPage加1)
    for p in range(int(startPage), int(endPage)+1):

        print('爬網第%d頁，共%d頁' % (p, endPage))

        url ='https://jo-fitness.com/page/%d/' % p

        ss = requests.session()

        res =ss.get(url = url, headers = headers)

        soup = BeautifulSoup(res.text,'html.parser')

        fitness = soup.select('div[class="ast-row"]')[0]

        article = fitness.select('article')

        #爬取每頁的文章
        for i in article:

            i_title =i.select('h2')[0].text

            print(i_title)

            i_url = i.select('a')[0]['href']

            print(i_url)

            i_res = requests.get(url =i_url, headers=headers)

            i_soup = BeautifulSoup(i_res.text, 'html.parser')

             #部分文章沒有最後更新時間
            try:

                i_time = i_soup.select('time[class="post-last-modified-td"]')[0].text

            except IndexError:

                i_time = 0

            #print(i_time)

            # 部分文章沒有作者
            try:

                i_author = i_soup.select('span[class="posted-by vcard author"]')[0].text

                # print(i_author)

            except IndexError:

                i_author  = 0

            i_content_list =i_soup.select('div[id="primary"]')[0].text

            #print(article_content_list)

            # 部分文章沒有Table of Contents
            try:

                i_content_str = str(i_content_list).split('Table of Contents')

                i_content_str1 = str(i_content_str[1]).split('推薦閱讀')

            except IndexError:

                i_content_str = str(i_content_list).split('推薦閱讀')


            i_content = i_content_str1[0]

            article_json = {'url':i_url, 'title':i_title, 'lesson' : 0, 'strength' : 0, 'lesson_time' : 0, 'describe' : i_content, 'time' : i_time, 'author' : i_author}

            #轉成jason檔
            article_json = json.dumps(article_json, ensure_ascii = False)

            #執行存檔
            saveFile(fileName, i_title, article_json, count)

            #存完每篇文章隨機休息5~10秒
            y = random.randint(5, 10)

            time.sleep(y)

            print('休息', y, '秒') # 印出休息秒數

            count += 1






if __name__ == '__main__':
    joFitness(4)














