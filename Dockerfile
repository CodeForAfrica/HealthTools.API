FROM python:3.7
ENV DEBIAN_FRONTEND noninteractive

COPY . /htools-api

WORKDIR /htools-api

RUN pip install --upgrade pip
RUN pip install -r requirements.txt && pip install --upgrade requests
RUN pip install -e .

EXPOSE 8000

CMD ["gunicorn", "--workers=2", "--bind=0.0.0.0:8000", "--reload", "healthtools.manage:app"]
