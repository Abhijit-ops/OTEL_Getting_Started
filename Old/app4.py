from random import randint
from opentelemetry import trace
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor

# Define a resource with service name
resource = Resource(attributes={"service.name": "my-service"})

# Set up tracer provider with the specified resource
trace.set_tracer_provider(TracerProvider(resource=resource))
tracer = trace.get_tracer(__name__)

# Create an OTLP exporter
otlp_exporter = OTLPSpanExporter(endpoint="http://172.17.0.2:4317", insecure=True)
#http://172.17.0.2:4318/v1/traces
# Set up a batch span processor with the exporter
span_processor = BatchSpanProcessor(otlp_exporter)

# Add the span processor to the tracer provider
trace.get_tracer_provider().add_span_processor(span_processor)

# Function to simulate a task and create a span
def simulate_task():
    with tracer.start_as_current_span("task"):
        # Simulate some work
        result = randint(1, 100)
        print(f"Task result: {result}")

# Main function to generate traces
def main():
    for i in range(5):
        simulate_task()

if __name__ == "__main__":
    main()
