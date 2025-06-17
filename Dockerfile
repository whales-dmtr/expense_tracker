FROM python:3.13.3-slim

WORKDIR /app

COPY . .

RUN pip3 install -r requirements.txt

EXPOSE 8000

ENTRYPOINT [ "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000" ]