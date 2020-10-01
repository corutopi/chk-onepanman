# chkOne

build
```
docker build -t chk-onepanman .
```

run on aws
```
docker run -e ENV=aws \
           -e YML_PATH=/root/conf/conf.yml \
           -e S3_YML_PATH=[yml file(make from tmplate) path on AWS S3.] \
           --rm \
           chk-onepanman:latest
```
