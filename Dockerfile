FROM python:2.7.13
COPY . /healthtools-ke-api
WORKDIR /healthtools-ke-api
RUN pip install -r requirements.txt
CMD ["gunicorn", "healthtools_ke_api:app"]
