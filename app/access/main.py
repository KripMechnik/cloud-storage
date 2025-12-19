# app/main.py
import logging
import os
import sys

from fastapi import FastAPI
from prometheus_fastapi_instrumentator import Instrumentator
from opentelemetry import trace
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor

from app.access.access_router import access_router


def configure_logging(service_name: str) -> None:
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)

    handler = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter(
        '{"timestamp":"%(asctime)s","level":"%(levelname)s",'
        '"service":"'
        + service_name
        + '","logger":"%(name)s","message":"%(message)s"}'
    )
    handler.setFormatter(formatter)
    root_logger.handlers = [handler]


def configure_tracing(service_name: str) -> TracerProvider:
    otlp_endpoint = os.getenv("OTEL_EXPORTER_OTLP_ENDPOINT", "http://otel-collector:4318/v1/traces")

    resource = Resource.create({"service.name": service_name})
    provider = TracerProvider(resource=resource)
    processor = BatchSpanProcessor(OTLPSpanExporter(endpoint=otlp_endpoint))
    provider.add_span_processor(processor)
    trace.set_tracer_provider(provider)
    return provider


service_name = os.getenv("SERVICE_NAME", "access-service")
configure_logging(service_name)
tracer_provider = configure_tracing(service_name)

app = FastAPI()
FastAPIInstrumentor.instrument_app(app, tracer_provider=tracer_provider)
Instrumentator().instrument(app).expose(app)

app.include_router(access_router)

