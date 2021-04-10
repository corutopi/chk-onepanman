import sys
from time import sleep
from logging import INFO
from logging import getLogger, StreamHandler, basicConfig

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

import src.conf as conf
import src.external.body as body

# about log
basicConfig(stream=sys.stdout,
            level=INFO,
            format="%(asctime)s [%(filename)s:%(lineno)d] %(levelname)-8s %(message)s")
logger = getLogger(__name__)
logger.setLevel(conf.LOG_LEVEL)

ext = body.getProcess()

story_num = ext.get_story_num(conf.KEY_FILE_PATH)
key_str = '第{}話'.format(story_num)


def main():
    logger.info('Process Start.')
    logger.info('Mode: {}'.format(conf.RUN_MODE))
    logger.debug('AccessURL: {}'.format(conf.TARGET_URL))
    logger.info('Startup Chrome Driver.')
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-gpu')
    # メモリスペースを変更してエラー(下記)回避
    #   WebDriverException: Message: unknown error: session deleted because of page crash
    # 参考: https://omohikane.com/python_selenium_webdriver_crashed/
    #     : https://qiita.com/yoshi10321/items/8b7e6ed2c2c15c3344c6
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--window-size=1280,1024')

    driver = webdriver.Chrome(executable_path=conf.DRIVER_PATH, options=options)

    logger.info('Access target URL.')
    driver.get(conf.TARGET_URL)
    body_element = driver.find_element_by_id('page-viewer')
    sleep(5)  # read wait

    logger.info('Scroll down to read story item.')
    driver.execute_script(
        'window.scrollTo(0, window.pageYOffset + {});'.format(conf.SCROLL_DOWN))
    sleep(5)  # read wait
    logger.info('Get page text.')
    check_txt = body_element.text

    driver.close()
    driver.quit()

    if key_str in check_txt:
        logger.info('Web page is updated ({})'.format(key_str))
        ext.sendmail(story_num=story_num)
        ext.put_story_num(conf.KEY_FILE_PATH, story_num)
    else:
        logger.info('no update ({})'.format(key_str))
    logger.info('Process End.')


if __name__ == '__main__':
    main()
