import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import json
from selenium.webdriver.common.action_chains import ActionChains
import os
from selenium.webdriver.chrome.options import Options


def get_tieba_url(driver):
    driver.get('http://tieba.baidu.com/i/i/forum')
    for tag in driver.find_elements_by_link_text('尾页'):
        last_pn = tag.get_attribute('href')[-1]

    time.sleep(2)
    with open('cache.txt', 'w', encoding='UTF-8') as f:
        for pn in range(1, int(last_pn) + 1):
            driver.get('http://tieba.baidu.com/i/i/forum?&pn=' + str(pn))
            for tag in driver.find_elements_by_css_selector('a'):
                url = tag.get_attribute('href')
                if '/f?kw=' in url and 'userbar' not in url:
                    f.write(url)
                    f.write('\n')
            time.sleep(1)
    driver.quit()


def sign_in(driver, url):
    driver.get(url)
    sign_in_button = driver.find_element_by_xpath(
        '//*[@id="signstar_wrapper"]/a')
    # ActionChains(driver).move_to_element(sign_in_button).perform()
    # time.sleep(2)
    sign_in_button.click()
    sign_in_button.click()


if __name__ == '__main__':
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument("service_args=['–ignore-ssl-errors=true', '–ssl-protocol=TLSv1']")
#     chrome_options.add_argument('--no-sandbox')
#     chrome_options.add_argument('--disable-gpu')
#     chrome_options.add_argument('--disable-dev-shm-usage')
    chromedriver = "/usr/bin/chromedriver"
    os.environ["webdriver.chrome.driver"] = chromedriver
    driver = webdriver.Chrome(chrome_options=options,
                              executable_path=chromedriver)
    driver.implicitly_wait(30)
    driver.set_page_load_timeout(30)
    driver.set_script_timeout(30)
    try:
        driver.get("https://tieba.baidu.com/index.html")
    except:
        driver.execute_script('window.stop()')

    cookie_list = os.environ['COOKIE'].split(';')
    for kv in cookie_list:
        k, v = kv.strip().split('=', 1)
        driver.add_cookie({
            "name": k,
            "value": v,
        })
    driver.refresh()
    if not os.path.exists('cache.txt') or os.path.getsize('cache.txt') == 0:
        get_tieba_url(driver)
    with open('cache.txt', 'r', encoding='UTF-8') as f:
        for url in f.readlines():
            url = url.strip()
            sign_in(driver, url)
            time.sleep(0.5)
    driver.quit()
