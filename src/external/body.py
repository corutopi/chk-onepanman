import src.conf as conf
from abc import ABCMeta, abstractmethod
import logging
import boto3


def getProcess():
    if conf.RUN_MODE == conf.MODE_AWS:
        return AwsProcess()
    elif conf.RUN_MODE == conf.MODE_LOCAL:
        return LocalProcess()


class TemplateProcess(metaclass=ABCMeta):
    def __init__(self):
        pass

    @abstractmethod
    def sendmail(self, story_num):
        pass

    @abstractmethod
    def put_story_num(self, key_file_path, num):
        pass

    @abstractmethod
    def get_story_num(self, key_file_path):
        pass

    @abstractmethod
    def check_latest_story_num(self):
        pass


class AwsProcess(TemplateProcess):
    def sendmail(self, story_num):
        sns = boto3.client(service_name='sns',
                           aws_access_key_id=conf.AWS_ACCESS_ID,
                           aws_secret_access_key=conf.AWS_SECRET_KEY,
                           region_name='ap-northeast-1')
        message = """
        ワンパンマン 第{storynum}話 が更新されました。
        サイトで確認しましょう！
        
        {url}
        """.format(storynum=story_num, url=conf.TARGET_URL)
        logging.debug('send message: {}'.format(message))
        response = sns.publish(TopicArn=conf.AWS_SNS_TOPIC,
                               Message=message,
                               Subject='Update Onepanman No.{}'.format(
                                   story_num))
        logging.debug(response)

    def put_story_num(self, key_file_path, num):
        tmp_file = conf.KEY_FILE_PATH
        s3 = boto3.resource(service_name='s3',
                            aws_access_key_id=conf.AWS_ACCESS_ID,
                            aws_secret_access_key=conf.AWS_SECRET_KEY)
        bucket = s3.Bucket(conf.AWS_S3_BUDGET)
        bucket.download_file(conf.AWS_S3_KEYFILE_PATH, tmp_file)

        logging.debug('Next Story Number is ... {}.'.format(num + 1))
        with open(tmp_file, mode='w') as f:
            f.write(str(num + 1))
        bucket.upload_file(tmp_file, conf.AWS_S3_KEYFILE_PATH)

    def get_story_num(self, key_file_path):
        tmp_file = conf.KEY_FILE_PATH
        s3 = boto3.resource(service_name='s3',
                            aws_access_key_id=conf.AWS_ACCESS_ID,
                            aws_secret_access_key=conf.AWS_SECRET_KEY)
        bucket = s3.Bucket(conf.AWS_S3_BUDGET)
        bucket.download_file(conf.AWS_S3_KEYFILE_PATH, tmp_file)

        with open(tmp_file) as f:
            story_num = int(f.read())

        # with open(key_file_path) as f:
        #     story_num = int(f.read())
        return story_num

    def check_latest_story_num(self):
        pass


class LocalProcess(TemplateProcess):
    def sendmail(self, story_num):
        logging.debug('Target Web-page was updated ! Let\'s Check now !')

    def put_story_num(self, key_file_path, num):
        with open(key_file_path, mode='w') as f:
            f.write(str(num + 1))

    def get_story_num(self, key_file_path):
        with open(key_file_path) as f:
            story_num = int(f.read())
        return story_num

    def check_latest_story_num(self):
        pass
