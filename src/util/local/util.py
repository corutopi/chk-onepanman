import logging


def sendmail(story_num, sns_topic=None, access_key_id=None, secret_access_key=None):
    logging.info('Target Web-page was updated ! Let\'s Check now !')


def put_story_num(key_file_path, num, access_key_id=None,
                  secret_access_key=None):
    with open(key_file_path, mode='w') as f:
        f.write(str(num + 1))


def get_story_num(key_file_path, access_key_id=None, secret_access_key=None):
    with open(key_file_path) as f:
        story_num = int(f.read())
    return story_num
