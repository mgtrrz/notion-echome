FROM python:3.9

COPY . /app

WORKDIR /app

RUN pip install -r requirements.txt

EXPOSE 8000

CMD ["gunicorn"  , "-b", "0.0.0.0:8000", "--chdir", "./notion-echome", "app:app"]