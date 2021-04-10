# chk-onepanman

build
```
docker build -t chk-onepanman .
```
```
docker-compose build
```

run on local
```
docker run -e YML_LOCATION=local ^
           -e YML_PATH=[YmlFilePath] ^
           -e LOG_LEVEL=[PythonLoggingLoglevel like DEBUG, INFO, etc ... ] ^
           -v [LocalDyanmicFolder]:[YmlFolder] ^
           -v [LocalConfFolder]:[DockerConfFolder] ^
           --rm ^
           chk-onepanman:latest
```

run on aws
```
docker run -e YML_LOCATION=aws \
           -e YML_PATH=/root/conf/conf.yml \
           -e LOG_LEVEL=[PythonLoggingLoglevel like DEBUG, INFO, etc ... ] \
           -e S3_YML_PATH=[yml file(make from tmplate) path on AWS S3.] \
           --rm \
           chk-onepanman:latest
```

--trial--
```plantuml
class "Config" as conf {
    singleton class.
}

abstract "TemplateProcess" as tp {
    +get_story_num()
    +put_story_num()
    +send_mail()
}

class "AWSProcess" as aws {
}

class "LocalProcess" as local {
}

tp <|-- aws
tp <|-- local
aws --> conf : view
local --> conf : view
```
