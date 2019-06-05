FROM python:3.6
ENV AWS_DEFAULT_REGION eu-west-2
RUN apt-get update && apt-get -y install zip git && pip install awscli bumpversion