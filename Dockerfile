FROM python:2.7-alpine
COPY requirements.txt /
RUN pip install -r /requirements.txt
WORKDIR /usr/src/app
COPY telldus_exporter.py /usr/src/app
CMD ["python", "/usr/src/app/telldus_exporter.py"]
