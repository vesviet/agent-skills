/**
 * Streaming RSC Page with View Transitions (Next.js 15 / React 19)
 *
 * Implements:
 * - Server Component data hoisting with React Suspense streaming
 * - Zod search parameter validation with resilient .catch() fallbacks
 * - Leaf Client Component with CSS View Transition trigger
 */

import React, { Suspense, startTransition } from 'react';
import { z } from 'zod';

// 1. Zod URL Search Parameter Schema
export const searchParamsSchema = z.object({
  tab: z.enum(['overview', 'analytics', 'audit']).catch('overview'),
  page: z.coerce.number().int().min(1).catch(1),
  q: z.string().trim().max(100).catch(''),
});

export type ValidatedSearchParams = z.infer<typeof searchParamsSchema>;

// Mock data fetcher running server-side
async function fetchMetricData(tab: string, page: number) {
  // Simulate database latency
  await new Promise((resolve) => setTimeout(resolve, 80));
  return [
    { id: '1', title: `Metric A (${tab})`, value: page * 1420 },
    { id: '2', title: `Metric B (${tab})`, value: page * 890 },
  ];
}

// 2. Client Leaf Component: View Transition Tab Navigation
export function ViewTransitionNavLeaf({ currentTab }: { currentTab: string }) {
  const tabs = ['overview', 'analytics', 'audit'];

  const handleTabChange = (nextTab: string) => {
    if (!document.startViewTransition) {
      window.location.search = `?tab=${nextTab}`;
      return;
    }

    document.startViewTransition(() => {
      startTransition(() => {
        const url = new URL(window.location.href);
        url.searchParams.set('tab', nextTab);
        window.history.pushState({}, '', url.toString());
      });
    });
  };

  return (
    <nav className="flex space-x-2 border-b border-border pb-2" aria-label="Route Tabs">
      {tabs.map((tab) => {
        const isActive = tab === currentTab;
        return (
          <button
            key={tab}
            type="button"
            onClick={() => handleTabChange(tab)}
            style={{ viewTransitionName: isActive ? 'active-tab-indicator' : undefined }}
            className={`px-4 py-2 text-sm font-medium rounded-md transition-transform active:scale-[0.98] ${
              isActive
                ? 'bg-primary text-primary-foreground shadow-sm'
                : 'text-muted-foreground hover:bg-muted hover:text-foreground'
            }`}
          >
            {tab.charAt(0).toUpperCase() + tab.slice(1)}
          </button>
        );
      })}
    </nav>
  );
}

// 3. Streaming Server Data Component
async function MetricDataList({ tab, page }: { tab: string; page: number }) {
  const metrics = await fetchMetricData(tab, page);

  return (
    <ul className="mt-4 grid gap-4 sm:grid-cols-2" role="list">
      {metrics.map((m) => (
        <li
          key={m.id}
          className="p-4 rounded-xl border border-border bg-card shadow-sm hover:border-primary/50 transition-colors"
        >
          <h3 className="text-sm font-medium text-muted-foreground">{m.title}</h3>
          <p className="mt-2 text-2xl font-bold tracking-tight text-foreground">
            {m.value.toLocaleString()}
          </p>
        </li>
      ))}
    </ul>
  );
}

// 4. Root React Server Component Page
export default async function AnalyticsRoutePage({
  searchParams,
}: {
  searchParams: Promise<Record<string, string | string[] | undefined>>;
}) {
  const rawParams = await searchParams;
  const validated = searchParamsSchema.parse({
    tab: typeof rawParams.tab === 'string' ? rawParams.tab : undefined,
    page: typeof rawParams.page === 'string' ? rawParams.page : undefined,
    q: typeof rawParams.q === 'string' ? rawParams.q : undefined,
  });

  return (
    <main className="container mx-auto px-4 py-8 min-h-[100dvh]">
      <header className="mb-6">
        <h1 className="text-3xl font-extrabold tracking-tight">System Performance Metrics</h1>
        <p className="text-muted-foreground text-sm mt-1">
          Real-time telemetry with React 19 RSC streaming and off-thread View Transitions.
        </p>
      </header>

      {/* Interactive Client Leaf */}
      <ViewTransitionNavLeaf currentTab={validated.tab} />

      {/* Streaming Asynchronous Server Component */}
      <Suspense
        fallback={
          <div className="mt-6 flex items-center justify-center p-8 text-muted-foreground">
            <span className="animate-pulse">Streaming metric data...</span>
          </div>
        }
      >
        <MetricDataList tab={validated.tab} page={validated.page} />
      </Suspense>
    </main>
  );
}
