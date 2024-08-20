FROM python:3
ENV PYTHONUMBUFFERED 1
RUN mkdir /app
WORKDIR /app
COPY requirements.txt /app/
RUN pip install -r requirements.txt
COPY . /app/

COPY ../downloads/* /app/biomdata/management/

COPY ../downloads /app/biomdata/management/
