from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
from selenium.webdriver.common.keys import Keys
import pandas as pd
import re
import requests
from bs4 import BeautifulSoup
import time

headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36'}

options = webdriver.ChromeOptions()
options.add_argument('lang=ko_KR')
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.88 Safari/537.36")
options.add_argument("window-size=1000,2800");
driver= webdriver.Chrome('./chromedriver', options = options)
driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", { "source": """ Object.defineProperty(navigator, 'webdriver', { get: () => undefined }) """ }) # 크롤링 방지 무력화
driver.implicitly_wait(10)
url = 'https://www.coupang.com/np/categories/195050'
df = pd.read_csv('crawling_data/cleaned_product_name.csv')
# print(df.head())
product_names = list(df.product_name)
# print(drink_names)
# drink_names = ['토민 샤인클링']

for product_name in product_names[::-1]:
    driver = webdriver.Chrome('./chromedriver', options=options)
    driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
        "source": """ Object.defineProperty(navigator, 'webdriver', { get: () => undefined }) """})  # 크롤링 방지 무력화
    driver.implicitly_wait(10)
    driver.get(url)
    driver.find_element_by_xpath('//*[@id="headerSearchKeyword"]').send_keys(product_name) #drink_name 리스트 읽기
    time.sleep(2)
    driver.find_element_by_xpath('//*[@id="headerSearchKeyword"]').submit() # 클릭하기
    time.sleep(2)
    try:
        elements = driver.find_elements_by_class_name('no-1') # 광고가 아닌 가장 첫번 째 제품 찾기
        elements[0].click()
    # count = 0
    # for click in elements:
    #     click.click()
    #     time.sleep(1)
    #     count +=1
    #     if count > 0: # 한 번만 클릭하고
    #         break

        window_after = driver.window_handles[1]
        driver.switch_to.window(window_after) # 새로운 창 hand하기
    except:
        print('새창 error')

    time.sleep(1)
    content_list = []
    try:
        driver.find_element_by_xpath('//*[@id="btfTab"]/ul[1]/li[2]').click() # 상품평 클릭
    except:
        print('상품평 리뷰 클릭 error')
    review_count = 0
    for i in range(2):
        if review_count == 1:  # best 리뷰에 글이 없는 경우가 1번 생기면
            break  # page를 도는 for 문도 끝내라
        # pages = driver.find_elements_by_class_name('sdp-review__article__page__num')
        for j in range(2,12):

            if review_count == 1 : # best 리뷰에 글이 없는 경우가 1번 생기면
                break # page를 도는 for 문도 끝내라
            try:
                time.sleep(2)
                # print(page.text)
                driver.find_element_by_xpath(f'//*[@id="btfTab"]/ul[2]/li[2]/div/div[6]/section[4]/div[3]/button[{j}]').click()
                # page.click() # 페이지 번호 list 누르기
                time.sleep(2)
            except:
                print('page_error')
                break
            contents = driver.find_elements_by_class_name('sdp-review__article__list__review__content')
            if contents:
                 # 베스트 리뷰의 첫번 째
                for content in contents:
                    content = content.text
                    content = re.compile('[^가-힣 ]').sub(' ', content)
                    print(i,content)
                    content_list.append(content)
            else:
                print('text 찾기 에러') # best 리뷰에 더 이상 글이 없다
                review_count += 1
        try:
            driver.find_element_by_class_name(f'sdp-review__article__page__next').click()
        except:
            print('button[12]_error')
            continue

    print(content_list)
    print(len(content_list))
    df = pd.DataFrame({'reviews':content_list})
    df.to_csv('./review_data/reviews_{}.csv'.format(product_name), index=False)
    driver.quit()




