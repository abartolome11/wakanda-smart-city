FROM python:3.12-slim

WORKDIR /app

ENV PYTHONPATH=/app

RUN pip install --no-cache-dir \
    fastapi uvicorn requests httpx tenacity \
    prometheus_client \
    opentelemetry-api \
    opentelemetry-sdk \
    opentelemetry-exporter-otlp \
    opentelemetry-instrumentation-fastapi

COPY . .

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
