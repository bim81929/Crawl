from selenium import webdriver
PROXY = "14.177.235.17:8080"
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--proxy-server=%s' % PROXY)
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')

import time
from selenium.webdriver.common.keys import Keys
import csv
import pandas as pd
import progressbar

PATH = "chromedriver"

search_url_dict = dict(zip(["SACDEP"], ["https://shopee.vn/S%E1%BA%AFc-%C4%90%E1%BA%B9p-cat.11036279"]))
data = pd.read_csv('Shop.csv', sep='\t')
url = [x for x in data['url']]

def getUrlInShop(baseUrl, num):
    if num == 1:
        return baseUrl
    return baseUrl + '?page=' + str(num) + '&sortBy=pop'

def crawlID(url, driver, start_index):
    with open("ID_product.csv", "w") as f:
        writer = csv.writer(f)
        writer.writerow(["id_shop", "id_product"])
        length = len(url)
        for index in range(0, length):
            print("Index: ", index + start_index)
            _url = url[index]
            driver.get(_url)
            time.sleep(4)
            # cuộn page
            total_height = int(driver.execute_script("return document.body.scrollHeight"))
            for i in range(1, total_height, 100):
                driver.execute_script("window.scrollTo(0, {});".format(i))
            try:  
                link = driver.find_element_by_xpath("//a[@class='navbar-with-more-menu__item']").get_attribute("href")
                _id_shop = link.replace("https://shopee.vn/shop/", "").replace("/search", "")
                page = 1
                while(1):
                    driver.get(getUrlInShop(link, page))
                    time.sleep(4)
                    total_height = int(driver.execute_script("return document.body.scrollHeight"))
                    for i in range(1, total_height, 100):
                        driver.execute_script("window.scrollTo(0, {});".format(i))

                    items = driver.find_elements_by_class_name("shop-search-result-view__item")
                    if len(items) > 0:
                        print("Page: ", page)
                        for i in items:
                            try:
                                link_product = i.find_element_by_css_selector("a").get_attribute("href")
                                writer.writerow([_id_shop, link_product.split('?')[0].split('.')[-1]])
                            except:
                                pass
                    else:
                        break
                    page += 1
            except:
                pass

if __name__ == '__main__':
    from datetime import datetime
    print("Start crawl")
    start = datetime.now()
    
    for i in range(5, 15):
        driver = webdriver.Chrome(PATH,chrome_options=chrome_options)
        driver.maximize_window()

        crawlID(url[i * 100: (i + 1) * 100], driver, i * 100)
        driver.close()
        time.sleep(60)
    print("Stop crawl")
    print('Total time: ', datetime.now() - start)
