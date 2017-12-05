import requests
from bs4 import BeautifulSoup


def requestHtml(url, data,tryCount):
    # 如果请求出错则再次请求，10次尝试
    while (tryCount > 0):
        tryCount = tryCount - 1
        res = requests.post(url, data)
        if res.status_code == 200:
            return res.text
    return ''


def getCompanyData(html):
    #<table><tr><td></td></tr></table>
    soup = BeautifulSoup(html, 'html.parser')
    table = soup.find(id="data_list_container")
    if table is None:
        print('报错，重新请求')
        return
    tableData = table.find_all('tr')[1:]  # 去除表头
    companyList = []
    for item in tableData:
        td = item.find_all('td')
        oredernum = td[0].text.strip()
        serialnum = td[1].text.strip()
        name = td[2].text.strip()
        address = td[3].text.strip()
        industry = td[4].text.strip()
        type = td[5].text.strip()
        companydata = {'oredernum': oredernum, 'serialnum': serialnum, 'name': name, 'address': address,
                       'industry': industry, 'type': type}
        companyList.append(companydata)
    return companyList


def getInputValue(html, id):
    soup = BeautifulSoup(html, 'html.parser')
    # 获取元素
    hidenInput = soup.find(id=id)
    return hidenInput['value']


def saveData(data,filePath):
    output = open(filePath, 'a', encoding='utf-8')
    for item in data:
        output.write(str(item))
        output.write('\n')
    output.close()



# 配置
url = 'http://www.szsti.gov.cn/services/hightech/default.aspx'
first = 1
# total = 591
total = 10
page = 1
data = {}
errorPage = []
filePath = 'running/company.txt'
logPath = 'running/logs.txt'
tryCount = 10

if __name__ == '__main__':

    while (page <= total):
        html = requestHtml(url, data,tryCount)
        if html == '':
            print('出错page = '+str(page))
            errorPage.append(page)
        else:
            companyList = getCompanyData(html)
            saveData(companyList,filePath)
            data['__VIEWSTATE'] = getInputValue(html, '__VIEWSTATE')
            data['__EVENTVALIDATION'] = getInputValue(html, '__EVENTVALIDATION')

        page = page + 1
        data['PagerControl_input'] = str(page)
        data['__EVENTTARGET'] = 'go'
        data['__EVENTTARGET'] = 'PagerControl'
        data['__EVENTARGUMENT'] = ''

    saveData(errorPage, logPath)#记录请求失败的页面

