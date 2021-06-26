FROM python:3.8

WORKDIR / flask_blog_app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY ./app ./app

CMD ["python", "./app/app.py"]