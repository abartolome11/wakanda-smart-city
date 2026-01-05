from fastapi import FastAPI, Response
from prometheus_client import Counter, generate_latest, CONTENT_TYPE_LATEST
import random, requests, os

app = FastAPI(title="Waste Service")

from otel import setup_tracing
setup_tracing(app, "waste")

REQUESTS = Counter("waste_requests_total", "Waste service requests")
REGISTRY_URL = os.getenv("REGISTRY_URL")

@app.on_event("startup")
def register():
    if REGISTRY_URL:
        requests.post(
            f"{REGISTRY_URL}/registry/register",
            json={"name": "waste", "url": "http://waste:8000"}
        )

@app.get("/waste/containers")
def containers():
    REQUESTS.inc()
    return {
        "avg_fill_percentage": random.randint(20, 95),
        "containers_total": 120
    }

@app.get("/metrics")
def metrics():
    return Response(
        content=generate_latest(),
        media_type=CONTENT_TYPE_LATEST
    )

