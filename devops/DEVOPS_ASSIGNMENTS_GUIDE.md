# DevOps Assignments Mapping Guide - Restaurant Management System

This document maps the **Restaurant Management System** codebase directly across 6 standard DevOps assignments for academic and enterprise submission.

---

## Assignment 1: Source Control, Framework Setup & Modular Architecture
- **Goal**: Establish standard repository structure, virtualenv management, dependency tracking (`requirements.txt`), and custom Django app architecture.
- **Implemented Artifacts**:
  - Apps created: `accounts`, `tables`, `menu`, `orders`, `billing`
  - Custom User model (`accounts/models.py`) with roles (`ADMIN`, `STAFF`, `CUSTOMER`)
  - Modular `config/settings.py` supporting dev/prod environment flags.

---

## Assignment 2: Containerization & Microservices Orchestration (Docker)
- **Goal**: Package Django application into a multi-stage, secure Docker image and orchestrate web & database services using Docker Compose.
- **Implemented Artifacts**:
  - `Dockerfile`: Multi-stage build (`python:3.11-slim`) optimizing image size and layer caching.
  - `docker-compose.yml`: Services for `web` (Django + Gunicorn) and `db` (PostgreSQL 15-alpine) with health checks.

---

## Assignment 3: Continuous Integration & Test Automation (CI/CD)
- **Goal**: Automate unit testing, code linting, coverage reports, and database migrations on every commit.
- **Implemented Artifacts**:
  - `.github/workflows/ci.yml`: GitHub Actions pipeline with a live PostgreSQL service container running `pytest --cov=.`.
  - Comprehensive unit test suites in `accounts/tests.py`, `tables/tests.py`, `menu/tests.py`, `orders/tests.py`, and `billing/tests.py`.

---

## Assignment 4: Production Hardening, Environment Security & Reverse Proxy
- **Goal**: Configure production environment variables, WSGI server (Gunicorn), and security best practices.
- **Implemented Artifacts**:
  - Production WSGI configuration in `config/wsgi.py`
  - `.env.example` template for secrets isolation
  - Security header middlewares enabled in `config/settings.py`.

---

## Assignment 5: Cloud-Native Deployment & Kubernetes Orchestration
- **Goal**: Deploy containerized application to Kubernetes (Minikube / EKS / GKE) with high availability and load balancing.
- **Implemented Artifacts**:
  - `devops/k8s/deployment.yaml`: 3-replica deployment with CPU/Memory resource limits, readiness, and liveness probes.
  - `devops/k8s/service.yaml`: LoadBalancer Service routing traffic to port 8000.
  - `devops/k8s/configmap.yaml`: ConfigMap managing environment variables.

---

## Assignment 6: Observability, Monitoring & Logging
- **Goal**: Implement system observability, health checks, and log collection.
- **Implemented Artifacts**:
  - Django health check endpoints (`/accounts/login/` probe target)
  - Custom logging configuration in `config/settings.py` capturing database queries and HTTP errors.
