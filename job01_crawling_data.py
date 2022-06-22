from bs4 import BeautifulSoup
import requests
import re
import pandas as pd
import time

headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36'}

product_name = []
for i in range(1, 18):
    url = 'https://www.coupang.com/np/categories/195050?page={}'.format(i)
    try:
        res = requests.get(url, headers=headers, timeout=10)
    except:
        print('pageerror')
        continue
    soup = BeautifulSoup(res.text, 'html.parser')
    contents = soup.find_all("li", {"class": "baby-product renew-badge"})

    for content in contents:
        # try:
        data_product_id = content.find('a')['data-product-id']
        data_item_id = content.find('a')['data-item-id']
        data_vendor_item_id = content.find('a')['data-vendor-item-id']
        url1 = 'https://www.coupang.com/vp/products/{}?itemId={}&vendorItemId={}&sourceType=CATEGORY&categoryId=194950&isAddedCart='.format(data_product_id,data_item_id,data_vendor_item_id)
        try:
            res = requests.get(url1, headers=headers, timeout=10)
        except:
            print('error')
            continue
        soup = BeautifulSoup(res.text, 'html.parser')
        product = soup.find("h2", {"class": "prod-buy-header__title"})
        print(product)
        product_name.append(product.get_text())


df = pd.DataFrame({'product_name':product_name})
df.to_csv('./crawling_data/product_name.csv', encoding='utf-8-sig', index=False)
print(product_name)