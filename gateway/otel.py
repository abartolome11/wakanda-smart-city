import os
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.resources import Resource
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor

def setup_tracing(app, service_name: str):
    resource = Resource.create({"service.name": service_name})

    trace.set_tracer_provider(TracerProvider(resource=resource))

    exporter = OTLPSpanExporter(
        endpoint=os.getenv("OTEL_EXPORTER_OTLP_ENDPOINT", "http://jaeger:4317"),
        insecure=True,
    )

    trace.get_tracer_provider().add_span_processor(
        BatchSpanProcessor(exporter)
    )

    FastAPIInstrumentor.instrument_app(app)
