#!/usr/bin/env python
# encoding=utf-8

from selenium import webdriver
import pytesseract
from PIL import Image
import requests
import sys 
import time

if sys.getdefaultencoding() != 'utf-8':
    reload(sys)
    sys.setdefaultencoding('utf-8')

ofile = open('result.txt', "a+")

def get_captcha(browser):
    session=requests.session()
    browser.save_screenshot(r"test.png")  
    imgelement = browser.find_elements_by_xpath('.//span[@class="number"]/img')[0]
    location = imgelement.location  
    size = imgelement.size  
    coderange = (int(location['x']),int(location['y']),int(location['x']+size['width']),
                          int(location['y']+size['height'])) 
    i=Image.open(r"test.png") 
    img_region = i.crop(coderange)  
    img_region.save(r"captcha.png")

    # img = session.get("https://isisn.nsfc.gov.cn/egrantindex/validatecode.jpg").content
    # with open('captcha.jpg','wb') as imgfile:
    #     imgfile.write(img)
    # image = image.open('captcha.jpg')
    # box = (45, 10, 160, 50)
    # region = image.crop(box)
    # region.save('captcha.jpg')

    image = Image.open('captcha.png')
    text = pytesseract.image_to_string(image)
    # print "captcha:"+text 

    return text

def submit_form(browser, subjectCode_Id, keyWord, grantCode, year, title):

    js = '$("#f_ctitle").val("' + title +'");'
    # js += '$("#f_subjectCode").val("' + subjectCode +'");'
    # js += '$("#f_subjectCode_hideName").val("' + subjectName +'");'
    js += '$("#f_subjectCode_hideId").val("' + subjectCode_Id +'");'
    js += '$("#sqdm").val("' + subjectCode_Id + '");'
    js += '$("#f_grantCode").val("' + grantCode +'");'
    js += '$("#f_keyWords").val("' + keyWord +'");'
    js += '$("#f_year").val("' + year +'");'

    result_element = None 
    while(result_element == None):
        checkcode = get_captcha(browser)
        if (checkcode == ""):
            browser.refresh()
            checkcode = get_captcha(browser)
        js1 = '$("#f_checkcode").val("' + checkcode +'");'
        browser.execute_script(js)
        browser.execute_script(js1)
        browser.find_element_by_id("searchBt").click()    
        try:
            result_element = browser.find_element_by_id('sp_2_TopBarMnt')
        except:
            result_element = None

    result_number = result_element.text
    if result_number == '0':
        return
    ofile.write("query: subject:" + subjectCode_Id + ' keyword:' + keyWord +' grant:' + grantCode + ' year:' + year + ' title:' +title+" 共"+result_number+"条结果：\n")
    result_table = browser.find_element_by_id("dataGrid")
    table_trs = result_table.find_elements_by_tag_name("tr")
    for tr in table_trs:
        table_tds = tr.find_elements_by_tag_name("td")
        row = ""
        for td in table_tds:
            row += td.text + ' '
        ofile.write("result: " + row +"\n")
    ofile.flush()

# subjectCodeIds = ["F0208", "F020801", "F020802", "F020803", "F020804","F020805","F020806","F020807","F020808","F020809"]
# allKeyWords = ["内容分发网络","互联网视频","互联网体系结构","SDN","访问模型","内容分发","传输控制","体系结构","NFV"]
# allKeyWords = ["云计算", "云存储", "网络测量" ,"流量异常检测"]

allKeyWords = []
subjectCodeIds = []
years = [] # ['2017', '2016','2015','2014','2013','2012','2011','2010'] # ,'2009','2008','2007','2006','2005']
# grantCodes = ['218','220','222','339','429','432','433','649','579','630','631','632','635','51','52','2699','70','7161']
grantCodes = ['218','220','222','429','2699','632']
# grantCodes = ['429', '2699']

def restart_firefox(browser):
    print "restarting firefox..."
    browser.close()
    browser = webdriver.Firefox()
    browser.get('https://isisn.nsfc.gov.cn/egrantindex/funcindex/prjsearch-list')

def auto_search():
    print('opening a browser...\n')
    browser = webdriver.Firefox()
    browser.get('https://isisn.nsfc.gov.cn/egrantindex/funcindex/prjsearch-list')
    index = 0
    for s in open("subject.config"):
        subjectCodeIds.append(s[:-1])
    for s in open("year.config"):
        years.append(s[:-1])
    for s in open("keyword.config"):
        allKeyWords.append(s[:-1])
    print allKeyWords, years, subjectCodeIds
    for subid in subjectCodeIds:
        for grantcode in grantCodes:
            for year in years:
                if len(allKeyWords) > 0:
                    title=''
                    for keyword in allKeyWords:
                        try:
                            submit_form(browser, subid, keyword, grantcode, year, title)
                        except:
                            time.sleep(3)
                        index += 1
                        print index
                        if index % 100 == 0:
                            print "restarting firefox..."
                            browser.close()
                            browser = webdriver.Firefox()
                            browser.get('https://isisn.nsfc.gov.cn/egrantindex/funcindex/prjsearch-list')
                        browser.back()
                        time.sleep(1)

                    # keyword = ''
                    # for title in allKeyWords:
                    #     try:
                    #         submit_form(browser, subid, keyword, grantcode, year, title)
                    #     except:
                    #         print "restarting firefox..."
                    #         browser.close()
                    #         browser = webdriver.Firefox()
                    #         browser.get('https://isisn.nsfc.gov.cn/egrantindex/funcindex/prjsearch-list')
                    #         submit_form(browser, subid, keyword, grantcode, year, title)
                    #     index += 1
                    #     print index	
                    #     if index % 100 == 0:
                    #         print "restarting firefox..."
                    #         browser.close()
                    #         browser = webdriver.Firefox()
                    #         browser.get('https://isisn.nsfc.gov.cn/egrantindex/funcindex/prjsearch-list')
                    #     browser.back()
                    #     time.sleep(1)
                else :
                    keyword = ''
                    title = ''
                    try:
                        submit_form(browser, subid, keyword, grantcode, year, title)
                    except:
                        time.sleep(3)
                    index += 1
                    print index
                    if index % 100  == 0:
                        print "restarting firefox..."
                        browser.close()
                        browser = webdriver.Firefox()
                        browser.get('https://isisn.nsfc.gov.cn/egrantindex/funcindex/prjsearch-list')
                        print "restart done"
                    browser.back()
                    time.sleep(1)

   
if __name__ == '__main__':
    print("starting...")
    auto_search()

