FROM python:3.9.1
ENV PYTHONUNBUFFERED=1

RUN mkdir /uks
WORKDIR /uks
ADD . /uks

COPY requirements.txt /uks/
RUN pip install -r requirements.txt
COPY . /uks/

RUN ["chmod", "+x", "wait_for_db.sh"]
RUN ["chmod", "+x", "start_app.sh"]