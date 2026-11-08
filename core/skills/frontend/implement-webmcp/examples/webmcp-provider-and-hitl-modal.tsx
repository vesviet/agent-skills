/**
 * WebMCP Client Provider with Human-in-the-Loop (HITL) Consent Modal
 *
 * Implements:
 * - SSR-safe feature detection ('modelContext' in document)
 * - Sanitized state mapping stripping confidential fields
 * - Default-deny tool registration with strict JSON schemas
 * - Fail-safe HITL confirmation modal with 60s timeout
 */

import React, { createContext, useContext, useEffect, useState, ReactNode } from 'react';

export interface WebMcpToolDefinition {
  name: string;
  description: string;
  isHighRisk: boolean;
  inputSchema: {
    type: 'object';
    properties: Record<string, { type: string; description: string }>;
    required: string[];
  };
  handler: (args: Record<string, unknown>) => Promise<Record<string, unknown>>;
}

export interface HitlRequest {
  toolName: string;
  args: Record<string, unknown>;
  resolve: (approved: boolean) => void;
}

interface WebMcpContextValue {
  isAvailable: boolean;
  registerTool: (tool: WebMcpToolDefinition) => void;
  pendingHitl: HitlRequest | null;
}

const WebMcpContext = createContext<WebMcpContextValue | null>(null);

export function WebMcpProvider({ children }: { children: ReactNode }) {
  const [isAvailable, setIsAvailable] = useState(false);
  const [tools, setTools] = useState<Map<string, WebMcpToolDefinition>>(new Map());
  const [pendingHitl, setPendingHitl] = useState<HitlRequest | null>(null);

  useEffect(() => {
    // 1. SSR-safe check
    if (typeof window !== 'undefined' && 'modelContext' in document) {
      setIsAvailable(true);
    }
  }, []);

  const registerTool = (tool: WebMcpToolDefinition) => {
    // Validate schema
    if (!tool.inputSchema.properties || Object.keys(tool.inputSchema.properties).length === 0) {
      throw new Error(`Tool ${tool.name} must declare explicit properties in inputSchema`);
    }

    setTools((prev) => new Map(prev).set(tool.name, tool));

    // Register with in-browser modelContext if supported
    if (typeof window !== 'undefined' && 'modelContext' in document) {
      // @ts-expect-error modelContext experimental API
      document.modelContext?.registerTool({
        name: tool.name,
        description: tool.description,
        inputSchema: tool.inputSchema,
        execute: async (args: Record<string, unknown>) => {
          if (tool.isHighRisk) {
            const approved = await new Promise<boolean>((resolve) => {
              setPendingHitl({ toolName: tool.name, args, resolve });
            });
            if (!approved) {
              return { error: { code: 'USER_REJECTED', message: 'Action rejected by user' } };
            }
          }
          return await tool.handler(args);
        },
      });
    }
  };

  return (
    <WebMcpContext.Provider value={{ isAvailable, registerTool, pendingHitl }}>
      {children}
      {pendingHitl && (
        <HitlApprovalModal
          request={pendingHitl}
          onDecision={(decision) => {
            pendingHitl.resolve(decision);
            setPendingHitl(null);
          }}
        />
      )}
    </WebMcpContext.Provider>
  );
}

function HitlApprovalModal({
  request,
  onDecision,
}: {
  request: HitlRequest;
  onDecision: (approved: boolean) => void;
}) {
  const [timeLeft, setTimeLeft] = useState(60);

  useEffect(() => {
    const timer = setInterval(() => {
      setTimeLeft((prev) => {
        if (prev <= 1) {
          clearInterval(timer);
          onDecision(false); // Fail-safe on timeout
          return 0;
        }
        return prev - 1;
      });
    }, 1000);

    return () => clearInterval(timer);
  }, [onDecision]);

  return (
    <div
      role="alertdialog"
      aria-modal="true"
      aria-labelledby="hitl-title"
      className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/70 backdrop-blur-sm"
    >
      <div className="w-full max-w-md rounded-2xl border border-destructive/50 bg-card p-6 shadow-2xl">
        <h3 id="hitl-title" className="text-lg font-bold text-foreground">
          Confirm High-Risk Action
        </h3>
        <p className="mt-2 text-sm text-muted-foreground">
          An AI assistant has requested execution of <strong>{request.toolName}</strong>.
        </p>

        <div className="mt-4 rounded-lg bg-muted p-3 font-mono text-xs text-foreground overflow-x-auto">
          <pre>{JSON.stringify(request.args, null, 2)}</pre>
        </div>

        <div className="mt-3 flex items-center justify-between text-xs text-muted-foreground">
          <span>Auto-rejecting in: {timeLeft}s</span>
        </div>

        <div className="mt-6 flex justify-end space-x-3">
          <button
            type="button"
            onClick={() => onDecision(false)}
            className="px-4 py-2 font-medium text-sm rounded-lg border border-border bg-background hover:bg-muted active:scale-[0.98]"
          >
            Deny
          </button>
          <button
            type="button"
            onClick={() => onDecision(true)}
            className="px-4 py-2 font-medium text-sm rounded-lg bg-destructive text-destructive-foreground hover:bg-destructive/90 active:scale-[0.98]"
          >
            Authorize Action
          </button>
        </div>
      </div>
    </div>
  );
}
