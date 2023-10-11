FROM python:3.10

COPY . /bot

WORKDIR /bot

RUN pip install -r requirements.txt

CMD ["python3","start.py"]