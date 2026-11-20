# Sample Target Application for DeployPilot
This is a lightweight target application for testing deployments, health checking, rollback, and container log streaming.

- **Port**: 8080
- **Endpoints**:
  - `GET /`: returns app name, version, status
  - `GET /health`: health check endpoint (returns 200 or 500 based on `APP_HEALTH_STATUS`)
