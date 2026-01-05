from fastapi import FastAPI, HTTPException
import httpx
import os

from service_client import ServiceClient

app = FastAPI(title="Wakanda API Gateway")

from otel import setup_tracing
setup_tracing(app, "gateway")


REGISTRY_URL = os.getenv("REGISTRY_URL")

async def get_client(service_name: str) -> ServiceClient:
    async with httpx.AsyncClient() as client:
        r = await client.get(f"{REGISTRY_URL}/registry/{service_name}")
        instances = r.json()

    if not instances:
        raise HTTPException(status_code=503, detail=f"{service_name} unavailable")

    return ServiceClient(instances)

@app.get("/traffic/status")
async def traffic():
    client = await get_client("traffic")
    return await client.get("/traffic/status")

@app.get("/energy/grid")
async def energy():
    client = await get_client("energy")
    return await client.get("/energy/grid")

@app.get("/water/pressure")
async def water():
    client = await get_client("water")
    return await client.get("/water/pressure")

@app.get("/waste/containers")
async def waste():
    client = await get_client("waste")
    return await client.get("/waste/containers")

@app.get("/security/events")
async def security():
    client = await get_client("security")
    return await client.get("/security/events")
