FROM python:2.7.13

COPY . /htools-api

WORKDIR /htools-api

RUN pip install -r requirements.txt

CMD ["gunicorn", "manage:app"]
