FROM python:3.9

WORKDIR /geoinfo/app

COPY app/requirements.txt .

RUN pip install -r requirements.txt

COPY ./app .

CMD ["python3","-m", "flask", "run", "--host=0.0.0.0"]
