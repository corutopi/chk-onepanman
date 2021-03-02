import os
import yaml

# ENV, YML_PATH
ENV = os.environ['ENV'] if 'ENV' in os.environ.keys() else 'local'
YML_PATH = os.environ['YML_PATH'] if 'YML_PATH' in os.environ.keys() \
    else 'conf/conf.yml'

with open(YML_PATH) as f:
    yml = yaml.load(f, Loader=yaml.SafeLoader)
DRIVER_PATH = yml['CheckOnepanman']['ChromeDriverPath']
TARGET_URL = yml['CheckOnepanman']['TargetURL']
SCROLL_DOWN = yml['CheckOnepanman']['ScrollDownNum']
KEY_FILE_PATH = yml['CheckOnepanman']['KeyFilePath']
AWS_ACCESS_ID = yml['CheckOnepanman']['AWS']['AccessKeyId']
AWS_SECRET_KEY = yml['CheckOnepanman']['AWS']['SecretAccessKey']
SNS_TOPIC = yml['CheckOnepanman']['AWS']['SNSTopicARN']

# class Config():
#     _load_cnt = 0
#     """
#     ここに設定値を定義
#     """
#     DRIVER_PATH = ''
#     TARGET_URL = ''
#     SCROLL_DOWN = ''
#     KEY_FILE_PATH = ''
#     AWS_ACCESS_ID = ''
#     AWS_SECRET_KEY = ''
#
#     def __init__(self, conf_path=''):
#         self._conf_path = conf_path
#         pass
#
#     def load(self):
#         if self._load_cnt > 0:
#             """警告を出す"""
#             pass
