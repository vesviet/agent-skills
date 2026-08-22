---
name: develop-laravel-feature
description: Develop features in a Laravel 13 + Filament v4 + Livewire 3 monolith. Use when adding admin resources, Blade pages, Livewire components, Actions, Services, or database migrations in this stack.
---

# Develop Laravel Feature

Use this skill when building or modifying features in a Laravel 13 monolith using Filament v4 for admin, Livewire 3 for interactive components, and Blade for static rendering.

**Stack baseline (2026):** Laravel 13, Filament v4, Livewire 3, PHP 8.3+, TailwindCSS v4, Pest PHP v5.

## Core Rules

- **Thin Controller**: Controllers validate (FormRequest) and return views/responses. Business logic goes in `app/Actions/` or `app/Services/`.
- **Livewire islands only**: Use Livewire for interactive widgets (drawers, modals, dynamic forms). Static pages and listings render with pure Blade.
- **DB transactions**: Multi-table writes must use `DB::transaction()`.
- **Soft deletes**: Models referenced by foreign keys should use `SoftDeletes`.
- **FormRequest always**: Never validate inside controllers or Livewire components directly — use FormRequest or Livewire `#[Validate]` attributes.
- **Queue for I/O**: Email, notifications, and external API calls go through the queue.
- **Laravel Reverb**: Use Reverb for WebSockets — not Pusher — in new installations.
- **Laravel Pulse**: Check Pulse dashboard for slow queries, queue failures, and exceptions in dev.

## Filament v4 — Schema API (Breaking from v3)

```php
// ❌ Filament v3 (old)
use Filament\Forms\Form;
public function form(Form $form): Form
{
    return $form->schema([TextInput::make('name')]);
}

// ✅ Filament v4 (current)
use Filament\Schemas\Schema;
public function form(Schema $schema): Schema
{
    return $schema->components([TextInput::make('name')]);
    // Note: .schema() renamed to .components()
}
```

## PHP 8.4 Features (Use in New Code)

```php
// Property Hooks — replace getters/setters
class Product extends Model {
    public string $slug {
        get => Str::slug($this->name);
    }
}

// Asymmetric Visibility
class Order extends Model {
    public private(set) string $status = 'pending';
}

// New array functions
$item = array_find($items, fn($i) => $i->id === $id);
```

## Suggested Process

### 1. Identify The Layer

| Task | Layer | Location |
|------|-------|----------|
| Admin CRUD | Filament v4 Resource | `app/Filament/Resources/` |
| New public page | Controller + Blade | `app/Http/Controllers/` + `resources/views/` |
| Interactive widget | Livewire | `app/Livewire/` + `resources/views/livewire/` |
| Business logic | Action / Service | `app/Actions/` or `app/Services/` |
| Schema change | Migration | `database/migrations/` |
| Input validation | FormRequest / Rule | `app/Http/Requests/` or `app/Rules/` |

### 2. Read Existing Patterns

Before writing code, open 1–2 existing files in the same layer to match:
- Filament v4 Resource structure (`Schema::components()` — not `Form::schema()`)
- Controller response patterns (view rendering, redirects)
- Livewire event dispatching and Alpine.js integration
- Model casts, relationships, scopes, and media conversions
- Action class invocation and `DB::transaction()` usage

### 3. Implement Following Standards

- Match the established pattern — do not introduce new architectural layers without discussion.
- Use Filament v4 `Schema` API for admin features.
- Use `FormRequest` classes for all HTTP validation.
- Wrap multi-table operations in `DB::transaction()`.

### 4. Test Critical Paths

- Write Pest v5 tests for business logic in Actions/Services.
- Write Feature tests for critical HTTP flows.
- Run: `php artisan test` or `./vendor/bin/pest`.

## Checklist

- [ ] feature placed in the correct architectural layer (Action/Service/Controller/Livewire/Filament)
- [ ] thin controller pattern followed — no business logic in controllers
- [ ] Livewire used only for interactive islands, Blade for static content
- [ ] Filament v4 `Schema::components()` API used (not deprecated `Form::schema()`)
- [ ] DB::transaction() wraps any multi-table write operations
- [ ] migrations include proper indexes on slug, foreign key, and status columns
- [ ] SoftDeletes used on models referenced by foreign keys
- [ ] FormRequest used for HTTP validation
- [ ] email and notifications dispatched via queue (never synchronous)
- [ ] Pest v5 tests written for critical business logic
- [ ] Laravel Pulse checked for slow queries and queue health after significant changes

## Related Skills

- **review-code**: review changes against Laravel and project conventions
- **write-tests**: write Pest v5 tests for business logic
- **navigate-service**: understand the codebase structure before changes
- **troubleshoot-service**: debug runtime issues
- **commit-code**: commit with proper conventions
