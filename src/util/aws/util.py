import boto3
import logging


def sendmail(story_num, sns_topic, access_key_id=None, secret_access_key=None):
    sns = boto3.client(service_name='sns',
                       aws_access_key_id=access_key_id,
                       aws_secret_access_key=secret_access_key,
                       region_name='ap-northeast-1')
    message = """
    ワンパンマン 第{}話 が更新されました。
    サイトで確認しましょう！
    """
    topic = sns_topic
    response = sns.publish(TopicArn=topic,
                           Message=message.format(story_num),
                           Subject='Update Onepanman No.{}'.format(story_num))
    logging.debug(response)


def put_story_num(key_file_path, num, access_key_id=None,
                     secret_access_key=None):
    tmp_file = 'dynamic/tmp.txt'
    s3 = boto3.resource(service_name='s3',
                        aws_access_key_id=access_key_id,
                        aws_secret_access_key=secret_access_key)
    bucket = s3.Bucket('ss-common-s3')
    bucket.download_file('chkOnepanman/key.txt', tmp_file)

    logging.debug('Next Story Number is ... {}.'.format(num + 1))
    with open(tmp_file, mode='w') as f:
        f.write(str(num + 1))
    bucket.upload_file(tmp_file, 'chkOnepanman/key.txt')


def get_story_num(key_file_path, access_key_id=None, secret_access_key=None):
    tmp_file = 'dynamic/tmp.txt'
    s3 = boto3.resource(service_name='s3',
                        aws_access_key_id=access_key_id,
                        aws_secret_access_key=secret_access_key)
    bucket = s3.Bucket('ss-common-s3')
    bucket.download_file('chkOnepanman/key.txt', tmp_file)

    with open(tmp_file) as f:
        story_num = int(f.read())

    # with open(key_file_path) as f:
    #     story_num = int(f.read())
    return story_num
