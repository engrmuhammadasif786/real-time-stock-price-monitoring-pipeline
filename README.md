### Introduction

This project involves building a stock price monitoring pipeline using Kafka for data ingestion, Spark for data transformation and MongoDB for data storage. An interactive Flask-based web dashboard with Plotly visualisations showed stock trends and volume containerized in Docker.

![Architecture Diagram](https://github.com/user-attachments/assets/45dbe4bf-fc5e-4eac-ae30-596f50763cc0)

### Building and running application

When you're ready, start application by running:
`docker compose up --build`.

Application will be available at http://localhost:5002.

### Deploying application to the cloud

First, build your image, e.g.: `docker build -t myapp .`.
If your cloud uses a different CPU architecture than your development
machine (e.g., you are on a Mac M1 and your cloud provider is amd64),
you'll want to build the image for that platform, e.g.:
`docker build --platform=linux/amd64 -t myapp .`.

Then, push it to your registry, e.g. `docker push myregistry.com/myapp`.

Consult Docker's [getting started](https://docs.docker.com/go/get-started-sharing/)
docs for more detail on building and pushing.

### References
* [Docker's Python guide](https://docs.docker.com/language/python/)
