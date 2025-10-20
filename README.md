# Monolithic and Microservices Architectures: A Practical Case Study

**Repository for Bachelor Thesis by Clemens Marx**

This repository contains all code, setup and architecture diagrams related to my bachelor thesis, which evaluates **monolithic and microservices architecture styles** through a custom-developed public transportation application. The application implements core functionalities including route calculation, disruption reporting, and arrival time information.  

Both architectures were containerized and deployed on Google Cloud using **Google Kubernetes Engine**. The microservices version decomposes the monolith into independent services, with special focus on the routing component as a compute-heavy bottleneck.  

Performance and scalability were evaluated using **load tests with Locust**, collecting metrics such as response time, throughput, CPU/memory usage, bandwidth, and cloud costs. The results show that monolithic architectures perform well under low load, while microservices scale better under higher demand, at the cost of slightly higher complexity and operational overhead.

## Repository Contents

- `diagrams_architecture/` - Architecture diagrams in PDF
- `locust/` - Locust load testing files
- `microservice_architecture/` - Microservices implementation with multiple Django services
- `microservice_kubernetes/` - Microservices deployment on Kubernetes (local and GKE)
- `monolith_kubernetes/` - Monolithic deployment on Kubernetes (as single Pod for good comparability)
- `monolithic_architecture/` - Monolithic application implementation
- `monolithic_cloudrun/` - Monolithic deployment on Google Cloud Run (for experimentation; not included in the final thesis)

## Architecture Diagrams

### Monolithic Architecture
[Monolithic Architecture](diagrams_architecture/application_monolithic.pdf)

### Microservices Architecture
[Microservices Architecture](diagrams_architecture/microservice_component2.pdf)
