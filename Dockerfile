FROM python:3.13.1

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /code

COPY requirements.txt .

RUN apt-get update \
&& apt-get install -y build-essential make \
&& pip install -r requirements.txt

COPY . /code

CMD [ "make", "m", "up", "r" ]