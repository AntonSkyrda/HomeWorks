FROM ubuntu:latest

RUN apt-get update && \
    apt-get install -y python3 python3-pip curl && \
    apt-get clean

RUN update-alternatives --install /usr/bin/python python /usr/bin/python3 1

RUN curl -sSL https://install.python-poetry.org | python3 - && \
    ln -s /root/.local/bin/poetry /usr/bin/poetry

ENV POETRY_VIRTUALENVS_CREATE=false

WORKDIR /src

COPY . /src

RUN poetry install --no-root

EXPOSE 5000

CMD ["python", "app.py"]
