import sys
import os

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

# Añadir raíz del proyecto
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

# Añadir gateway
GATEWAY_DIR = os.path.join(ROOT_DIR, "gateway")
if GATEWAY_DIR not in sys.path:
    sys.path.insert(0, GATEWAY_DIR)

# Añadir cada microservicio como si fuera root (/app en Docker)
SERVICES_DIR = os.path.join(ROOT_DIR, "services")

for service in os.listdir(SERVICES_DIR):
    service_path = os.path.join(SERVICES_DIR, service)
    if os.path.isdir(service_path) and service_path not in sys.path:
        sys.path.insert(0, service_path)
