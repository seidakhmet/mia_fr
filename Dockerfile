FROM python:3.10 as python-base

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWIRTEBYTECODE=1 \
    PYSETUP_PATH=/opt/pysetup \
    APPLICATION_PATH=/usr/app
ENV VENV_PATH=$PYSETUP_PATH/.venv
ENV PATH=$VENV_PATH/bin:$PATH

RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq5 \
    gettext \
    locales

RUN sed -i -e 's/# ru_RU.UTF-8 UTF-8/ru_RU.UTF-8 UTF-8/' /etc/locale.gen && \
    sed -i -e 's/# en_US.UTF-8 UTF-8/en_US.UTF-8 UTF-8/' /etc/locale.gen && \
    sed -i -e 's/# kk_KZ.UTF-8 UTF-8/kk_KZ.UTF-8 UTF-8/' /etc/locale.gen && \
    locale-gen && \
    update-locale LANG=ru_RU.UTF-8 && \
    echo "LANGUAGE=ru_RU.UTF-8" >> /etc/default/locale && \
    echo "LC_ALL=ru_RU.UTF-8" >> /etc/default/locale \


FROM base as builder
RUN mkdir /app
WORKDIR  /app
COPY /pyproject.toml /app
RUN pip3 install poetry
RUN poetry config virtualenvs.create false

COPY . .
RUN poetry install --without dev

RUN sed -i 's/\r$//g' /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

WORKDIR /app/src

ENTRYPOINT ["/app/entrypoint.sh"]