import os
import yaml

# const
ENV_AWS = 'aws'
ENV_LOCAL = 'local'
LOG_LEVEL_DEFAULT = 'INFO'

# from os env
ENV = os.environ['ENV'] if 'ENV' in os.environ.keys() else ENV_LOCAL
YML_PATH = os.environ['YML_PATH'] if 'YML_PATH' in os.environ.keys() \
    else 'conf/conf.yml'
LOG_LEVEL = os.environ['LOG_LEVEL'] if 'LOG_LEVEL' in os.environ.keys() else LOG_LEVEL_DEFAULT

# from yml file
with open(YML_PATH) as f:
    yml = yaml.load(f, Loader=yaml.SafeLoader)
DRIVER_PATH = yml['CheckOnepanman']['ChromeDriverPath']
TARGET_URL = yml['CheckOnepanman']['TargetURL']
SCROLL_DOWN = yml['CheckOnepanman']['ScrollDownNum']
KEY_FILE_PATH = yml['CheckOnepanman']['KeyFilePath']
AWS_ACCESS_ID = yml['CheckOnepanman']['AWS']['AccessKeyId']
AWS_SECRET_KEY = yml['CheckOnepanman']['AWS']['SecretAccessKey']
AWS_SNS_TOPIC = yml['CheckOnepanman']['AWS']['SNSTopicARN']
AWS_S3_BUDGET = yml['CheckOnepanman']['AWS']['S3BudgetName']
AWS_S3_KEYFILE_PATH = yml['CheckOnepanman']['AWS']['S3KeyFilePth']

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
