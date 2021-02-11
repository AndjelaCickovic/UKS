FROM python:3.9.1
ENV PYTHONUNBUFFERED=1
WORKDIR /uks_project
COPY requirements.txt /uks_project/
RUN pip install -r requirements.txt
COPY . /uks_project/