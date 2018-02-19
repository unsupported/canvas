FROM python:3

WORKDIR /usr/src/app

ADD odbcinst.ini /etc/odbcinst.ini

RUN apt-get update && apt-get -y install gcc

RUN apt-get install -y tdsodbc unixodbc-dev

RUN apt install unixodbc-bin -y

RUN apt-get clean -y

COPY . .

RUN pip install -r requirements.txt

CMD [ "python", "./main.py" ]