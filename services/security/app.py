from fastapi import FastAPI, Response
from prometheus_client import Counter, generate_latest, CONTENT_TYPE_LATEST
import random, requests, os

app = FastAPI(title="Security Service")

from otel import setup_tracing
setup_tracing(app, "security")

REQUESTS = Counter("security_requests_total", "Security service requests")
REGISTRY_URL = os.getenv("REGISTRY_URL")

@app.on_event("startup")
def register():
    if REGISTRY_URL:
        requests.post(
            f"{REGISTRY_URL}/registry/register",
            json={"name": "security", "url": "http://security:8000"}
        )

@app.get("/security/events")
def events():
    REQUESTS.inc()
    return {
        "active_alerts": random.randint(0, 5),
        "level": "low"
    }

@app.get("/metrics")
def metrics():
    return Response(
        content=generate_latest(),
        media_type=CONTENT_TYPE_LATEST
    )
