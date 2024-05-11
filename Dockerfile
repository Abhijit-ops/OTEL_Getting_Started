# Use the official Python image as a base image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
#COPY app.py /app
COPY app3.py /app

# Install dependencies
RUN pip install --no-cache-dir flask opentelemetry-instrumentation-flask opentelemetry-sdk opentelemetry-exporter-otlp
# Set the environment variable for OpenTelemetry auto-instrumentation
ENV OTEL_PYTHON_LOGGING_AUTO_INSTRUMENTATION_ENABLED=true

EXPOSE 5000
# Run the OpenTelemetry instrumentation and Flask application


# working 
CMD ["python", "app3.py"]  
  
