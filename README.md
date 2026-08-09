# 🚀 IBM DevOps Capstone Project — Customer Accounts Microservice

[![CI Build](https://github.com/muhammadbilaldevops/IBM-DevOps-Capstone-Project/actions/workflows/ci-build.yaml/badge.svg)](https://github.com/muhammadbilaldevops/IBM-DevOps-Capstone-Project/actions/workflows/ci-build.yaml)
[![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-REST_API-black?logo=flask)](https://flask.palletsprojects.com/)
[![Docker](https://img.shields.io/badge/Docker-ready-2496ED?logo=docker)](https://www.docker.com/)
[![Kubernetes](https://img.shields.io/badge/Kubernetes-ready-326CE5?logo=kubernetes)](https://kubernetes.io/)
[![Tekton](https://img.shields.io/badge/Tekton-CD-FD495C?logo=tekton)](https://tekton.dev/)

> 🎯 A secure, tested Customer Accounts REST microservice built as the IBM DevOps Capstone Project. The repository demonstrates Agile planning, TDD, REST CRUD operations, GitHub Actions CI, security headers and CORS, Docker, Kubernetes, and Tekton continuous delivery.

## 📌 Capstone objectives

- 📝 Plan work with user stories, backlog and sprint artifacts.
- 🧪 Develop the Accounts service using test-driven development.
- 🔄 Implement Create, Read, List, Update and Delete operations.
- 📊 Maintain **95%+ test coverage** with `nosetests` and coverage.
- 🔐 Add Flask-Talisman security headers and Flask-CORS policies.
- ⚙️ Automate linting and tests with GitHub Actions.
- 🐳 Build the service as a Docker image named `accounts`.
- ☸️ Deploy the image to Kubernetes with two replicas.
- 🔁 Automate clone → lint → test → build → deploy with Tekton.

## 🧰 Technology stack

| Area | Technology |
|---|---|
| Language | Python 3.11 |
| API | Flask |
| Database | SQLite locally / PostgreSQL-compatible via `DATABASE_URI` |
| ORM | Flask-SQLAlchemy |
| Testing | `nosetests` + coverage |
| Quality | Flake8 + Pylint |
| Security | Flask-Talisman + Flask-CORS |
| CI | GitHub Actions |
| Container | Docker |
| Orchestration | Kubernetes / OpenShift |
| CD | Tekton |

## 🗂️ Repository structure

```text
.
├── .github/workflows/ci-build.yaml
├── evidence/
│   ├── images/                 # reference evidence images
│   ├── text/                   # named text evidence files
│   └── ASSIGNMENT-MAP.md
├── kubernetes/
│   ├── namespace.yaml
│   ├── deployment.yaml
│   └── service.yaml
├── scripts/
│   └── curl-demo.sh
├── service/
│   ├── __init__.py
│   ├── config.py
│   ├── models.py
│   └── routes.py
├── tekton/
│   ├── pipeline.yaml
│   ├── pipelinerun.yaml
│   ├── tasks.yaml
│   └── README.md
├── tests/
│   └── test_routes.py
├── Dockerfile
├── Procfile
├── requirements.txt
├── setup.cfg
├── SUBMISSION-ANSWERS.md
├── user-story.md
└── README.md
```

## ⚡ Run locally

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt

export FLASK_APP=service
flask run --host=0.0.0.0 --port=8080
```

Open `http://localhost:8080/`.

### Expected root response

```json
{"name":"Account REST API Service","version":"1.0"}
```

Health check:

```bash
curl -sS http://localhost:8080/health
```

```json
{"status":"OK"}
```

## 🌐 REST API

The IBM capstone convention is `/accounts`. The repository also keeps `/api/accounts` aliases for compatibility with the earlier implementation.

| Method | Endpoint | Purpose |
|---|---|---|
| `POST` | `/accounts` | Create an account |
| `GET` | `/accounts` | List all accounts |
| `GET` | `/accounts/<id>` | Read an account |
| `PUT` | `/accounts/<id>` | Update an account |
| `DELETE` | `/accounts/<id>` | Delete an account |

Example CREATE request:

```bash
curl -sS -X POST http://localhost:8080/accounts \
  -H "Content-Type: application/json" \
  -d '{"name":"Jane Doe","email":"jane@example.com","address":"1 Main St","phone_number":"555-0100","date_joined":"2025-01-15"}'
```

## 🧪 Quality gates

```bash
flake8 service tests --count --statistics
nosetests -v
coverage report -m
```

`setup.cfg` is configured with a **95% minimum coverage threshold**. The CI workflow executes checkout → dependency installation → Flake8 → `nosetests` → coverage.

## 🔐 Security

Flask-Talisman adds security headers including `X-Frame-Options`, `X-Content-Type-Options`, Content-Security-Policy and Referrer-Policy. Flask-CORS allows browser clients to call the Accounts resources.

For local development, HTTPS enforcement is disabled. To enable it:

```bash
export TALISMAN_FORCE_HTTPS=true
```

Never commit passwords, tokens, registry credentials, or other secrets.

## 🐳 Docker

Build and run:

```bash
docker build -t accounts:latest .
docker run --rm -p 8080:8080 accounts:latest
```

Verify:

```bash
curl -sS http://localhost:8080/
```

## ☸️ Kubernetes

```bash
kubectl apply -f kubernetes/namespace.yaml
kubectl apply -f kubernetes/deployment.yaml
kubectl apply -f kubernetes/service.yaml
kubectl get deployment,pods,rs,service -l app=accounts -n accounts
kubectl port-forward -n accounts service/accounts 8080:8080
```

The deployment uses two replicas and HTTP readiness/liveness probes on port `8080`.

## 🔄 Tekton CD

The CD pipeline is intentionally ordered as:

```text
clone → lint + tests → build-image → deploy
```

Apply the pipeline resources in an OpenShift/Tekton environment:

```bash
kubectl apply -f tekton/tasks.yaml
kubectl apply -f tekton/pipeline.yaml
kubectl create -f tekton/pipelinerun.yaml
```

The Buildah task must be configured with an image registry that the cluster can push to. The supplied PipelineRun uses the OpenShift `pipeline` service account convention.

## 📎 Assignment evidence

`evidence/text/` contains named, reproducible text evidence for the text questions. `evidence/images/` contains **reference/expected-output images** for the upload questions.

⚠️ **Important for grading:** the IBM assignment explicitly asks for screenshots of the learner's Kanban board. Reference images cannot truthfully prove that your IBM board was changed. For the final submission, upload authentic screenshots from your own IBM/GitHub Kanban environment showing the requested story in the requested column.

See [`SUBMISSION-ANSWERS.md`](SUBMISSION-ANSWERS.md) and [`evidence/ASSIGNMENT-MAP.md`](evidence/ASSIGNMENT-MAP.md) for the complete submission checklist.

## ❤️ Capstone status

The application code, tests, CI definition, Dockerfile, Kubernetes manifests, and Tekton definitions are maintained together so the repository can be used as a reproducible DevOps demonstration.

**Built with Python 🐍 · Flask 🌐 · Docker 🐳 · Kubernetes ☸️ · Tekton 🔁**
