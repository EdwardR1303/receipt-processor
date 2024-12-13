FROM python:3.11-slim-buster

WORKDIR /app

COPY requirements.txt requirements.txt

RUN python -m pip install -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["python", "app.py"]