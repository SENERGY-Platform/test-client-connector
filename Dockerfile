FROM python:3-alpine

ARG branch
ENV BRANCH=${branch}

WORKDIR /usr/src/app

RUN apk update && apk upgrade && apk add --no-cache git

RUN pip install --no-cache-dir git+https://github.com/SENERGY-Platform/client-connector-lib.git@$BRANCH

COPY . .

RUN mkdir cc-lib
RUN mkdir storage

CMD [ "python", "./client.py"]
