FROM python:3.13-slim
WORKDIR /app

COPY pyproject.toml uv.lock ./
COPY src/ ./src/

RUN pip install uv
RUN uv sync

CMD ["uv", "run", "python", "-m", "src.server"]
