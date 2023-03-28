FROM python:alpine

WORKDIR /app

# For Poetry
ENV PATH="/root/.local/bin:$PATH"

RUN apk update && \
    apk upgrade && \
    apk --no-cache add curl firefox gcc && \
    rm -rf /var/cache/apk/*

COPY pyproject.toml poetry.lock ./

RUN pip install --upgrade pip

RUN curl -sSL https://install.python-poetry.org | python3 - && \
    poetry install --no-interaction --no-cache --without dev

COPY src/ src/

ENTRYPOINT ["poetry", "run", "python"]

CMD ["src/main.py"]
