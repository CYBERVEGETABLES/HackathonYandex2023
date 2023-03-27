FROM python:alpine

WORKDIR /app

# For Poetry
ENV PATH="/root/.local/bin:$PATH"

RUN apk update && \
    apk upgrade && \
    apk --no-cache add curl firefox && \
    rm -rf /var/cache/apk/*

COPY pyproject.toml poetry.lock ./
COPY src/ src/

RUN curl -sSL https://install.python-poetry.org | python3 - && \
    poetry install --no-interaction --no-cache --without dev

ENTRYPOINT ["poetry", "run", "python"]

CMD ["src/main.py"]
