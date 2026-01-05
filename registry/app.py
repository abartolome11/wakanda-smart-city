from fastapi import FastAPI
from pydantic import BaseModel
from typing import Dict, List

app = FastAPI(title="Service Registry")

services: Dict[str, List[str]] = {}

class Service(BaseModel):
    name: str
    url: str

@app.post("/registry/register")
def register(service: Service):
    services.setdefault(service.name, [])
    if service.url not in services[service.name]:
        services[service.name].append(service.url)
    return {
        "status": "registered",
        "services": services
    }

@app.get("/registry/{name}")
def discover(name: str):
    return services.get(name, [])
