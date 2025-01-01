FROM python:3.12-alpine

RUN mkdir /webapp

COPY . /webapp/

WORKDIR /webapp

CMD ["sh", "start.sh"]

EXPOSE 8080