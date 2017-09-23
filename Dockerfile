FROM python:3.6.2
ADD . /logger
WORKDIR /logger
RUN pip install -r requirements.txt

CMD ["python", "run.py"]
