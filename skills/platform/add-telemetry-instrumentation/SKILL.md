# Add Telemetry Instrumentation

Add observability (logging, metrics, tracing) to a service or feature to ensure operational visibility.

## Context

Cloud-native and distributed systems require deep visibility. When adding new features or bootstrapping services, explicit telemetry must be added.

## Steps

1. **Identify Critical Paths**: Determine the key boundaries, entry points, and failure domains of the feature.
2. **Structured Logging**: Add structured JSON logging with relevant correlation IDs (e.g., trace IDs, request IDs) for significant state changes, warnings, or errors.
3. **Metrics**: Add relevant metrics (e.g., counters for requests, histograms for latency) for business-critical events and system performance.
4. **Distributed Tracing**: Instrument spans across service boundaries, external API calls, or database queries.
5. **Security Check**: Verify that no sensitive PII, tokens, or credentials are leaked in the telemetry data.
