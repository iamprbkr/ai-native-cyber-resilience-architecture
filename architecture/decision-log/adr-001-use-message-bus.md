# ADR-001: Use Asynchronous Message Bus for Pipeline Communication

**Status**: Accepted  
**Date**: 2026-06-09  
**Author**: iamprbkr  

## Context

The platform processes alerts through multiple stages (ingestion → enrichment → scoring → correlation → AI → response). These stages must be:
- Loosely coupled for independent scaling and deployment
- Resilient to individual service failures
- Observable for metrics and debugging

## Decision

Use an asynchronous message bus (Redis Streams / Apache Kafka) as the central communication backbone.

## Consequences

### Positive
- Services can scale independently based on load
- A failure in one service does not block others (queue persists)
- Clear audit trail of all pipeline events
- Multiple consumers can subscribe to same topics (e.g., metrics service)

### Negative
- Added operational complexity (message bus cluster management)
- Eventual consistency must be handled
- Schema evolution requires coordination

## Alternatives Considered

1. **Synchronous REST/gRPC calls**: Simpler but couples services, cascading failures
2. **Shared database**: Simple but creates DB bottleneck and schema coupling
3. **Direct function calls**: Tightest coupling, not suitable for distributed deployment

## Implementation Plan

1. Define message schemas (protobuf or Avro)
2. Topic naming: `{stage}.{event_type}` pattern
3. Consumer groups for horizontal scaling
4. Dead letter queue for failed messages
