###############################
# Stage 1: Build dependencies #
###############################

FROM python:3.10-slim-bullseye AS build

ARG PLATFORM
RUN echo "Runtime environment: $PLATFORM"

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update && apt-get install -y \
    libpq-dev \
    bash \
    gcc \
    build-essential \
    python3-dev \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

COPY ../requirements/ /requirements/

RUN pip install --upgrade pip && \
    if [ "$PLATFORM" = "dev" ]; then \
        pip install --no-cache-dir -r /requirements/dev.txt; \
    else \
        pip install --no-cache-dir -r /requirements/prod.txt; \
    fi

##########################
# Stage 2: Runtime image #
##########################

FROM python:3.10-slim-bullseye

ARG PLATFORM
RUN echo "Runtime environment: $PLATFORM"

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update && apt-get install -y libpq5 && apt-get clean && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY ../app/ /app/

COPY ../docker/entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

COPY --from=build /usr/local/ /usr/local/

ENTRYPOINT ["/app/entrypoint.sh"]
CMD ["gunicorn", "modernism.wsgi:application", "--bind", "0.0.0.0:8000"]
