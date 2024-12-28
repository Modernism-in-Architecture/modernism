###############################
# Stage 1: Build dependencies #
###############################

FROM --platform=linux/arm64 python:3.10-slim-bullseye AS build

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update && apt-get install -y \
    libpq-dev \
    bash \
    gcc \
    build-essential \
    python3-dev \
    && apt-get clean

COPY ../requirements/ /requirements/

RUN pip install --upgrade pip && pip install --no-cache-dir -r /requirements/dev.txt

##########################
# Stage 2: Runtime image #
##########################

FROM --platform=linux/arm64 python:3.10-slim-bullseye

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update && apt-get install -y libpq-dev && apt-get clean && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY ../app/ /app/

COPY --from=build /usr/local/ /usr/local/

CMD ["gunicorn", "modernism.wsgi:application", "--bind", "0.0.0.0:8000"]
