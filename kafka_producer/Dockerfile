FROM python:3.8-slim

# Set the working directory in the container
WORKDIR /producer

# Copy the producer script to the container
COPY . /producer

# Install Kafka and requests dependencies
RUN pip install kafka-python requests

# Run the Kafka producer script
CMD ["python", "producer.py"]
