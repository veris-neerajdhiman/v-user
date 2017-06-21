FROM django

WORKDIR /v-user


ADD ./requirements/base.txt /v-user/requirements/base.txt
RUN apt-get update && apt-get install -y git

RUN pip install -r ./requirements/base.txt

ADD . /v-user

EXPOSE 80

COPY ./config/docker/docker-entrypoint.sh /
ENTRYPOINT ["./config/docker/docker-entrypoint.sh"]