# Documento de Arquitectura  
## Sistema de Gestión de Servicios Urbanos Inteligentes – Wakanda Smart City
### Autor: Álvaro Bartolomé Montes

---

## 1. Introducción

Este documento describe la arquitectura del sistema **Wakanda Smart City**, una plataforma basada en **microservicios** diseñada para gestionar distintos servicios urbanos inteligentes como tráfico, energía, agua, residuos y seguridad.

El sistema ha sido desarrollado siguiendo una arquitectura distribuida, contenedorizada con Docker, incorporando mecanismos de **descubrimiento de servicios**, **balanceo de carga**, **resiliencia**, **monitorización** y **trazabilidad distribuida**.

---

## 2. Objetivos de la arquitectura

Los principales objetivos de la arquitectura son:

- Modularidad y desacoplamiento entre servicios
- Escalabilidad horizontal mediante réplicas
- Tolerancia a fallos y resiliencia
- Observabilidad completa del sistema
- Facilidad de despliegue local mediante `docker-compose`

---

## 3. Visión general de la arquitectura

La arquitectura sigue un patrón de **microservicios con API Gateway**, donde todas las peticiones externas entran a través de un punto único de acceso.

### Componentes principales:
- API Gateway
- Service Registry
- Microservicios independientes
- Sistema de monitorización (Prometheus + Grafana)
- Sistema de trazabilidad distribuida (OpenTelemetry + Jaeger)

---

## 4. Componentes del sistema

### 4.1 API Gateway

El **Gateway** actúa como punto de entrada único al sistema.

Funciones principales:
- Enrutamiento de peticiones hacia los microservicios
- Descubrimiento dinámico de servicios a través del registry
- Balanceo de carga entre réplicas
- Aplicación de patrones de resiliencia (timeouts, retries, circuit breaker)
- Propagación del contexto de trazas (OpenTelemetry)

Ejemplos de endpoints:
- `/traffic/status`
- `/energy/grid`
- `/water/pressure`

---

### 4.2 Service Registry

El **Service Registry** permite el descubrimiento dinámico de servicios.

Funciones:
- Registro de servicios en tiempo de arranque
- Almacenamiento de instancias activas
- Consulta de servicios por nombre

Cada microservicio se registra automáticamente indicando:
- Nombre del servicio
- URL interna (hostname Docker + puerto)

---

### 4.3 Microservicios

Cada microservicio es independiente y encapsula una funcionalidad concreta:

| Servicio   | Funcionalidad principal |
|-----------|------------------------|
| Traffic   | Gestión del tráfico urbano |
| Energy    | Estado de la red eléctrica |
| Water     | Presión y estado del agua |
| Waste     | Gestión de residuos |
| Security  | Eventos de seguridad |

Características comunes:
- API REST con FastAPI
- Métricas expuestas en `/metrics`
- Registro automático en el registry
- Instrumentación OpenTelemetry
- Contenedores Docker independientes

---

## 5. Comunicación entre componentes

- Comunicación síncrona HTTP/REST
- Resolución de nombres mediante DNS interno de Docker
- El gateway consulta al registry para localizar instancias
- Los microservicios no se comunican directamente entre sí

---

## 6. Balanceo de carga

El balanceo de carga se realiza en el **Gateway**, no en Docker.

### Funcionamiento:
1. Un servicio registra múltiples instancias
2. El gateway obtiene todas las instancias disponibles
3. Selecciona una instancia mediante **round-robin**
4. Reenvía la petición a la instancia seleccionada

Este enfoque permite:
- Escalado horizontal
- Alta disponibilidad
- Distribución de carga

---

## 7. Resiliencia y tolerancia a fallos

Se aplican patrones de resiliencia en el Gateway:

- **Timeouts** para evitar bloqueos
- **Retries** automáticos
- **Circuit Breaker** para evitar sobrecarga cuando un servicio falla
- **Fallbacks** cuando un servicio no está disponible

Esto garantiza que el sistema degrade de forma controlada.

---

## 8. Monitorización

### 8.1 Prometheus

- Recolecta métricas desde `/metrics`
- Métricas por servicio:
  - Número de peticiones
  - Estado del servicio
  - Frecuencia de llamadas

### 8.2 Grafana

- Visualización de métricas
- Dashboards por servicio
- Paneles con:
  - Peticiones por segundo
  - Comparativa entre servicios
  - Estado general del sistema

---

## 9. Trazabilidad distribuida

### OpenTelemetry + Jaeger

- Todas las peticiones están instrumentadas
- El contexto de trazas se propaga entre servicios
- Jaeger permite visualizar:
  - Flujo completo de una petición
  - Dependencias entre servicios
  - Latencias por componente

Esto facilita el diagnóstico de cuellos de botella y errores.

---

## 10. Despliegue

El sistema se despliega localmente mediante:
docker-compose up

Se levantan automáticamente:
- Gateway
- Registry
- Microservicios
- Prometheus
- Grafana
- Jaeger

No se requieren dependencias externas adicionales.

---

## 11. Pruebas

Se han implementado pruebas básicas con pytest que validan:
- Endpoints de cada microservicio
- Enrutamiento del gateway
- Respuestas HTTP correctas
Las pruebas pueden ejecutarse localmente sin necesidad de contenedores en ejecución.

---

## 12. Conclusiones

La arquitectura implementada cumple con los principios de los sistemas distribuidos modernos:
- Escalable
- Observable
- Resiliente
- Modular
El uso de tecnologías estándar como Docker, FastAPI, Prometheus, Grafana y Jaeger facilita la comprensión, el mantenimiento y la extensibilidad del sistema.
