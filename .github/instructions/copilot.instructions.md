# Copilot Instructions for Frolf Bot Project

## Project Overview

This is a **multi-tenant Discord bot system** for disc golf event management built with **event-driven architecture (EDA)**, **Go microservices**, and **GitOps deployment**. The system consists of:

- **Backend Service** (`frolf-bot`): Event-driven business logic service
- **Discord Bot** (`discord-frolf-bot`): Discord interaction layer
- **Infrastructure** (`frolf-bot-infrastructure`): Kubernetes, ArgoCD, observability stack

## Architecture Principles

### Event-Driven Architecture (EDA)
- **NATS JetStream** is the event backbone for all inter-service communication
- **Watermill** framework for event routing and handling in Go
- **No direct database access** from Discord bot - all operations via events
- Events are **guild-scoped** for multi-tenancy (every event includes `guild_id`)
- **Queue groups** for environment-specific processing isolation
- Event handlers use **context propagation** for tracing and cancellation

### Multi-Tenancy
- **Guild-based isolation**: Each Discord server (guild) is a tenant
- **Service tiers**: Free and Pro tiers with different resource limits
- **GitOps scaling**: ArgoCD ApplicationSet auto-deploys guilds from config files
- **Runtime configuration**: Dynamic guild config loading without restarts
- **Namespace per guild** in Kubernetes (e.g., `guild-123456789`)

### Clean Architecture & Domain-Driven Design
- **Module structure**: Each domain (round, user, score, leaderboard, guild) is a module
- **Layered architecture**:
  - `application/`: Service layer with business logic
  - `infrastructure/`: Repositories, queue, router (external adapters)
  - `utils/`: Domain-specific utilities and validators
- **Repository pattern**: Database access abstracted behind interfaces
- **Dependency injection**: Modules receive dependencies via constructors
- **Domain types**: Strongly-typed domain models (e.g., `RoundID`, `GuildID`, `DiscordID`)

## Go Project Structure

### Backend Service (`frolf-bot`)
```
frolf-bot/
├── app/
│   ├── app.go                      # Main application initialization
│   └── modules/
│       ├── round/                   # Example module structure
│       │   ├── module.go           # Module entry point with lifecycle
│       │   ├── application/        # Service layer (business logic)
│       │   │   └── service.go
│       │   ├── infrastructure/     # External adapters
│       │   │   ├── repositories/   # Database access (Bun ORM)
│       │   │   ├── queue/          # River job queue
│       │   │   └── router/         # Watermill event routing
│       │   ├── utils/              # Domain utilities
│       │   └── mocks/              # Generated mocks (gomock)
│       ├── user/
│       ├── score/
│       ├── leaderboard/
│       └── guild/
├── config/                          # Configuration loading
├── db/bundb/                        # Database service aggregator
├── integration_tests/               # Integration test suites
│   ├── containers/                  # Testcontainers setup
│   └── modules/                     # Module-specific integration tests
├── main.go                          # Entry point with health checks
└── Makefile                         # Comprehensive test/build targets
```

### Discord Bot (`discord-frolf-bot`)
```
discord-frolf-bot/
├── app/
│   ├── bot/                         # Bot initialization
│   ├── discordgo/                   # Discord API wrapper
│   ├── guildconfig/                 # Event-driven guild config resolver
│   └── [module]/                    # Per-module Discord handlers
│       ├── discord/                 # Discord interaction handlers
│       └── watermill/               # Event subscribers
├── main.go                          # Supports 3 modes: standalone, gateway, worker
└── ARCHITECTURE.md                  # Bot-specific architecture docs
```

### Infrastructure (`frolf-bot-infrastructure`)
```
frolf-bot-infrastructure/
├── argocd-applications/             # ApplicationSets for GitOps
├── charts/                          # Helm values for dependencies
├── multi-tenant/                    # Multi-guild management
│   ├── guilds/                      # Guild config files (git-tracked)
│   └── kustomize/                   # Per-guild overlays
├── observability/                   # Grafana, Loki, Tempo, Mimir, Alloy
├── ansible/                         # Infrastructure setup playbooks
├── Tiltfile                         # Live development with hot-reload
└── Makefile                         # Onboarding, setup, dev commands
```

## Development Practices

### Testing Strategy

#### Unit Tests
- Located alongside source code (e.g., `service_test.go`)
- Use **gomock** for mocking interfaces
- Run with `make test-unit-all` or `go test ./app/... -short`
- Fast, isolated, no external dependencies

#### Integration Tests
- Located in `integration_tests/modules/[module]/`
- Use **Testcontainers** for Postgres and NATS
- Helper pattern: `testutils/` provides reusable test helpers
- Test entire event flows end-to-end
- Run with `make test-integration-all`
- Example naming: `create_round3_test.go`, `participant_status_test.go`

#### Test Helpers
- **Data generators**: `testutils/data_generator.go` for consistent test data
- **Helper patterns**: `RoundTestHelper`, `UserTestHelper` for event testing
- **Wait patterns**: `WaitForRoundCreated()`, `WaitForMessages()` with timeouts
- **Database helpers**: `CreateRoundInDB()`, `CreateUserInDB()`

#### Coverage
- Generate with `make coverage-all`
- HTML reports: `make coverage-html`
- Module-specific coverage targets available
- Coverage filtered by `cmd/coverage-filter/`

### Makefile Conventions
- **Comprehensive targets**: Migration, test, coverage, mock generation
- **Grouped targets**: Unit/integration/all test variations
- **River queue**: Separate migration targets (`river-migrate-up`, `river-clean`)
- **Summary mode**: Test targets with `-summary` suffix for CI/reporting
- **Module-specific**: Targets like `integration-round-service`

### Mock Generation
- **gomock** for generating mocks from interfaces
- Targets: `make mocks-all`, `make mocks-[module]`
- Mocks stored in `mocks/` subdirectory per module
- Regenerate after interface changes

### Database & Migrations
- **Bun ORM** for database access with pgdialect
- **Migration files**: `app/modules/[module]/infrastructure/repositories/migrations/`
- **Migration commands**: `make migrate-all`, `make rollback-all`
- **River migrations**: Separate queue table migrations
- **Auto-migrate**: `AUTO_MIGRATE=true` env var for dev mode
- **Model registration**: All models registered in `db/bundb/bundb.go`

### Event Bus Patterns
- **Publishers**: Publish events via `EventBus.Publish(topic, payload, metadata)`
- **Subscribers**: Use Watermill routers with handlers
- **Metadata**: Discord message IDs, correlation IDs in metadata map
- **Health checks**: EventBus provides health checker interface
- **Tracing**: Automatic trace propagation via middleware

### Configuration Management
- **YAML-based**: `config.yaml` for base configuration
- **Environment overrides**: Support for env var overrides
- **12-factor**: Secrets via environment variables
- **Multi-environment**: Different configs for dev/staging/prod

### Observability

#### Structured Logging
- **slog** standard library logger
- **JSON format** for production
- **Watermill adapter**: `loggerfrolfbot.ToWatermillAdapter()`
- **Context-aware**: Use `logger.InfoContext(ctx, ...)` for trace correlation

#### Distributed Tracing
- **OpenTelemetry** for tracing
- **Tempo** backend for trace storage
- **Watermill middleware**: `tracingfrolfbot.TraceHandler()` for event tracing
- **Context propagation**: Trace IDs passed through event metadata

#### Metrics
- **Prometheus** for metrics collection
- **Per-module metrics**: Each module has custom metrics registry
- **Health endpoints**: `/health` on port 8080
- **Profiling**: Optional pprof on port 6060 (`PPROF_ENABLED=true`)

#### Monitoring Stack
- **Grafana** for dashboards
- **Loki** for log aggregation
- **Mimir** for long-term metrics storage
- **Tempo** for distributed tracing
- **Alloy** for telemetry collection and routing

## Kubernetes & GitOps

### ArgoCD Patterns
- **ApplicationSets** for templating multiple apps
- **Multi-source apps**: Combine Helm charts with custom manifests
- **Self-healing**: Automated sync and drift correction
- **The Lich King**: Master ApplicationSet that manages all other AppSets

### Deployment Strategies
- **Namespace isolation**: Each guild gets own namespace
- **Resource quotas**: CPU/memory limits per tier
- **Health probes**: Liveness and readiness checks on `/health`
- **Graceful shutdown**: Signal handling for clean shutdown

### GitOps Workflow
1. Create guild config file in `multi-tenant/guilds/guild-[id].yaml`
2. Commit and push to git
3. ArgoCD ApplicationSet auto-detects and deploys
4. Per-guild namespaces, secrets, and resources created
5. Ansible for infrastructure setup, ArgoCD for app deployment

### Local Development
- **Tilt** for live development with hot-reload
- **ko** for fast container builds without Dockerfiles
- **Docker Desktop Kubernetes** or **Colima** for local cluster
- **Port forwarding**: Access services via `kubectl port-forward`
- **Local values**: Override Helm values in `local-dev/values/`

### Resource Right-Sizing
- **Requests**: Based on p95 observed usage + 20-50% headroom
- **Limits**: 2-4x requests for CPU (bursty workloads), 1.5-2x for memory
- **VPA/HPA**: Vertical/horizontal pod autoscaling support
- **Goldilocks**: Recommendations for resource requests
- **Document**: See `docs/Right-Sizing.md` for methodology

## Code Style & Conventions

### Go Idioms
- **Error wrapping**: Use `fmt.Errorf("context: %w", err)`
- **Context first**: Function signatures start with `ctx context.Context`
- **Interfaces**: Small, focused interfaces (1-5 methods)
- **Dependency injection**: Constructor functions receive dependencies
- **Table-driven tests**: Use test tables for parameterized tests

### Naming Conventions
- **Modules**: Lowercase, singular (e.g., `round`, `user`)
- **Services**: `Service` interface and `serviceImpl` struct
- **Repositories**: `[Entity]DB` interface and `[Entity]DBImpl` struct
- **Types**: Domain types in `shared/types/` (e.g., `RoundID`, `GuildID`)
- **Tests**: `Test[FunctionName]` for unit, `Test[Feature]` for integration

### File Organization
- **Interfaces**: Defined in separate files (e.g., `interface.go`)
- **Models**: Database models in `repositories/models.go`
- **Migrations**: In `repositories/migrations/[timestamp]_[description].go`
- **Helpers**: Reusable helpers in `testutils/` or `utils/`

### Comments & Documentation
- **Package comments**: Every package has a doc comment
- **Public APIs**: All exported functions/types documented
- **Complex logic**: Explain why, not what
- **TODO comments**: Include context and owner

## CI/CD

### GitHub Actions
- **ko build and push**: Builds container images with ko
- **OCI Registry**: Oracle Cloud Infrastructure Registry (OCIR)
- **Image tags**: Short commit SHA + `latest`
- **Secrets**: Registry credentials in GitHub Secrets

### Build Tools
- **ko**: Containerize Go apps without Dockerfile
- **Make**: Primary build orchestration
- **Go modules**: Dependency management with `go.mod`

## Common Patterns to Follow

### Creating a New Module
1. Create module directory: `app/modules/[module]/`
2. Add `module.go` with lifecycle methods (`Run`, `Close`)
3. Create `application/service.go` with business logic
4. Add `infrastructure/repositories/` for database
5. Add `infrastructure/router/` for event handling
6. Generate mocks: `make mocks-[module]`
7. Add integration tests in `integration_tests/modules/[module]/`

### Adding Event Handling
1. Define event payload in shared types
2. Create publisher in service layer
3. Add router configuration in `infrastructure/router/`
4. Implement handler with tracing middleware
5. Add integration test for full event flow

### Database Changes
1. Create migration file: `[timestamp]_description.go`
2. Update model in `repositories/models.go`
3. Update repository interface
4. Update repository implementation
5. Run migrations: `make migrate`
6. Update tests for new schema

### Adding Configuration
1. Update config struct in `config/config.go`
2. Add YAML example in `config.yaml`
3. Add environment variable support
4. Document in README
5. Add validation logic

## Common Gotchas

- **River migrations separate**: Run `make river-migrate-up` before app migrations
- **Context propagation**: Always pass context through event metadata
- **Guild scoping**: Every event must include `guild_id`
- **Mock regeneration**: Re-run `make mocks-all` after interface changes
- **Testcontainers cleanup**: Integration tests clean up containers automatically
- **NATS URLs**: Use environment-specific URLs (localhost for dev, service names for k8s)
- **Database DSN**: Parse from environment or config, never hardcode
- **Graceful shutdown**: Always handle context cancellation in `Run()` methods

## Security Practices

- **Secrets**: Never commit secrets, use Sealed Secrets or env vars
- **Least privilege**: Service accounts with minimal permissions
- **Network policies**: Restrict pod-to-pod communication
- **RBAC**: Role-based access control in Kubernetes
- **Environment separation**: Dev/staging/prod isolation

## Performance Considerations

- **Connection pooling**: Reuse database connections
- **Event batching**: Batch operations where possible
- **Caching**: Guild config cached in Discord bot layer
- **Resource limits**: Set appropriate CPU/memory limits
- **Autoscaling**: HPA for horizontal scaling under load

## Debugging Tips

- **pprof profiling**: Enable with `PPROF_ENABLED=true`
- **Verbose logging**: Use `-v` flag for detailed test output
- **Port forwarding**: Access services via `kubectl port-forward`
- **Event inspection**: Use NATS CLI to inspect message queues
- **Trace viewing**: Grafana Tempo for distributed traces
- **Test helpers**: Use `WaitFor` patterns for async operations

## References

- **Architecture docs**: `ARCHITECTURE.md` in each repo
- **Multi-tenant guide**: `frolf-bot-infrastructure/multi-tenant/README.md`
- **Right-sizing guide**: `frolf-bot-infrastructure/docs/Right-Sizing.md`
- **Kubernetes best practices**: `frolf-bot/KUBERNETES_BEST_PRACTICES.md` (empty - WIP)
- **Module READMEs**: Each module has specific documentation

## When Contributing

1. **Follow the module pattern**: Use existing modules as templates
2. **Write tests first**: TDD approach for new features
3. **Update mocks**: Regenerate after interface changes
4. **Run full test suite**: `make test-all-project` before committing
5. **Check coverage**: Maintain or improve coverage
6. **Update docs**: Document new features and patterns
7. **Use conventional commits**: Clear, descriptive commit messages
8. **Test locally**: Use Tilt for local validation before pushing

---

**This project follows event-driven, multi-tenant, cloud-native patterns with strong emphasis on testing, observability, and GitOps deployment.**
