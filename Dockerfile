FROM python:3.9-slim

RUN apt-get update \
    && apt-get install -y gcc libpq-dev \
    && apt-get clean

WORKDIR /app
COPY . /app

RUN python -m venv /venv
RUN /venv/bin/pip install --upgrade pip
RUN /venv/bin/pip install .

EXPOSE 5000

CMD ["/venv/bin/python", "-m", "event-ticketing"]
