# Laravel Filament Overlay

Generic, reusable conventions for any Laravel 13+ project using Filament v4 admin, Livewire 3 interactive islands, and Blade static rendering. Stack-specific, project-agnostic.

## Tech Stack (2026)

- **Framework:** Laravel **13** (released Mar 17, 2026; PHP 8.3+ required)
  - ⚠️ Laravel 12 bug fix support **ended Aug 13, 2026** — migrate now
- **Admin:** Filament PHP **v4** (released Aug 12, 2025 — unified `Schema` API, breaking changes)
- **Frontend:** Blade + Livewire **3** + Alpine.js + TailwindCSS **v4**
- **Database:** PostgreSQL / MySQL
- **Media:** Spatie Media Library (optional)
- **Testing:** Pest PHP **v5** (v5 = current; adds AI-based Evals testing)
- **PHP:** 8.3+ (8.4 recommended — Property Hooks, Asymmetric Visibility)
- **WebSockets:** Laravel Reverb (self-hosted, replaces Pusher/Soketi)
- **Monitoring:** Laravel Pulse (zero-config, ships with Laravel 13)

## ⚠️ 2026 Critical Changes

### Filament v4 — Breaking Schema API
```php
// ❌ Filament v3
public function form(Form $form): Form
{
    return $form->schema([...]);
}

// ✅ Filament v4 — unified Schema API
public function form(Schema $schema): Schema
{
    return $schema->components([...]);  // .schema() renamed to .components()
}
```

New in v4: TipTap rich editor, slider, code editor, table repeater, MFA built-in,
custom data sources (not Eloquent-only), deep nested resources, 2–3× faster table rendering.

### Laravel 13 New Features
- **Laravel AI SDK** (stable) — `use Illuminate\Support\Facades\AI;`
- **PHP Attributes** for framework components: `#[Table]`, `#[Fillable]`
- **JSON:API Resources** built-in
- `PreventRequestForgery` middleware (CSRF via `Sec-Fetch-Site` header)

### PHP 8.4 Features (Use in New Code)
```php
// Property Hooks
class Product {
    public string $slug {
        get => Str::slug($this->name);
        set => $this->name = $value;
    }
}

// Asymmetric Visibility
class Order {
    public private(set) string $status = 'pending';
}

// New array functions
$found = array_find($items, fn($i) => $i->id === $id);
```

## Included

- `rules/laravel-conventions.md` — Architecture, DB integrity, Filament v4, Livewire 3, testing standards
- `skills/develop-laravel-feature/` — Generic skill for building features in this stack

Compose with global core and optionally with a project-specific overlay.
