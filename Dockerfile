FROM python:3.6
RUN apt-get update && apt-get -y install zip git && pip install awscli bumpversion