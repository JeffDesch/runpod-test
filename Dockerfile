FROM python:3.11.1-buster

WORKDIR /

RUN pip install runpod
RUN pip install elevenlabs

ADD start.py .

CMD [ "python", "-u", "/start.py" ]