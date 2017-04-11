FROM python:2.7.13
WORKDIR .
RUN pip install -r requirements.txt
CMD ["python", "nurses.py"]
