# Go Microservices Overlay

This overlay defines language-level and architecture-level conventions for Go (Golang) microservices. 
It bridges the gap between the portable core skills and the specific implementation details of a Go backend.

## Conventions

- **Dependency Management:** Go Modules (`go.mod`).
- **Architecture:** Clean Architecture / Hexagonal Architecture (Ports and Adapters).
- **Concurrency:** Idiomatic use of goroutines and channels, avoiding shared memory.
- **Testing:** Standard `testing` package, favoring table-driven tests.
- **Logging:** Structured JSON logging (e.g., standard `log/slog`).
- **Error Handling:** Explicit error checking and propagation; wrapping errors with context using `fmt.Errorf("%w")`.
- **API:** gRPC for internal service-to-service communication, REST/GraphQL for external gateways.
