# author_li
# create time :2018/5/1


from selenium import webdriver
from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
import time
from tools import config
# from selenium.webdriver.common.action_chains import ActionChains
# from selenium.webdriver.remote.command import Command
# from selenium.webdriver.support import expected_conditions as EC



start_setting={
    'qq_number':'xxxxxxxxx',
    'password':'xxxxxxxxx'
}

def get_cookies_():
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument(
        'user-agent={}'.format(config.UserAgents[24]))
    driver = webdriver.Chrome(chrome_options=chrome_options, executable_path='chromedriver.exe')
    driver.get('https://qzone.qq.com/')
    time.sleep(2)
    a = driver.find_element_by_id('u')
    a.send_keys(start_setting['qq_number'])
    b = driver.find_element_by_id('p')
    b.send_keys(start_setting['password'])

    c = driver.find_element_by_id('go')
    c.click()
    time.sleep(1)
    d = driver.find_element_by_id('nav_bar_me')
    d.click()
    time.sleep(1)
    driver.find_element_by_id('feed_remind_main').click()

    g_tk_key = ''
    cookie_list = []
    for i in driver.get_cookies():
        cookie = i['name'] + '=' + i['value']
        cookie_list.append(cookie)
        if i['name'] == 'p_skey':
            g_tk_key = i['value']
    cookie_str = ';'.join(cookie_list)
    driver.quit()
    print(cookie_str)
    return cookie_str,g_tk_key

def get_g_tk(g_tk_key):
    ''' make g_tk value'''

    h = 5381

    for s in g_tk_key:
        h += (h << 5) + ord(s)
    print(h & 2147483647)
    return h & 2147483647


def write_into():
    cookie, g_tk_key = get_cookies_()
    g_tk = get_g_tk(g_tk_key)
    with open('cookie.ini','w') as f:
        f.write(cookie + 'liyang' + str(g_tk))


if __name__ == '__main__':
    write_into()