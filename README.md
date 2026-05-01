# textsummary
A full stack app that lets you summarize long texts.


## Architecture

```mermaid
sequenceDiagram
    Browser->>nginx: POST /api/jobs
    nginx->>job-service: forward request
    job-service->>RabbitMQ: publish job message
    job-service->>Browser: return job_id
    Browser->>nginx: WebSocket /ws
    nginx->>notification-service: upgrade connection
    RabbitMQ->>model-service: consume job
    model-service->>PostgreSQL: store result
    model-service->>RabbitMQ: publish completion
    RabbitMQ->>notification-service: consume completion
    notification-service->>Browser: push result via WebSocket
```