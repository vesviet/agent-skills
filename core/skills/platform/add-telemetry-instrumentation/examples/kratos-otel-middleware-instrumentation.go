package telemetry

import (
	"context"
	"time"

	"github.com/go-kratos/kratos/v2/middleware"
	"github.com/go-kratos/kratos/v2/transport"
	"go.opentelemetry.io/otel"
	"go.opentelemetry.io/otel/attribute"
	"go.opentelemetry.io/otel/metric"
	"go.opentelemetry.io/otel/propagation"
	semconv "go.opentelemetry.io/otel/semconv/v1.26.0"
	"go.opentelemetry.io/otel/trace"
)

// TelemetryMiddleware creates a Kratos middleware instrumenting distributed tracing and metrics.
func TelemetryMiddleware(tracerName string, meterName string) middleware.Middleware {
	tracer := otel.GetTracerProvider().Tracer(tracerName)
	meter := otel.GetMeterProvider().Meter(meterName)

	durationHist, _ := meter.Float64Histogram(
		"http_server_duration_seconds",
		metric.WithDescription("HTTP server request latency in seconds"),
		metric.WithUnit("s"),
	)

	return func(handler middleware.Handler) middleware.Handler {
		return func(ctx context.Context, req interface{}) (interface{}, error) {
			startTime := time.Now()

			var operation string
			if tr, ok := transport.FromServerContext(ctx); ok {
				operation = tr.Operation()
				// Extract W3C TraceContext from incoming headers
				ctx = otel.GetTextMapPropagator().Extract(ctx, propagation.HeaderCarrier(tr.RequestHeader()))
			}

			// Start active OpenTelemetry span
			ctx, span := tracer.Start(
				ctx,
				operation,
				trace.WithSpanKind(trace.SpanKindServer),
				trace.WithAttributes(
					semconv.RPCSystemKey.String("kratos"),
					attribute.String("rpc.service", operation),
				),
			)
			defer span.End()

			reply, err := handler(ctx, req)

			duration := time.Since(startTime).Seconds()
			statusCode := "200"
			if err != nil {
				statusCode = "500"
				span.RecordError(err)
				span.SetAttributes(attribute.String("error.type", "internal_error"))
			}

			// Record Prometheus / OTel duration histogram
			durationHist.Record(ctx, duration, metric.WithAttributes(
				attribute.String("operation", operation),
				attribute.String("status_code", statusCode),
			))

			return reply, err
		}
	}
}

// RecordGenAiSpan adds GenAI semantic convention attributes to an active span.
func RecordGenAiSpan(ctx context.Context, model string, inputTokens, outputTokens int, ttft time.Duration) {
	span := trace.SpanFromContext(ctx)
	if !span.IsRecording() {
		return
	}

	span.SetAttributes(
		attribute.String("gen_ai.system", "openai"),
		attribute.String("gen_ai.response.model", model),
		attribute.Int("gen_ai.usage.input_tokens", inputTokens),
		attribute.Int("gen_ai.usage.output_tokens", outputTokens),
		attribute.Int("gen_ai.usage.tokens", inputTokens+outputTokens),
		attribute.Float64("gen_ai.server.time_to_first_token", ttft.Seconds()),
	)
}
