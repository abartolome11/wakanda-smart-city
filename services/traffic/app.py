from fastapi import FastAPI, Response
from prometheus_client import Counter, generate_latest, CONTENT_TYPE_LATEST
import random
import requests
import os


app = FastAPI(title="Traffic Service")

from otel import setup_tracing
setup_tracing(app, "traffic")

REQUESTS = Counter(
    "traffic_requests_total",
    "Total number of traffic service requests"
)

REGISTRY_URL = os.getenv("REGISTRY_URL")

@app.on_event("startup")
def register_service():
    if REGISTRY_URL:
        requests.post(
            f"{REGISTRY_URL}/registry/register",
            json={
                "name": "traffic",
                "url": "http://traffic:8000"
            }
        )

@app.get("/traffic/status")
def traffic_status():
    REQUESTS.inc()
    return {
        "intersection_id": "I-12",
        "vehicle_count": random.randint(100, 400),
        "average_speed_kmh": round(random.uniform(10, 35), 1),
        "signal_phase": "NS_GREEN"
    }

@app.get("/metrics")
def metrics():
    return Response(
        content=generate_latest(),
        media_type=CONTENT_TYPE_LATEST
    )

