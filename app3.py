from random import randint
from flask import Flask
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
#otlp_exporter = OTLPSpanExporter(endpoint="http://172.17.0.2:4317", insecure=True)

otlp_exporter = OTLPSpanExporter(endpoint="http://my-opentelemetry-collector:4317", insecure=True)
# Set up a batch span processor with the exporter
span_processor = BatchSpanProcessor(otlp_exporter)

# Add the span processor to the tracer provider
trace.get_tracer_provider().add_span_processor(span_processor)

# Acquire a tracer
#tracer = trace.get_tracer("diceroller.tracer")

app = Flask(__name__)

@app.route("/rolldice")
def roll_dice():
    return str(roll())

def roll():
    # This creates a new span that's the child of the current one
    with tracer.start_as_current_span("roll") as rollspan:
        res = randint(1, 6)
        rollspan.set_attribute("roll.value", res)
        return res


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')

