# Restaurant Management System

A complete, production-grade **Full-Stack Restaurant Management System** built with **Python 3.11+**, **Django**, **Django REST Framework (DRF)**, and **Tailwind CSS**, mapped directly across 6 enterprise DevOps assignments.

---

## 🏛️ System Architecture & Stack

- **Backend Framework**: Python 3.11+ / Django 5+ / Django REST Framework
- **Frontend UI**: Tailwind CSS, FontAwesome, HTML5 Glassmorphism UI Templates
- **Database**: SQLite (Development) / PostgreSQL 15+ (Production Containerized)
- **Deployment & DevOps**: Docker, Docker Compose, GitHub Actions CI/CD, Kubernetes (K8s) Manifests

```
restaurant_system/
├── config/                 # Project Settings, Root URLs, WSGI/ASGI Configuration
├── accounts/               # User Roles (ADMIN, STAFF, CUSTOMER) & Auth APIs
├── tables/                 # Table Entity, Seating Capacity, Status (AVAILABLE, OCCUPIED, RESERVED)
├── menu/                   # Food Categories, Menu Items, Pricing, Stock Availability
├── orders/                 # Kitchen Orders, Line Items, Workflow Status (PENDING -> PREPARING -> SERVED -> COMPLETED)
├── billing/                # Tax Invoices, Payment Processing (CASH, CARD, UPI), Payment Status
├── templates/              # Full-Stack Responsive Tailwind Web Dashboard Views
├── static/                 # CSS & JavaScript Assets
├── devops/                 # Kubernetes Manifests, Docker Compose, CI/CD Pipeline Configuration
├── seed_data.py            # Automated Database Seeding Script
├── app.py                  # Setup Verification Script
└── manage.py               # Django Command Line Utility
```

---

## 📦 Core Business Modules

1. **`accounts`**: Custom User Model (`AbstractUser`) supporting role-based access control (`ADMIN`, `STAFF`, `CUSTOMER`).
2. **`tables`**: Seating floor plan manager tracking real-time table status (`AVAILABLE`, `OCCUPIED`, `RESERVED`) and capacity.
3. **`menu`**: Food catalog managing categories, item descriptions, price tags, and inventory stock toggles.
4. **`orders`**: Kitchen Display System (KDS) managing live order placement, item quantity updates, total calculation, and status progression.
5. **`billing`**: Tax invoice generator supporting subtotal, tax rate, discount deduction, payment settlement (`CASH`, `CARD`, `UPI`), printable invoices, and automatic table release.

---

## 🚀 Initial Setup & Execution Guide

### Prerequisites
- Python 3.11+ installed
- Git installed

### Step-by-Step Installation

1. **Clone & Navigate to Repository**:
   ```bash
   git clone <your-repository-url>
   cd restaurant_system
   ```

2. **Create & Activate Virtual Environment**:
   ```bash
   # Windows
   python -m venv venv
   venv\Scripts\activate

   # Linux / macOS
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Run Database Migrations**:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

5. **Seed Database with Demo Data**:
   ```bash
   python seed_data.py
   ```

6. **Verify Environment Setup**:
   ```bash
   python app.py
   ```

7. **Run Unit Test Suite**:
   ```bash
   python manage.py test accounts.tests tables.tests menu.tests orders.tests billing.tests
   ```

8. **Start Development Server**:
   ```bash
   python manage.py runserver
   ```
   Open **[http://127.0.0.1:8000/](http://127.0.0.1:8000/)** in your browser.
   - Admin Login: `admin` / `admin123`
   - Staff Login: `staff` / `staff123`

---

## 🛠️ DevOps Assignments Reference

- **Assignment 1**: Git Source Control, `.gitignore`, virtualenv, and base project architecture.
- **Assignment 2**: Docker & Docker Compose (`Dockerfile`, `docker-compose.yml`).
- **Assignment 3**: GitHub Actions CI/CD Pipeline (`.github/workflows/ci.yml`).
- **Assignment 4**: Production Hardening, Environment Secrets (`.env.example`), Gunicorn/Nginx.
- **Assignment 5**: Kubernetes Cluster Deployment (`devops/k8s/deployment.yaml`, `service.yaml`, `configmap.yaml`).
- **Assignment 6**: Observability & Monitoring (`devops/DEVOPS_ASSIGNMENTS_GUIDE.md`).
