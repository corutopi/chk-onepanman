import src.conf as conf
from abc import ABCMeta, abstractmethod
import logging
import boto3


def getProcess():
    if conf.ENV == conf.ENV_AWS:
        return AwsProcess()
    elif conf.ENV == conf.ENV_LOCAL:
        return LocalProcess()


class MainProcess(metaclass=ABCMeta):
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


class AwsProcess(MainProcess):
    def sendmail(self, story_num):
        sns = boto3.client(service_name='sns',
                           aws_access_key_id=conf.AWS_ACCESS_ID,
                           aws_secret_access_key=conf.AWS_SECRET_KEY,
                           region_name='ap-northeast-1')
        message = """
        ワンパンマン 第{}話 が更新されました。
        サイトで確認しましょう！
        """
        response = sns.publish(TopicArn=conf.SNS_TOPIC,
                               Message=message.format(story_num),
                               Subject='Update Onepanman No.{}'.format(
                                   story_num))
        logging.debug(response)

    def put_story_num(self, key_file_path, num):
        tmp_file = 'dynamic/tmp.txt'
        s3 = boto3.resource(service_name='s3',
                            aws_access_key_id=conf.AWS_ACCESS_ID,
                            aws_secret_access_key=conf.AWS_SECRET_KEY)
        bucket = s3.Bucket('ss-common-s3')
        bucket.download_file('chkOnepanman/key.txt', tmp_file)

        logging.debug('Next Story Number is ... {}.'.format(num + 1))
        with open(tmp_file, mode='w') as f:
            f.write(str(num + 1))
        bucket.upload_file(tmp_file, 'chkOnepanman/key.txt')

    def get_story_num(self, key_file_path):
        tmp_file = 'dynamic/tmp.txt'
        s3 = boto3.resource(service_name='s3',
                            aws_access_key_id=conf.AWS_ACCESS_ID,
                            aws_secret_access_key=conf.AWS_SECRET_KEY)
        bucket = s3.Bucket('ss-common-s3')
        bucket.download_file('chkOnepanman/key.txt', tmp_file)

        with open(tmp_file) as f:
            story_num = int(f.read())

        # with open(key_file_path) as f:
        #     story_num = int(f.read())
        return story_num

    def check_latest_story_num(self):
        pass


class LocalProcess(MainProcess):
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
