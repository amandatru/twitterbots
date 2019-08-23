FROM python:2.7-alpine

COPY . /bots/
COPY requirements.txt /tmp
RUN pip install -r /tmp/requirements.txt
RUN pip install python-musixmatch

WORKDIR /bots
CMD ["python", "tweety_bot.py"]
