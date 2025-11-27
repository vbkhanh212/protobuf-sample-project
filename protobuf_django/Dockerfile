FROM python:3.13-slim-bullseye

WORKDIR /protobuf_django

COPY . /protobuf_django/

RUN pip install --no-cache-dir -r requirements.txt

CMD ["./run_granian.sh"]
