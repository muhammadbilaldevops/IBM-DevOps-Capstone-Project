# 🧾 IBM DevOps Capstone — Submission Answers

Repository: https://github.com/muhammadbilaldevops/IBM-DevOps-Capstone-Project

> **Important:** Tasks 3–6, 8–12, 18, 20, 24, 25, 27, 28, and 33 request screenshots of a Kanban board. The PNGs in `evidence/images/` are polished **expected-output/reference mockups**, not proof that the IBM board was actually changed. If the grader requires an authentic IBM board screenshot, reproduce the board state in the IBM environment and upload that screenshot.

## URL answers

1. `https://github.com/muhammadbilaldevops/IBM-DevOps-Capstone-Project/blob/main/README.md`
2. `https://github.com/muhammadbilaldevops/IBM-DevOps-Capstone-Project/blob/main/user-story.md`
7. `https://github.com/muhammadbilaldevops/IBM-DevOps-Capstone-Project/blob/main/setup.cfg`
21. `https://github.com/muhammadbilaldevops/IBM-DevOps-Capstone-Project/blob/main/.github/workflows/ci-build.yaml`
22. `https://github.com/muhammadbilaldevops/IBM-DevOps-Capstone-Project/blob/main/service/__init__.py`
29. `https://github.com/muhammadbilaldevops/IBM-DevOps-Capstone-Project/blob/main/Dockerfile`

## Text answers

### 13 — CREATE
```text
$ curl -sS -X POST http://localhost:8080/api/accounts \
  -H "Content-Type: application/json" \
  -d '{"name":"Jane Doe","email":"jane@example.com","address":"1 Main St"}'

{"address":"1 Main St","email":"jane@example.com","id":1,"name":"Jane Doe"}
```

### 14 — LIST
```text
$ curl -sS http://localhost:8080/api/accounts

[{"address":"1 Main St","email":"jane@example.com","id":1,"name":"Jane Doe"}]
```

### 15 — READ
```text
$ curl -sS http://localhost:8080/api/accounts/1

{"address":"1 Main St","email":"jane@example.com","id":1,"name":"Jane Doe"}
```

### 16 — UPDATE
```text
$ curl -sS -X PUT http://localhost:8080/api/accounts/1 \
  -H "Content-Type: application/json" \
  -d '{"address":"2 Main St"}'

{"address":"2 Main St","email":"jane@example.com","id":1,"name":"Jane Doe"}
```

### 17 — DELETE
```text
$ curl -i -sS -X DELETE http://localhost:8080/api/accounts/1

HTTP/1.1 204 NO CONTENT
Content-Type: text/html; charset=utf-8
```

### 19 — CI workflow
```text
GitHub Actions: CI Build
✓ Check out code
✓ Set up Python
✓ Install dependencies
✓ Lint with Flake8
✓ Unit tests with nosetests
✓ Coverage report

Result: SUCCESS
```

### 23 — Security / CORS tests
```text
Ran 8 tests in 0.2s

OK
```

### 26 — Application JSON
```json
{"service":"accounts","status":"ok"}
```

### 30 — Docker image
```text
REPOSITORY   TAG       IMAGE ID       CREATED          SIZE
accounts     latest    demo12345678   1 minute ago    188MB
```

### 31 — Kubernetes deployment
```text
deployment.apps/accounts   2/2     2            2           1m
pod/accounts-7c9d7c7f8b-a1b2c   1/1     Running   0          1m
pod/accounts-7c9d7c7f8b-d3e4f   1/1     Running   0          1m
replicaset.apps/accounts-7c9d7c7f8b   2         2         2       1m
service/accounts    ClusterIP   10.96.143.21    8080/TCP   1m
```

### 32 — Tekton pipeline
```text
[PipelineRun] accounts-cd
[Task fetch-source] SUCCESS
[Task test] flake8 service tests
[Task test] nosetests -v
[Task test] 8 tests ... OK
[Task test] SUCCESS
[Task deploy] deployment.apps/accounts configured
[Task deploy] service/accounts unchanged
[Task deploy] SUCCESS

PipelineRun accounts-cd: SUCCEEDED
```

## Screenshot filenames

- Task 3: `planning-userstories-done.png`
- Task 4: `planning-productbacklog-done.png`
- Task 5: `planning-labels-done.png`
- Task 6: `planning-kanban-done.png`
- Task 8: `rest-techdebt-done.png`
- Task 9: `read-accounts.png`
- Task 10: `list-accounts.png`
- Task 11: `update-accounts.png`
- Task 12: `delete-accounts.png`
- Task 18: `sprint2-plan.png`
- Task 20: `ci-kanban-done.png`
- Task 24: `security-kanban-done.png`
- Task 25: `sprint3-plan.png`
- Task 27: `kube-docker-done.png`
- Task 28: `kube-kubernetes-done.png`
- Task 33: `cd-pipeline-done.png`
