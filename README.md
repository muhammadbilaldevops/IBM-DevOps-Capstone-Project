# 🚀 IBM DevOps Capstone Project — Accounts Microservice

[![CI Build](https://github.com/muhammadbilaldevops/IBM-DevOps-Capstone-Project/actions/workflows/ci-build.yaml/badge.svg)](https://github.com/muhammadbilaldevops/IBM-DevOps-Capstone-Project/actions/workflows/ci-build.yaml)
[![Python](https://img.shields.io/badge/Python-3.11%2B-blue?logo=python)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-REST_API-black?logo=flask)](https://flask.palletsprojects.com/)
[![Docker](https://img.shields.io/badge/Docker-ready-2496ED?logo=docker)](https://www.docker.com/)
[![Kubernetes](https://img.shields.io/badge/Kubernetes-ready-326CE5?logo=kubernetes)](https://kubernetes.io/)

> A production-style Flask Accounts REST API built for the IBM DevOps Capstone assignment, with automated testing, linting, security headers, Docker packaging, Kubernetes manifests, and a Tekton CD pipeline.

## ✨ What is included?

| Area | Implementation |
|---|---|
| REST API | Create, Read, List, Update, Delete accounts |
| Persistence | SQLite via Flask-SQLAlchemy |
| Testing | `pytest` + `nosetests` + coverage |
| Quality | Flake8 + Pylint configuration |
| Security | Flask-Talisman security headers + Flask-CORS |
| CI | GitHub Actions workflow in `.github/workflows/ci-build.yaml` |
| Container | Hardened Python 3.11 Docker image |
| Kubernetes | Deployment, Service, probes, 2 replicas |
| CD | Tekton Pipeline + PipelineRun |
| Assignment evidence | `evidence/` contains expected-output references for every upload/text task |

## 🗂️ Project structure

```text
.
├── .github/workflows/ci-build.yaml
├── evidence/
│   ├── images/
│   └── text/
├── kubernetes/
│   ├── deployment.yaml
│   ├── namespace.yaml
│   └── service.yaml
├── scripts/curl-demo.sh
├── service/
│   ├── __init__.py
│   ├── config.py
│   ├── models.py
│   └── routes.py
├── tekton/
│   ├── pipeline.yaml
│   ├── pipelinerun.yaml
│   └── README.md
├── tests/test_routes.py
├── Dockerfile
├── Procfile
├── requirements.txt
├── setup.cfg
├── user-story.md
└── README.md
```

## ⚡ Quick start

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

export FLASK_APP=service
flask run --host=0.0.0.0 --port=8080
```

Then open `http://localhost:8080/`.

### REST endpoints

| Method | Endpoint | Purpose |
|---|---|---|
| `POST` | `/api/accounts` | Create an account |
| `GET` | `/api/accounts` | List all accounts |
| `GET` | `/api/accounts/<id>` | Read one account |
| `PUT` | `/api/accounts/<id>` | Update an account |
| `DELETE` | `/api/accounts/<id>` | Delete an account |

Example:

```bash
curl -X POST http://localhost:8080/api/accounts \
  -H "Content-Type: application/json" \
  -d '{"name":"Jane Doe","email":"jane@example.com","address":"1 Main St"}'
```

## 🧪 Quality checks

```bash
flake8 service tests
nosetests -v
coverage report
pylint service
```

The CI workflow runs checkout → Python setup → dependency installation → Flake8 → nosetests → coverage.

## 🐳 Docker

```bash
docker build -t accounts:latest .
docker run --rm -p 8080:8080 accounts:latest
```

## ☸️ Kubernetes

```bash
kubectl apply -f kubernetes/namespace.yaml
kubectl apply -f kubernetes/deployment.yaml
kubectl apply -f kubernetes/service.yaml

kubectl get deployments,pods,rs,services -l app=accounts -n accounts
```

For Minikube:

```bash
minikube image load accounts:latest
kubectl apply -f kubernetes/deployment.yaml
kubectl port-forward -n accounts service/accounts 8080:8080
```

## 🔐 Security

`service/__init__.py` enables CORS for `/api/*` and configures Flask-Talisman security headers. HTTPS enforcement is disabled by default for local development and can be enabled with:

```bash
export TALISMAN_FORCE_HTTPS=true
```

Do **not** commit credentials or production secrets.

## 🔄 Tekton CD

```bash
kubectl apply -f tekton/pipeline.yaml
kubectl create -f tekton/pipelinerun.yaml
```

The sample pipeline clones the source, runs linting/tests first, and deploys Kubernetes manifests only after the test task succeeds.

## 📸 Assignment evidence

The `evidence/` directory contains **reference/expected-output images and text captures**, generated from this implementation. They are useful for preparing the IBM assignment submission. For grading, replace board-style reference images with your own screenshots from the actual IBM/Kanban environment if the grader requires authentic UI screenshots.

See [`evidence/ASSIGNMENT-MAP.md`](evidence/ASSIGNMENT-MAP.md) for a task-by-task checklist.

## 📝 Assignment checklist

- [x] README with project name and CI badge
- [x] `user-story.md` user-story template
- [x] `setup.cfg` for nosetests, coverage, Flake8, and Pylint
- [x] CRUD REST endpoints
- [x] Security headers and CORS
- [x] GitHub Actions CI
- [x] Dockerfile
- [x] Kubernetes deployment and service
- [x] Tekton pipeline definitions
- [x] Expected cURL/test/Kubernetes/Tekton outputs
- [x] PNG evidence references for all upload tasks

## 📚 Notes

This repository is intentionally self-contained and uses a lightweight SQLite database for local development. Kubernetes and Tekton require a compatible cluster with the corresponding tooling installed.

**Built with ❤️ for the IBM DevOps Capstone learning project.**
