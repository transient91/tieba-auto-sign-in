import time
from selenium import webdriver
import json

if __name__ == '__main__':
    driver = webdriver.Edge()
    driver.implicitly_wait(5)
    driver.set_page_load_timeout(5)
    driver.set_script_timeout(5)
    try:
        driver.get("https://tieba.baidu.com/index.html")
    except:
        driver.execute_script('window.stop()')

    with open('info.json', 'r', encoding='UTF-8') as f:
        info = json.load(f)
    cookies = info['cookie']
    cookie_list = cookies.split(';')
    for kv in cookie_list:
        k, v = kv.strip().split('=', 1)
        driver.add_cookie({
            "name": k,
            "value": v,
        })
    driver.refresh()
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
