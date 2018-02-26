FROM python:3.6

RUN pip install aiohttp
ADD . /app
WORKDIR /app

EXPOSE 8080
CMD python3 mastermaster.py
