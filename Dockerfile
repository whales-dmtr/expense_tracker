FROM python:3.13.3-alpine3.22

RUN apk add --no-cache postgresql-client

WORKDIR /app

COPY . .

RUN pip3 install -r requirements.txt

RUN chmod +x /app/entrypoint.sh

EXPOSE 8000

ENTRYPOINT ["./entrypoint.sh"]
