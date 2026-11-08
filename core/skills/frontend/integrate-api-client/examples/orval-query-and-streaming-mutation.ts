/**
 * Production TanStack Query v5 Optimistic Mutation & Streaming Client
 *
 * Implements:
 * - Centralized queryOptions factory (eliminating magic strings)
 * - Three-phase optimistic mutation lifecycle (onMutate -> onError -> onSettled)
 * - Functional updater syntax preventing stale closure captures
 * - Streaming SSE reader with AbortController cancellation
 */

import { queryOptions, QueryClient, useMutation } from '@tanstack/react-query';

export interface UserTask {
  id: string;
  title: string;
  completed: boolean;
}

// 1. Centralized queryOptions Factory
export const taskQueries = {
  all: () => ['tasks'] as const,
  list: (status: 'all' | 'pending' | 'completed') =>
    queryOptions({
      queryKey: [...taskQueries.all(), 'list', status],
      queryFn: async (): Promise<UserTask[]> => {
        const res = await fetch(`/api/v1/tasks?status=${status}`);
        if (!res.ok) throw new Error(`Fetch failed: ${res.statusText}`);
        return res.json();
      },
      staleTime: 1000 * 60 * 2,
    }),
};

// 2. Optimistic Mutation Hook Lifecycle
export function useUpdateTaskOptimistic(queryClient: QueryClient) {
  const queryKey = taskQueries.list('all').queryKey;

  return useMutation({
    mutationFn: async (updatedTask: UserTask) => {
      const res = await fetch(`/api/v1/tasks/${updatedTask.id}`, {
        method: 'PATCH',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(updatedTask),
      });
      if (!res.ok) throw new Error('Task update failed on server');
      return res.json();
    },
    // Step 1: Snapshot and Optimistically Mutate
    onMutate: async (newTask) => {
      await queryClient.cancelQueries({ queryKey });
      const previousTasks = queryClient.getQueryData<UserTask[]>(queryKey) || [];

      queryClient.setQueryData<UserTask[]>(queryKey, (old = []) =>
        old.map((t) => (t.id === newTask.id ? { ...t, ...newTask } : t))
      );

      return { previousTasks };
    },
    // Step 2: Rollback on Error
    onError: (_err, _newTask, context) => {
      if (context?.previousTasks) {
        queryClient.setQueryData(queryKey, context.previousTasks);
      }
    },
    // Step 3: Reconcile with Server
    onSettled: () => {
      queryClient.invalidateQueries({ queryKey });
    },
  });
}

// 3. Streaming AI Token Consumer with AbortSignal
export async function consumeAiStream(
  prompt: string,
  onToken: (token: string) => void,
  abortSignal: AbortSignal
): Promise<void> {
  const response = await fetch('/api/v1/ai/stream', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ prompt }),
    signal: abortSignal,
  });

  if (!response.ok || !response.body) {
    throw new Error(`Streaming failed with status: ${response.status}`);
  }

  const reader = response.body.pipeThrough(new TextDecoderStream()).getReader();

  try {
    while (true) {
      const { value, done } = await reader.read();
      if (done) break;
      if (value) {
        onToken(value);
      }
    }
  } finally {
    reader.releaseLock();
  }
}
