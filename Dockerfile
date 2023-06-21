from python:3.11

WORKDIR /

RUN pip install runpod

ADD start.py .

CMD [ "python", "-u", "/start.py" ]