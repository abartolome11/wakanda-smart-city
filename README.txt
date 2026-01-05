Wakanda Smart City – Arquitectura de Microservicios
Autor: Álvaro Bartolomé Montes

Este proyecto implementa una arquitectura de microservicios en Python para la gestión de servicios urbanos inteligentes en Wakanda (tráfico, energía, agua, residuos y seguridad).

La solución está basada en FastAPI, Docker, Prometheus, Grafana y Jaeger, e incluye descubrimiento de servicios, balanceo de carga, resiliencia y observabilidad completa.

-------------------------------------------------------------------------------------------------------------------

Arquitectura general

La arquitectura sigue un modelo de microservicios desacoplados, compuesta por:

- API Gateway: punto de entrada único para los clientes.
- Service Registry: registro y descubrimiento dinámico de servicios.
- Microservicios:
  - Traffic
  - Energy
  - Water
  - Waste
  - Security
- Observabilidad:
  - Prometheus (métricas)
  - Grafana (dashboards)
  - Jaeger (trazabilidad distribuida)

Cada microservicio se registra automáticamente en el registry al arrancar.

-------------------------------------------------------------------------------------------------------------------

Endpoints principales

API Gateway (puerto 8080)

Endpoint            Descripción
/traffic/status	    Estado del tráfico
/energy/grid	    Estado de la red eléctrica
/water/pressure	    Presión del agua
/waste/containers	Estado de contenedores
/security/events	Eventos de seguridad

Ejemplo:
    curl http://localhost:8080/traffic/status

-------------------------------------------------------------------------------------------------------------------

Construir y lanzar contenedores
    
docker compose down -v
docker compose build --no-cache
docker compose up

Alternativamente, para replicación de un microservicio:
docker compose up --scale <microservicio>=2

-------------------------------------------------------------------------------------------------------------------

Balanceo entre réplicas

El API Gateway hace balanceo a nivel de cliente.

Comando para levantar 2 instancias del mismo microservicio: 
    docker compose up --scale traffic=2

Para comprobar que funciona, añadir a la salida del microservicio replicado:
    return {
    "intersection_id": "I-12",
    "instance": socket.gethostname()
}

Al probar varias veces el comando:
    curl http://localhost:8080/traffic/status

Devolverá 
    {"intersection_id":"I-12","instance":"fb5139f21709"}
    {"intersection_id":"I-12","instance":"158d5b209add"}

Demostrando así que existe balanceo entre réplicas.

-------------------------------------------------------------------------------------------------------------------

Fallo de un servicio

El gateway incluye mecanismos de resiliencia:
- Timeouts
- Retries
- Circuit Breaker
- Si un servicio no responde:
    - El circuit breaker se abre.
    - Se devuelve una respuesta de fallback.
    - Se evita saturar servicios caídos.

Para simularlo (codigo en services/traffic/app.py):
import random

@app.get("/traffic/status")
def traffic_status():
    REQUESTS.inc()

    if random.random() < 0.4:
        raise Exception("Simulated traffic service failure")

    return {
        "intersection_id": "I-12",
        "vehicle_count": random.randint(100, 400),
        "average_speed_kmh": 25.0,
        "signal_phase": "NS_GREEN"
    }

Si entonces hacemos en otra terminal (por ejemplo): 
curl http://localhost:8080/traffic/status

Tendremos la salida:
{
  "status": "fallback",
  "message": "Service temporarily unavailable"
}

-------------------------------------------------------------------------------------------------------------------

Monitorización con Prometheus y Grafana

- Prometheus
    Recolecta métricas de todos los microservicios (/metrics).

Acceso:
    http://localhost:9090


- Grafana
    Dashboards con métricas de:
        Número de peticiones
        Estado de servicios
        Carga por microservicio

Acceso:
    http://localhost:3000


Credenciales por defecto:
    usuario: admin
    contraseña: admin

-------------------------------------------------------------------------------------------------------------------

Trazabilidad distribuida con Jaeger

El proyecto utiliza OpenTelemetry para generar trazas distribuidas.

- Cada petición atraviesa:
    Gateway
    Registry
    Microservicio
- Las trazas permiten ver el flujo completo de la solicitud.

Acceso a Jaeger:
    http://localhost:16686

-------------------------------------------------------------------------------------------------------------------

Test

Ejecutar con pytest
Para que funcione se necesita instalar las dependencias en local:
Comando: pip install fastapi pytest httpx prometheus_client requests tenacity opentelemetry-api opentelemetry-sdk opentelemetry-exporter-otlp opentelemetry-instrumentation-fastapi

-------------------------------------------------------------------------------------------------------------------
