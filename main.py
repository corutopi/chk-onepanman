import os
import sys
from time import sleep
from logging import INFO, DEBUG
from logging import getLogger, StreamHandler, basicConfig

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import yaml

# ENV, YML_PATH
ENV = os.environ['ENV'] if 'ENV' in os.environ.keys() else 'local'
YML_PATH = os.environ['YML_PATH'] if 'YML_PATH' in os.environ.keys() \
    else 'conf/conf.yml'

# about log
basicConfig(stream=sys.stdout,
            level=None,
            format="%(asctime)s [%(filename)s:%(lineno)d] %(levelname)-8s %(message)s")
logger = getLogger(__name__)
logger.setLevel(INFO)


# env 毎にymlファイルを取得
path = ''
if ENV == 'local':
    path = YML_PATH
    import src.util.local.util as util
elif ENV == 'aws':
    # from S3
    path = YML_PATH
    import src.util.aws.util as util

with open(path) as f:
    yml = yaml.load(f, Loader=yaml.SafeLoader)
DRIVER_PATH = yml['CheckOnepanman']['ChromeDriverPath']
TARGET_URL = yml['CheckOnepanman']['TargetURL']
SCROLL_DOWN = yml['CheckOnepanman']['ScrollDownNum']
KEY_FILE_PATH = yml['CheckOnepanman']['KeyFilePath']
AWS_ACCESS_ID = yml['CheckOnepanman']['AWS']['AccessKeyId']
AWS_SECRET_KEY = yml['CheckOnepanman']['AWS']['SecretAccessKey']
SNS_TOPIC = yml['CheckOnepanman']['AWS']['SNSTopicARN']

story_num = util.get_story_num(KEY_FILE_PATH, AWS_ACCESS_ID, AWS_SECRET_KEY)
key_str = '第{}話'.format(story_num)


def main():
    logger.info('Process Start.')
    logger.info('Startup Chrome Driver.')
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-gpu')
    options.add_argument('--window-size=1280,1024')

    driver = webdriver.Chrome(executable_path=DRIVER_PATH, options=options)

    logger.info('Access target URL.')
    driver.get(TARGET_URL)
    body_element = driver.find_element_by_id('page-viewer')
    sleep(5)  # read wait

    logger.info('Scroll down to read story item.')
    driver.execute_script(
        'window.scrollTo(0, window.pageYOffset + {});'.format(SCROLL_DOWN))
    sleep(5)  # read wait
    logger.info('Get page text.')
    check_txt = body_element.text

    driver.close()
    driver.quit()

    if key_str in check_txt:
        logger.info('Web page is updated ({})'.format(key_str))
        util.sendmail(story_num=story_num,
                      sns_topic=SNS_TOPIC,
                      access_key_id=AWS_ACCESS_ID,
                      secret_access_key=AWS_SECRET_KEY)
        util.put_story_num(KEY_FILE_PATH, story_num,
                           access_key_id=AWS_ACCESS_ID,
                           secret_access_key=AWS_SECRET_KEY)
    else:
        logger.info('no update ({})'.format(key_str))
    logger.info('Process End.')


if __name__ == '__main__':
    main()
