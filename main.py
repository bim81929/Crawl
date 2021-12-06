from selenium import webdriver
chrome_options = webdriver.ChromeOptions()
prefs = {'profile.default_content_setting_values': {'cookies': 2, 'images': 2, 'javascript': 2, 
                            'plugins': 2, 'popups': 2, 'geolocation': 2, 
                            'notifications': 2, 'auto_select_certificate': 2, 'fullscreen': 2, 
                            'mouselock': 2, 'mixed_script': 2, 'media_stream': 2, 
                            'media_stream_mic': 2, 'media_stream_camera': 2, 'protocol_handlers': 2, 
                            'ppapi_broker': 2, 'automatic_downloads': 2, 'midi_sysex': 2, 
                            'push_messaging': 2, 'ssl_cert_decisions': 2, 'metro_switch_to_desktop': 2, 
                            'protected_media_identifier': 2, 'app_banner': 2, 'site_engagement': 2, 
                            'durable_storage': 2}}
chrome_options.add_experimental_option('prefs', prefs)
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_argument("start-maximized")
chrome_options.add_argument("disable-infobars")
chrome_options.add_argument("--disable-extensions")

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
                    time.sleep(1)
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
    list_proxy = ['http://ipkuremb:bocdu4tfm4j3@209.127.191.180:9279',
                    'http://ipkuremb:bocdu4tfm4j3@45.95.96.132:8691',
                    'http://ipkuremb:bocdu4tfm4j3@45.95.96.187:8746',
                    'http://ipkuremb:bocdu4tfm4j3@45.95.96.237:8796',
                    'http://ipkuremb:bocdu4tfm4j3@193.8.127.189:9271',
                    'http://ipkuremb:bocdu4tfm4j3@45.94.47.66:8110',
                    'http://ipkuremb:bocdu4tfm4j3@45.94.47.108:8152',
                    'http://ipkuremb:bocdu4tfm4j3@193.8.56.119:9183',
                    'http://ipkuremb:bocdu4tfm4j3@45.95.99.226:7786',
                    'http://ipkuremb:bocdu4tfm4j3@45.95.99.20:7580']
    for i in range(10, 20):
        PROXY = random.choice(list_proxy)
        list_proxy.remove(PROXY)
        chrome_options.add_argument('--proxy-server=%s' % PROXY)
        driver = webdriver.Chrome(PATH,chrome_options=chrome_options)

        crawlID(url[i * 100: (i + 1) * 100], driver, i * 100)
        driver.close()
        time.sleep(10)
    print("Stop crawl")
    print('Total time: ', datetime.now() - start)
