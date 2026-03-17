FROM python:3.13-slim
WORKDIR /app

COPY pyproject.toml uv.lock ./
COPY src/ ./src/

RUN pip install uv
RUN uv sync --frozen

CMD ["uv", "run", "python", "src/server.py"]
