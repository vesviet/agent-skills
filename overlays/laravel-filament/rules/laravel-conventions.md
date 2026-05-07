# Laravel Conventions — Filament + Livewire Stack

Portable Laravel coding standards for projects using Filament v3 admin and Livewire 3 interactive components. These extend `core/rules/code.md`.

## Architecture (Thin Controller Pattern)

- Controllers only validate (`FormRequest`) and return responses.
- Business logic belongs in `app/Actions/` (single-action classes) or `app/Services/`.
- Livewire components handle interactive islands only (drawers, modals, dynamic forms).
- Static pages and listings render with pure Blade — no Livewire overhead on read-only views.
- Never put business logic in Livewire component classes — delegate to Actions/Services.

## Database Integrity

- Multi-table writes MUST be wrapped in `DB::transaction()`.
- Use `SoftDeletes` trait on models referenced by foreign keys to prevent cascading data loss.
- Migrations MUST index columns used in WHERE/ORDER: slugs, foreign keys, status fields, unique identifiers.
- Use enum casts on models for status columns — never store as raw strings.
- Always define `$fillable` or `$guarded` explicitly on every model.

## Filament v3 Admin

- Resources live in `app/Filament/Resources/`.
- Resource naming: `{Model}Resource.php` with pages in `{Model}Resource/Pages/`.
- Use Filament's built-in form components; prefer `SpatieMediaLibraryFileUpload` when using Spatie.
- Status fields use `SelectColumn` in tables for inline editing.
- Use Filament's `NavigationGroup` for logical grouping.
- Keep Resource forms and tables self-contained — do not scatter logic across multiple files.

## Livewire 3 + Alpine.js

- Livewire for server-side state (cart contents, form submission, real-time data).
- Alpine.js for client-side UI state (toggle visibility, transitions, animations).
- Dispatch browser events from Livewire for cross-component communication.
- Debounce user input with `wire:model.live.debounce.300ms` — never use `wire:model.live` without debounce on text fields.
- Use `#[Computed]` for derived properties instead of recalculating in render.

## Media Handling (Spatie)

- Use `spatie/laravel-medialibrary` for file uploads when available.
- Define media conversions on the model (WebP, responsive sizes).
- Store originals on disk, serve optimized versions.
- Use `addMediaConversion('thumb')` and `addMediaConversion('preview')` as standard sizes.

## Validation

- Always use `FormRequest` classes for HTTP requests — never validate in controllers.
- Livewire validation uses `#[Validate]` attributes or `$rules` property — keep rules on the component, delegate logic to Actions.
- Shared validation rules go in `app/Rules/` as custom Rule objects.

## Routing

- Use resourceful route naming: `{resource}.index`, `{resource}.show`, `{resource}.store`.
- Group routes by concern with `Route::prefix()` and `Route::name()`.
- Use route model binding with `{slug}` for public-facing URLs.

## Queue & Email

- Never send email synchronously — always dispatch via queue.
- Use `ShouldQueue` interface on all Mailables and Notifications.
- Log failed jobs and configure retry backoff.

## Testing (Pest PHP)

- Tests live in `tests/Feature/` and `tests/Unit/`.
- Feature tests for HTTP flows (routes, forms, checkout).
- Unit tests for Actions and Services (business logic).
- Use `RefreshDatabase` trait in feature tests.
- Run with `php artisan test` or `./vendor/bin/pest`.
- Minimum coverage: critical business logic paths (payments, calculations, state transitions).

## Project Structure Convention

```
app/
├── Actions/            ← Single-action classes (invokable)
├── Services/           ← Stateful service classes
├── Filament/Resources/ ← Admin CRUD resources
├── Http/
│   ├── Controllers/    ← Thin controllers
│   └── Requests/       ← FormRequest validation
├── Livewire/           ← Interactive island components
├── Models/             ← Eloquent models
├── Rules/              ← Custom validation rules
└── Providers/
```
