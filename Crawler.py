from bs4 import BeautifulSoup
import urllib.request as req
import urllib.parse as parse
import http.cookiejar as cook
import ssl

def __customHTTPSHandler__():
    return req.HTTPSHandler(context=ssl.SSLContext(ssl.PROTOCOL_TLSv1))

def __getPrivateHtml__(base_url, cookie, sRJupNo):
    opener = req.build_opener(__customHTTPSHandler__())
    opener.addheaders.append(('Cookie', cookie))
    f = opener.open(base_url + sRJupNo)
    soup = BeautifulSoup(f, 'html.parser')
    # print(soup)
    return soup

def getCookie(Id,Passwd):
    cookiejar = cook.CookieJar()
    url = 'https://www.wellihillipark.com/sub3/member/login_chk.asp'
    data = parse.urlencode({
        'id': Id,
        'pw': Passwd
    }).encode('utf-8')
    opener  = req.build_opener(req.HTTPCookieProcessor(cookiejar), __customHTTPSHandler__())
    reques = req.Request(url,data)
    f = opener.open(reques)
    html = f.read()
    #print(cookiejar)
    if cookiejar.__len__() == 1: return None # login fail

    textCookie = ''
    for c in cookiejar:
        textCookie = textCookie + c.name + '=' + c.value + '; '
    #with req.urlopen(reques, data=data) as f:
    #   head = f
    #
    #        cookie = cook.CookieJar.extract_cookies(self, head, reques)
    #
    #       print(cookie)
    #     resp = f.read()
    #      #print(head,'|')
    print('[debug]cookie:',textCookie)
    return(textCookie)

def __chkSrJup__(cookie):
    opener = req.build_opener(__customHTTPSHandler__())
    opener.addheaders.append(('Cookie', cookie))
    url = 'https://www.wellihillipark.com/sub3/seasoninfo/infodata/my_main_SeasonTicket.html?sryear=1718'
    try:
        op = opener.open(url)
    except:
        return '0'
    return '1'

def getSimpleInfo(cookie):
    opener = req.build_opener(__customHTTPSHandler__())
    opener.addheaders.append(('Cookie',cookie))
    url = 'https://www.wellihillipark.com/sub3/seasoninfo/infodata/my_main_SeasonTicket.html?sryear=1718'
    try:
        op = opener.open(url)
    except:
        print('exception type2')
        return '0'
    soup = BeautifulSoup(op,'html.parser')
    #print('infopage:',soup,'-----')
    sRJup = soup.select("form[name='main'] > input")
    sRJupNo = sRJup[0].attrs.get('value')
    name = sRJup[1].attrs.get('value')
    photo_link = sRJup[2].attrs.get('value')
    first_boarding = sRJup[5].attrs.get('value')
    last_boarding = sRJup[6].attrs.get('value')

    print('[DEBUG]\nname:',name,'\nsrJupNo:',sRJupNo,'\nphoto link:',photo_link,'\nfirst board:',first_boarding,'\nlast board:',last_boarding)

    return name,sRJupNo,photo_link,first_boarding,last_boarding

def initLoginCheck(id,passwd):
    cookie = getCookie(id,passwd)

    if cookie == None:
        return -1
    elif __chkSrJup__(cookie) == '0':
        return 0
    return 1

def getRank(cookie,sRJupNo):
    #sRJupNo = getSrJupNo(cookie)
    html = __getPrivateHtml__(
        'https://www.wellihillipark.com/sub3/seasoninfo/infodata/Season_Ranke.asp?sryear=1718&sRJupNo=', cookie,
        str(sRJupNo))
    ranks = html.select("tr > td")
    it = iter(ranks)
    rank_list=[]
    for rank in it:
        next(it)
        rank=next(it).text
        rank_begin = rank.find('상위')
        rank_end = rank.find('%')
        rank_list.append(rank[rank_begin+3:rank_end])
    print('[DEBUG]',rank_list)
    return rank_list

def getDetailInfo(cookie,sRJupNo):
    soup = __getPrivateHtml__(
        'https://www.wellihillipark.com/sub3/seasoninfo/infodata/my_main_SeasonTicket_info.html?sryear=1718&sRJupNo=',
        cookie,
        sRJupNo
    )
    li = soup.select("table[width='640']")
                     #> tr > td")
    score_set = []
    for data_li in li:
        score_list=[]
        detail_list = data_li.select("tr")
        for detail in detail_list[:-1]:
            #print('---')
            detail_list_list = detail.select("td")[1:]
            for score in detail_list_list:
                #print(score.text)
                score_list.append(score.text)

        score_set.append(score_list)
        #print('--end--')
    print('[DEBUG] : ',score_set)
    return score_set

if __name__ == '__main__':
    WARNID = "minjea917"
    ID = 'slls2008'
    WARNPASSWD = "rnjsalswo10"
    PASSWD = 'ehdqkddk123'

    case = input() # 0: login check, 1: get data 2: testing exception
    id=''
    passwd=''
    if case == '0':
        initLoginCheck(ID,PASSWD)

    elif case == '1':
        id=ID
        passwd=PASSWD
        cookie = getCookie(id, passwd)
        name, sRJupNo, _, _, _ = getSimpleInfo(cookie)
        getRank(cookie,sRJupNo)

    elif case == '2':
        id=WARNID
        passwd=WARNPASSWD
        cookie = getCookie(id, passwd)
        _, sRJupNo, _, _, _ = getSimpleInfo(cookie)
        getRank(cookie,sRJupNo)











