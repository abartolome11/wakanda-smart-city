from fastapi import FastAPI, Response
from prometheus_client import Counter, generate_latest, CONTENT_TYPE_LATEST
import random, requests, os

app = FastAPI(title="Energy Service")

from otel import setup_tracing
setup_tracing(app, "energy")

REQUESTS = Counter("energy_requests_total", "Energy service requests")
REGISTRY_URL = os.getenv("REGISTRY_URL")

@app.on_event("startup")
def register():
    if REGISTRY_URL:
        requests.post(
            f"{REGISTRY_URL}/registry/register",
            json={"name": "energy", "url": "http://energy:8000"}
        )

@app.get("/energy/grid")
def grid_status():
    REQUESTS.inc()
    return {
        "grid_load_mw": random.randint(500, 1200),
        "renewable_percentage": random.randint(20, 80)
    }

@app.get("/metrics")
def metrics():
    return Response(
        content=generate_latest(),
        media_type=CONTENT_TYPE_LATEST
    )

