FROM python:3.12-trixie
COPY --from=ghcr.io/astral-sh/uv:0.11.4 /uv /uvx /bin/

WORKDIR /src

COPY pyproject.toml uv.lock /src/
ENV UV_NO_DEV=1
RUN uv sync --locked

COPY app /src/app
WORKDIR /src/app
EXPOSE 8000
CMD ["uv", "run", "main.py"]
