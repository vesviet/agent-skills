# Go Microservices Conventions

This rule applies to all roles working within the `go-microservices` overlay.

## Project Structure And Architecture

- Follow Clean Architecture / Hexagonal Architecture (Ports and Adapters) patterns.
- Keep business logic isolated from transport concerns (HTTP, gRPC).
- Use dependency injection for testing and decoupling.

## Standard Libraries And Patterns

- **Dependency Management:** Use Go Modules (`go.mod`).
- **Concurrency:** Prefer channels for communication. Avoid shared state. Use `sync` package only when channels are not appropriate. 
- **Error Handling:** Check errors explicitly. Wrap errors with context using `fmt.Errorf("...: %w", err)` to maintain error chains.
- **Logging:** Use structured JSON logging (e.g., standard `log/slog`). Avoid unstructured `fmt.Print` or generic `log.Print` in production paths.

## Testing

- Use standard `testing` package.
- Favor table-driven tests for comprehensive coverage.
- Mock external dependencies at the interface boundary.

## APIs

- Use gRPC for internal service-to-service communication when performance and strict contracts are needed.
- Expose REST or GraphQL for external-facing clients and gateways.
