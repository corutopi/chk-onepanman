###########################################################
# base image:
#   # docekr image のベースとしてはdebianのほうがメジャー？
#   # python3(や selenium)の公式イメージに乗り換えるのもありかも.
#
# GoogleChrome:
#   $ google-chrome-stable -version -> Google Chrome 84.0.4147.125
#   ! May change when docker image update(or remake) !
#
###########################################################

# base image
FROM centos:7

# setting
WORKDIR /root

# install basic command
RUN yum install -y unzip

# install python
# install pip
RUN yum install -y python3-3.6.8 python3-pip-9.0.3-7.el7_7

# setup chrome-webdriver
## まるまる以下を参考に作成. 構成等については要理解.
## https://qiita.com/onorioriori/items/4fa271daa3621e8f6fd9
### install Google Chrome
# version confirmation command
# $ google-chrome -version
# $ google-chrome-stable -version
RUN curl https://intoli.com/install-google-chrome.sh | bash

### install GConf2
RUN yum install -y GConf2-3.2.6-8.el7

### install ChromeDriver
# version confirmation command
# $ chromedriver --version
# new driver search below URL.
#   https://chromedriver.chromium.org/downloads
# Notes:
#   GoogleChrome can be installed with only the latest version (really?).
#   So ChromeDriver also need to be installed the latest version.
#   Use LATEST_RELEASE tag to get the latest version number of ChromeDirver.
RUN export CD_LATEST_VERSION=`curl https://chromedriver.storage.googleapis.com/LATEST_RELEASE` && \
    wget https://chromedriver.storage.googleapis.com/${CD_LATEST_VERSION}/chromedriver_linux64.zip && \
    unzip chromedriver_linux64.zip && \
    mv chromedriver /usr/local/bin && \
    rm -f chromedriver_linux64.zip

### install GoogleNotoFonts (only use scheenshot)
#### over 1G byte
RUN mkdir -p ./tmp && cd ./tmp && \
    wget https://noto-website-2.storage.googleapis.com/pkgs/Noto-hinted.zip && \
    unzip Noto-hinted.zip && \
    mkdir -p /usr/share/fonts/opentype/noto && \
    mv *otf *ttf /usr/share/fonts/opentype/noto && \
    fc-cache -f -v && \
    cd ../ && rm -rf ./tmp

# install awscli
RUN mkdir -p ./tmp && cd ./tmp && \
    curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip" && \
    unzip awscliv2.zip && \
    ./aws/install && \
    cd ../ && rm -rf ./tmp

# locale setting
RUN localedef -i ja_JP -c -f UTF-8 -A /usr/share/locale/locale.alias ja_JP.UTF-8
ENV LANG ja_JP.UTF-8

# install other python package
## requirements.txt と同期させられないか？
RUN pip3 install selenium==3.141.0 PyYAML==5.3.1 boto3==1.14.46

# copy script file
COPY ./main.py ./
COPY ./entry_point.sh ./
COPY ./src ./src
RUN mkdir ./dynamic

# default env
ENV LOG_LEVEL INFO

# assignment entry_point
ENTRYPOINT sh ./entry_point.sh
