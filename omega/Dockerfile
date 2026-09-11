FROM python:3.13-slim

RUN pip install --no-cache-dir --upgrade pip uv

WORKDIR /app/omega

COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-install-project

COPY . .
RUN uv sync --frozen

RUN mkdir -p /app/omega_working_directory

ENV PATH="/app/omega/.venv/bin:$PATH"

ENTRYPOINT ["omega"]
