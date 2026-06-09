# Deployment Guide

## Local Deployment

### Docker Compose

```bash
# 1. Build all images
make docker-build

# 2. Start services
make docker-up

# 3. Check logs
docker compose -f docker/docker-compose.yml logs -f
```

### Manual

```bash
# Start the message bus (Redis)
docker run -d -p 6379:6379 redis:7-alpine

# Run individual services
python -m src.ingestion.service
python -m src.scoring.engine
python -m src.response.engine
```

## Production Considerations

### Infrastructure Requirements

| Service | vCPU | Memory | Storage |
|---------|------|--------|---------|
| Message Bus | 2 | 4 GB | 50 GB SSD |
| Ingestion API | 2 | 2 GB | Stateless |
| Processing Services | 4 | 8 GB | Stateless |
| AI Services | 4 | 16 GB | 20 GB (model cache) |
| Metrics DB | 2 | 4 GB | 100 GB SSD |

### High Availability

- Deploy message bus as a cluster (3+ nodes)
- Stateless services behind load balancer (horizontal scaling)
- Multi-AZ deployment for cloud providers
- Database with automated failover

### Security Hardening

- Enable mTLS between all services
- Deploy in private subnets
- Use secrets manager for all credentials
- Enable audit logging to immutable storage
- Regular security patching schedule

### Monitoring

- Prometheus metrics endpoint on each service
- Grafana dashboard for real-time visibility
- Alerting on pipeline latency > 30s
- Log aggregation to ELK or Loki
