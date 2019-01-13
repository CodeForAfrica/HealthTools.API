FROM python:2.7
ENV DEBIAN_FRONTEND noninteractive

COPY . /htools-api

WORKDIR /htools-api

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

EXPOSE 8000

CMD ["gunicorn", "--workers=2", "--bind=0.0.0.0:8000", "healthtools.manage:app"]
