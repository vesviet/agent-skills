---
name: develop-laravel-feature
description: Develop features in a Laravel 11 + Filament v3 + Livewire 3 monolith. Use when adding admin resources, Blade pages, Livewire components, Actions, Services, or database migrations in this stack.
---

# Develop Laravel Feature

Use this skill when building or modifying features in a Laravel 11 monolith using Filament v3 for admin, Livewire 3 for interactive components, and Blade for static rendering.

## Core Rules

- **Thin Controller**: Controllers validate (FormRequest) and return views/responses. Business logic goes in `app/Actions/` or `app/Services/`.
- **Livewire islands only**: Use Livewire for interactive widgets (drawers, modals, dynamic forms). Static pages and listings render with pure Blade.
- **DB transactions**: Multi-table writes must use `DB::transaction()`.
- **Soft deletes**: Models referenced by foreign keys should use `SoftDeletes`.
- **FormRequest always**: Never validate inside controllers or Livewire components directly — use FormRequest or Livewire `#[Validate]` attributes.
- **Queue for I/O**: Email, notifications, and external API calls go through the queue.

## Suggested Process

### 1. Identify The Layer

| Task | Layer | Location |
|------|-------|----------|
| Admin CRUD | Filament Resource | `app/Filament/Resources/` |
| New public page | Controller + Blade | `app/Http/Controllers/` + `resources/views/` |
| Interactive widget | Livewire | `app/Livewire/` + `resources/views/livewire/` |
| Business logic | Action / Service | `app/Actions/` or `app/Services/` |
| Schema change | Migration | `database/migrations/` |
| Input validation | FormRequest / Rule | `app/Http/Requests/` or `app/Rules/` |

### 2. Read Existing Patterns

Before writing code, open 1–2 existing files in the same layer to match:
- Filament Resource structure (form schema, table columns, filters)
- Controller response patterns (view rendering, redirects)
- Livewire event dispatching and Alpine.js integration
- Model casts, relationships, scopes, and media conversions
- Action class invocation and DB::transaction() usage

### 3. Implement Following Standards

- Match the established pattern exactly — do not introduce new architectural layers without discussion.
- Use Filament v3 API for admin features (not custom admin pages).
- Use `FormRequest` classes for all HTTP validation.
- Wrap multi-table operations in `DB::transaction()`.

### 4. Test Critical Paths

- Write Pest or PHPUnit tests for business logic in Actions/Services.
- Write Feature tests for critical HTTP flows.
- Run: `php artisan test` or `./vendor/bin/pest`.

## Checklist

- [ ] feature placed in the correct architectural layer (Action/Service/Controller/Livewire/Filament)
- [ ] thin controller pattern followed — no business logic in controllers
- [ ] Livewire used only for interactive islands, Blade for static content
- [ ] DB::transaction() wraps any multi-table write operations
- [ ] migrations include proper indexes on slug, foreign key, and status columns
- [ ] SoftDeletes used on models referenced by foreign keys
- [ ] FormRequest used for HTTP validation
- [ ] email and notifications dispatched via queue
- [ ] Pest/PHPUnit tests written for critical business logic
- [ ] Filament Resource follows existing conventions in the project

## Related Skills

- **review-code**: review changes against Laravel and project conventions
- **write-tests**: write Pest/PHPUnit tests for business logic
- **navigate-service**: understand the codebase structure before changes
- **troubleshoot-service**: debug runtime issues
- **commit-code**: commit with proper conventions
