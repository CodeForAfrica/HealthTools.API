FROM python:2.7.13
COPY . /api-healthtools
WORKDIR /api-healthtools
RUN pip install -r requirements.txt
CMD ["gunicorn", "api_healthtools_ke.nurses:app"]
