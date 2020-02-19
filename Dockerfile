FROM python:3.6

# The environment variable ensures that the python output is set straight
# to the terminal with out buffering it first
ENV PYTHONUNBUFFERED 1

RUN mkdir /interview-calendar

WORKDIR /interview-calendar

ADD . /interview-calendar/

RUN pip install -r requirements.txt