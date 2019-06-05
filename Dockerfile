FROM python:3.6
RUN apt-get update && apt-get install zip git && pip install awscli bumpversion