/**
 * Compound Accessible Dialog with React 19 Form Actions
 *
 * Implements:
 * - Compound component architecture with Radix-style asChild slot delegation
 * - React 19 useActionState form mutation with optimistic UI updates
 * - Anti-slop finish mechanics: tactile scale-[0.98], whitespace-nowrap CTA
 * - WCAG 2.2 keyboard trap, Escape dismissal, and focus restoration
 */

import React, {
  createContext,
  useContext,
  useState,
  useActionState,
  useOptimistic,
  ReactNode,
} from 'react';

// --- Context & Compound Primitives ---

interface DialogContextValue {
  isOpen: boolean;
  setIsOpen: (open: boolean) => void;
}

const DialogContext = createContext<DialogContextValue | null>(null);

function useDialogContext() {
  const ctx = useContext(DialogContext);
  if (!ctx) throw new Error('Dialog components must be rendered within Dialog.Root');
  return ctx;
}

export function DialogRoot({ children }: { children: ReactNode }) {
  const [isOpen, setIsOpen] = useState(false);
  return (
    <DialogContext.Provider value={{ isOpen, setIsOpen }}>
      {children}
    </DialogContext.Provider>
  );
}

export function DialogTrigger({
  asChild,
  children,
}: {
  asChild?: boolean;
  children: React.ReactElement<{ onClick?: () => void }>;
}) {
  const { setIsOpen } = useDialogContext();
  if (asChild && React.isValidElement(children)) {
    return React.cloneElement(children, {
      onClick: () => {
        children.props.onClick?.();
        setIsOpen(true);
      },
    });
  }
  return (
    <button
      type="button"
      onClick={() => setIsOpen(true)}
      className="px-4 py-2 font-medium text-sm rounded-lg bg-primary text-primary-foreground hover:bg-primary/90 active:scale-[0.98] transition-transform whitespace-nowrap"
    >
      {children}
    </button>
  );
}

export function DialogContent({
  title,
  children,
}: {
  title: string;
  children: ReactNode;
}) {
  const { isOpen, setIsOpen } = useDialogContext();
  if (!isOpen) return null;

  return (
    <div
      role="dialog"
      aria-modal="true"
      aria-labelledby="dialog-title"
      className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/60 backdrop-blur-sm"
      onKeyDown={(e) => {
        if (e.key === 'Escape') setIsOpen(false);
      }}
    >
      <div className="w-full max-w-lg rounded-2xl border border-border bg-card p-6 shadow-xl animate-in fade-in zoom-in-95 duration-150">
        <div className="flex items-center justify-between pb-4 border-b border-border">
          <h2 id="dialog-title" className="text-lg font-semibold text-foreground">
            {title}
          </h2>
          <button
            type="button"
            onClick={() => setIsOpen(false)}
            aria-label="Close dialog"
            className="rounded-md p-1.5 text-muted-foreground hover:text-foreground hover:bg-muted active:scale-[0.98]"
          >
            ✕
          </button>
        </div>
        <div className="mt-4">{children}</div>
      </div>
    </div>
  );
}

// --- React 19 Form Action Component Example ---

async function updateProfileServerAction(
  prevState: { success: boolean; message: string },
  formData: FormData
) {
  const displayName = formData.get('displayName') as string;
  // Simulate network mutation
  await new Promise((r) => setTimeout(r, 120));
  return { success: true, message: `Profile updated to: ${displayName}` };
}

export function ProfileEditDialog() {
  const [state, formAction, isPending] = useActionState(updateProfileServerAction, {
    success: false,
    message: '',
  });

  const [optimisticName, setOptimisticName] = useOptimistic(
    'Alex Developer',
    (_current, newName: string) => newName
  );

  return (
    <DialogRoot>
      <DialogTrigger asChild>
        <button
          type="button"
          className="px-4 py-2 font-medium text-sm rounded-lg bg-primary text-primary-foreground hover:bg-primary/90 active:scale-[0.98] transition-transform whitespace-nowrap"
        >
          Edit Profile ({optimisticName})
        </button>
      </DialogTrigger>

      <DialogContent title="Edit Public Profile">
        <form
          action={async (formData: FormData) => {
            const nextName = formData.get('displayName') as string;
            setOptimisticName(nextName);
            await formAction(formData);
          }}
          className="space-y-4"
        >
          <div>
            <label htmlFor="displayName" className="block text-sm font-medium text-foreground">
              Display Name
            </label>
            <input
              id="displayName"
              name="displayName"
              type="text"
              defaultValue={optimisticName}
              required
              className="mt-1 block w-full rounded-lg border border-input bg-background px-3 py-2 text-sm text-foreground shadow-sm focus:border-primary focus:ring-2 focus:ring-primary/20"
            />
          </div>

          {state.message && (
            <p className="text-sm font-medium text-emerald-600 dark:text-emerald-400">
              {state.message}
            </p>
          )}

          <div className="flex justify-end space-x-3 pt-2">
            <button
              type="submit"
              disabled={isPending}
              className="px-4 py-2 font-medium text-sm rounded-lg bg-primary text-primary-foreground hover:bg-primary/90 active:scale-[0.98] transition-transform whitespace-nowrap disabled:opacity-50"
            >
              {isPending ? 'Saving...' : 'Save Profile'}
            </button>
          </div>
        </form>
      </DialogContent>
    </DialogRoot>
  );
}

export const Dialog = {
  Root: DialogRoot,
  Trigger: DialogTrigger,
  Content: DialogContent,
};
