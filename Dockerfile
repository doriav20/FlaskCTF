FROM python:3.14-slim AS builder

WORKDIR /build

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    UV_LINK_MODE=copy \
    UV_NO_DEV=1 \
    UV_UNMANAGED_INSTALL=/uv-bin \
    VIRTUAL_ENV=/build/.venv \
    PATH="/build/.venv/bin:/uv-bin:${PATH}"

RUN apt-get update && apt-get install -y --no-install-recommends \
    curl ca-certificates dos2unix \
    && rm -rf /var/lib/apt/lists/*

RUN curl -LsSf https://astral.sh/uv/install.sh | sh

COPY pyproject.toml uv.lock ./

RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --locked --no-install-project --no-dev

COPY app.py constants.py utils.py ./
COPY templates ./templates
COPY static ./static
COPY secret/is_admin ./secret/is_admin
COPY utils/admins_example.txt ./utils/admins_example.txt

RUN dos2unix ./utils/admins_example.txt

RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --locked --no-dev


FROM python:3.14-slim AS runtime

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    VIRTUAL_ENV=/app/.venv \
    PATH="/app/.venv/bin:/uv-bin:${PATH}"

COPY --from=builder /uv-bin /uv-bin
COPY --from=builder /build/.venv /app/.venv
COPY --from=builder /build/app.py /app/app.py
COPY --from=builder /build/constants.py /app/constants.py
COPY --from=builder /build/utils.py /app/utils.py
COPY --from=builder /build/templates /app/templates
COPY --from=builder /build/static /app/static
COPY --from=builder /build/secret/is_admin /app/secret/is_admin
COPY --from=builder /build/utils/admins_example.txt /tmp/admins.txt

EXPOSE 5000

CMD ["uv", "run", "python", "app.py"]
