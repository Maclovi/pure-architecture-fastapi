# Observability

The Cats API integrates observability tools to monitor performance, logs, and traces, ensuring robust production monitoring.

## Tools

- **Prometheus**: Metrics collection (`deploy/prometheus/prometheus.yml`).
- **Grafana**: Visualization dashboard (`deploy/grafana/dashboards/api-metrics.json`).
- **Loki**: Log aggregation (`deploy/loki/config.yaml`).
- **Tempo**: Distributed tracing (`docker-compose.stage.yaml`).
- **Vector**: Log processing (`deploy/vector/vector.toml`).

## Setup

Observability services are defined in `docker-compose.stage.yaml` and activated with the `grafana` profile:

```bash
just up
```

- **Grafana**: http://localhost/grafana (default: admin/admin).
- **Prometheus**: Exposed on port 9090 (internal).
- **Loki**: Exposed on port 3100 (internal).
- **Tempo**: Exposed on port 14250 (internal).

## Metrics

The Grafana dashboard (api-metrics.json) monitors:

- Total requests.
- Request counts by method and path.
- Average request duration.
- Exception counts.
- 2xx/5xx response percentages.
- Request latency (99th percentile).
- Requests per second.

Example Prometheus query:

```promql
sum(fastapi_requests_total{app_name="$app_name", path!="/metrics"})
```

## Logs

Loki aggregates logs from the `cats.api` container, processed by Vector. View logs in Grafana under the “Log of All FastAPI App” panel.
Example Loki query:

```loki
{container_name=~"(?s).*api"} | json | line_format "{{.message_level}} trace_id={{.message_trace_id}} {{.message_event}}"
```

## Tracing

Tempo handles distributed tracing, integrated with Loki for log correlation. Traces are accessible via Grafana’s Tempo data source.

## Configuration

Key environment variables (`.env.dist`):

- `APP_NAME`: Application name for metrics (`cats`).
- `GRPC_ENDPOINT`: Tempo endpoint (`http://cats.tempo:4317`).

See for deployment details.
