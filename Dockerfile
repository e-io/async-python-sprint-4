# This file is just for a test. It is not connecting to Postgres.
# To run and use this project, use instructions in Readme. Not this file.

FROM python:3.11
LABEL authors="Pavel"

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./requirements-dev.txt /code/requirements-dev.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements-dev.txt

COPY ./src /code/src

EXPOSE 8080/tcp

CMD ["uvicorn", "src.main:app", "--host", "127.0.0.1", "--port", "8080"]
