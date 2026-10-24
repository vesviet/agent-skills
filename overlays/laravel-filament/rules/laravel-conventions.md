# Laravel Conventions — Filament v4 + Livewire Stack

Portable Laravel coding standards for projects using Filament v4 admin and Livewire 3 interactive components. These extend `core/rules/code.md`.

**Stack baseline (2026):** Laravel 13, Filament v4, Livewire 3, PHP 8.3+, TailwindCSS v4, Pest PHP v5.
⚠️ Laravel 12 bug fix support ended Aug 13, 2026 — migrate to Laravel 13.

## Architecture (Thin Controller Pattern)

- Controllers only validate (`FormRequest`) and return responses.
- Business logic belongs in `app/Actions/` (single-action classes) or `app/Services/`.
- Livewire components handle interactive islands only (drawers, modals, dynamic forms).
- Static pages and listings render with pure Blade — no Livewire overhead on read-only views.
- Never put business logic in Livewire component classes — delegate to Actions/Services.

## Database Integrity

- Multi-table writes MUST be wrapped in `DB::transaction()`.
- Use `SoftDeletes` trait on models referenced by foreign keys.
- Migrations MUST index columns used in WHERE/ORDER: slugs, foreign keys, status fields.
- Use enum casts on models for status columns — never store as raw strings.
- Always define `$fillable` or `$guarded` explicitly on every model.

## Filament v4 Admin (2026 — Breaking Changes from v3)

**Unified `Schema` API** — the biggest v4 breaking change:

```php
// ❌ Filament v3 pattern
use Filament\Forms\Form;
public function form(Form $form): Form
{
    return $form->schema([
        TextInput::make('name'),
    ]);
}

// ✅ Filament v4 pattern
use Filament\Schemas\Schema;
public function form(Schema $schema): Schema
{
    return $schema->components([    // .schema() renamed to .components()
        TextInput::make('name'),
    ]);
}
```

Other v4 changes:
- Resources: `app/Filament/Resources/` — structure unchanged
- Resource naming: `{Model}Resource.php` with pages in `{Model}Resource/Pages/`
- **MFA**: built-in (no plugin needed) — enable via `Filament::auth()->mfa()->enabled()`
- **Custom data sources**: Filament v4 supports any data source, not Eloquent-only
- **Table rendering**: 2–3× faster with partial re-renders on action modals
- **New components**: TipTap rich editor, slider, code editor, table repeater
- **Client-side methods**: `hiddenJs()`, `afterStateUpdatedJs()` — reduces server round-trips
- Status fields: `SelectColumn` in tables for inline editing
- Navigation: `NavigationGroup` for logical grouping

## Livewire 3 + Alpine.js

- Livewire for server-side state (cart contents, form submission, real-time data).
- Alpine.js for client-side UI state (toggle visibility, transitions, animations).
- Dispatch browser events from Livewire for cross-component communication.
- Debounce text inputs: `wire:model.live.debounce.300ms` — never bare `wire:model.live`.
- Use `#[Computed]` for derived properties instead of recalculating in render.

## Laravel 13 Features

```php
// Laravel AI SDK (stable in L13) — provider-agnostic
use Illuminate\Support\Facades\AI;
$response = AI::text('Summarize this product description: ' . $product->description);

// PHP Attributes for framework components
#[Table('products')]
#[Fillable('name', 'slug', 'price')]
class Product extends Model { }

// JSON:API Resources built-in
use Illuminate\Http\Resources\Json\JsonApiResource;
```

## PHP 8.4 Features (Use in New Code)

```php
// Property Hooks — computed properties without accessors
class Product extends Model {
    public string $excerpt {
        get => Str::limit($this->description, 150);
    }
}

// Asymmetric Visibility — read-public, write-private
class Order extends Model {
    public private(set) string $orderNumber;
}

// New array functions
$item = array_find($items, fn($i) => $i->status === 'pending');
$hasActive = array_any($items, fn($i) => $i->is_active);
```

## Media Handling (Spatie)

- Use `spatie/laravel-medialibrary` for file uploads.
- Define media conversions on the model (WebP, responsive sizes).
- Standard conversions: `addMediaConversion('thumb')`, `addMediaConversion('preview')`.
- Use `SpatieMediaLibraryFileUpload` in Filament forms.

## Validation

- Always use `FormRequest` classes for HTTP requests.
- Livewire validation: `#[Validate]` attributes or `$rules` property.
- Shared rules: `app/Rules/` as custom Rule objects.

## WebSockets (Laravel Reverb — 2026 Standard)

```bash
# Install Reverb (replaces Pusher/Soketi)
php artisan install:broadcasting --reverb
```

- Self-hosted on ReactPHP — no external API round-trips.
- Horizontal scaling via Redis pub/sub.
- Monitored via Laravel Pulse (`ReverbConnections` recorder).
- Never use Pusher in new projects when hosting infrastructure allows Reverb.

## Monitoring (Laravel Pulse — Standard in L13)

- Ships with Laravel — zero-config for basic metrics.
- Monitors: queues, slow queries, exceptions, HTTP requests, Reverb connections.
- `php artisan pulse:work` in Supervisor alongside queue workers.

## Routing

- Resourceful route naming: `{resource}.index`, `{resource}.show`, `{resource}.store`.
- Group routes: `Route::prefix()` + `Route::name()`.
- Route model binding with `{slug}` for public-facing URLs.

## Queue & Email

- Never send email synchronously — dispatch via queue.
- `ShouldQueue` on all Mailables and Notifications.
- Log failed jobs; configure retry backoff.
- Use Reverb + queue for real-time notifications.

## Testing (Pest PHP v5)

```php
// Pest v5 — current standard
test('user can create a product', function () {
    $user = User::factory()->admin()->create();
    $response = actingAs($user)->post('/api/products', [
        'name' => 'New Product',
        'price' => 99.99,
    ]);
    $response->assertCreated();
    assertDatabaseHas('products', ['name' => 'New Product']);
});

// AI-based Evals (Pest v5 — grade LLM responses)
test('AI summary is relevant', function () {
    $summary = AI::text('Summarize: ' . $product->description);
    expect($summary)->toBeRelevantTo($product->description);
})->evals();
```

- Tests: `tests/Feature/` (HTTP flows) + `tests/Unit/` (Actions/Services).
- `RefreshDatabase` trait in feature tests.
- Run: `php artisan test` or `./vendor/bin/pest`.
- Minimum coverage: payments, calculations, state transitions.

## Project Structure Convention

```
app/
├── Actions/            ← Single-action classes (invokable)
├── Services/           ← Stateful service classes
├── Filament/Resources/ ← Admin CRUD resources (Filament v4 Schema API)
├── Http/
│   ├── Controllers/    ← Thin controllers (validate + return only)
│   └── Requests/       ← FormRequest validation
├── Livewire/           ← Interactive island components
├── Models/             ← Eloquent models (PHP 8.4 property hooks)
├── Rules/              ← Custom validation rules
└── Providers/
```

## Standard 2026 Alignment

This overlay rule file is part of the agent-skills engineering pack. The 2026
upgrade pass added the following Standard 2026 alignment footer to every
overlay rule file in the pack.

- **OWASP ASI**: applied as described in the core pack — see
  `core/roles/role-standard.md` (ASI01-ASI10) and the per-skill
  `## Security Guardrails (OWASP ASI)` section in each skill. The rules in this
  file are applied by the role that owns the affected action; the runtime
  gate is `core/scripts/hooks/check-policy.py` with
  `core/policies/action-boundaries.yaml`.
- **Failure Modes** (overlay-specific): the rules in this file can be violated
  by drift, missing context, or untracked exceptions. The owning role is
  expected to surface concrete failure scenarios in the workflow's
  `### Failure Modes` section and to capture remediations via
  `contracts/schemas/incident-report.json` when the rule is bypassed.
- **Output Contracts**: when a rule in this file produces a structured
  artifact (brief, plan, config, content handoff, audit event), the artifact
  must conform to the corresponding schema in `core/contracts/schemas/`.
  See `See `core/skills/backend/scaffold-new-service/SKILL.md` and the `implementation-result.json` schema.` for the related skill output contract reference.
- **Skill Toolbox Lock**: a rule in this file is enforced by the role whose
  Skill Toolbox lists the related skill as Primary. Roles that hold the
  skill as Supporting must delegate rather than execute directly (per
  `core/workflows/README.md`).
- **Commit / publish gate**: rule changes that affect user-visible behavior
  must follow the META-RULE in `core/rules/code.md` — no commit, no push,
  no publish without explicit user confirmation.

See `core/skills/backend/scaffold-new-service/SKILL.md` and the `implementation-result.json` schema.

Last updated: 2026-09-01
