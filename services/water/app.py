from fastapi import FastAPI, Response
from prometheus_client import Counter, generate_latest, CONTENT_TYPE_LATEST
import random, requests, os

app = FastAPI(title="Water Service")

from otel import setup_tracing
setup_tracing(app, "water")

REQUESTS = Counter("water_requests_total", "Water service requests")
REGISTRY_URL = os.getenv("REGISTRY_URL")

@app.on_event("startup")
def register():
    if REGISTRY_URL:
        requests.post(
            f"{REGISTRY_URL}/registry/register",
            json={"name": "water", "url": "http://water:8000"}
        )

@app.get("/water/pressure")
def pressure():
    REQUESTS.inc()
    return {
        "pressure_bar": round(random.uniform(1.5, 3.5), 2),
        "zone": "north"
    }

@app.get("/metrics")
def metrics():
    return Response(
        content=generate_latest(),
        media_type=CONTENT_TYPE_LATEST
    )
