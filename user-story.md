# User Stories 📋

## Product vision

As a customer, I want a simple Accounts service so that I can create, read, list, update, and delete account records through a reliable REST API.

## User-story template

> **As a** `<role>`, **I want** `<capability>`, **so that** `<benefit>`.

## Product backlog

### Core REST API
- **Setting up the development environment** — As a developer, I want a reproducible development environment so that I can build and test the service consistently. **[Technical Debt]**
- **Create an account** — As a user, I want to create an account so that a new customer record can be stored.
- **Read an account from the service** — As a user, I want to read an account so that I can view one customer record.
- **List all accounts in the service** — As a user, I want to list all accounts so that I can browse customer records.
- **Update an account in the service** — As a user, I want to update an account so that customer information stays current.
- **Delete an account from the service** — As a user, I want to delete an account so that obsolete records can be removed.

### Engineering and delivery
- **Need the ability to automate continuous integration checks** — As a developer, I want automated linting and tests so that every change is validated. **[Enhancement]**
- **Need to add security headers and CORS policies** — As a developer, I want security headers and CORS policies so that browser/API clients are protected. **[Enhancement]**
- **Containerize your microservice using Docker** — As a developer, I want a container image so that the service runs consistently across environments.
- **Deploy your Docker image to Kubernetes** — As a developer, I want Kubernetes deployment manifests so that the service can be orchestrated.
- **Create a CD pipeline to automate deployment to Kubernetes** — As a developer, I want a CD pipeline so that deployments are repeatable and automated.

## Sprint plan

### Sprint 1 🏃
- Setting up the development environment
- Create an account
- Read an account from the service
- List all accounts in the service
- Update an account in the service
- Delete an account from the service

### Sprint 2 🏃
- Need the ability to automate continuous integration checks
- Need to add security headers and CORS policies

### Sprint 3 🏃
- Containerize your microservice using Docker
- Deploy your Docker image to Kubernetes
- Create a CD pipeline to automate deployment to Kubernetes
