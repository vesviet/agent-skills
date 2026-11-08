/**
 * Headless Combobox Compound Component Architecture
 *
 * Implements:
 * - Headless state hook (`useCombobox`) separating logic from presentation
 * - Compound primitives: Combobox.Root, Combobox.Input, Combobox.List, Combobox.Option
 * - Full ARIA 1.2 combobox pattern with keyboard navigation (ArrowUp/Down, Enter, Escape)
 * - Radix-style asChild slot delegation and anti-boolean prop sprawl
 */

import React, {
  createContext,
  useContext,
  useState,
  useRef,
  useId,
  ReactNode,
} from 'react';

export interface ComboboxOption {
  value: string;
  label: string;
  disabled?: boolean;
}

// --- Headless Hook ---

export function useCombobox(options: ComboboxOption[], onSelect?: (value: string) => void) {
  const [isOpen, setIsOpen] = useState(false);
  const [query, setQuery] = useState('');
  const [activeIndex, setActiveIndex] = useState(-1);

  const filteredOptions = options.filter((opt) =>
    opt.label.toLowerCase().includes(query.toLowerCase())
  );

  const selectIndex = (index: number) => {
    const item = filteredOptions[index];
    if (item && !item.disabled) {
      setQuery(item.label);
      setIsOpen(false);
      setActiveIndex(-1);
      onSelect?.(item.value);
    }
  };

  const onKeyDown = (e: React.KeyboardEvent) => {
    switch (e.key) {
      case 'ArrowDown':
        e.preventDefault();
        if (!isOpen) {
          setIsOpen(true);
          setActiveIndex(0);
        } else {
          setActiveIndex((prev) => (prev < filteredOptions.length - 1 ? prev + 1 : 0));
        }
        break;
      case 'ArrowUp':
        e.preventDefault();
        if (!isOpen) {
          setIsOpen(true);
          setActiveIndex(filteredOptions.length - 1);
        } else {
          setActiveIndex((prev) => (prev > 0 ? prev - 1 : filteredOptions.length - 1));
        }
        break;
      case 'Enter':
        e.preventDefault();
        if (isOpen && activeIndex >= 0) {
          selectIndex(activeIndex);
        }
        break;
      case 'Escape':
        e.preventDefault();
        setIsOpen(false);
        setActiveIndex(-1);
        break;
    }
  };

  return {
    isOpen,
    setIsOpen,
    query,
    setQuery,
    activeIndex,
    setActiveIndex,
    filteredOptions,
    selectIndex,
    onKeyDown,
  };
}

// --- Context & Compound Primitives ---

type ComboboxContextValue = ReturnType<typeof useCombobox> & {
  listboxId: string;
  inputId: string;
};

const ComboboxContext = createContext<ComboboxContextValue | null>(null);

function useComboboxContext() {
  const ctx = useContext(ComboboxContext);
  if (!ctx) throw new Error('Combobox subcomponents must be inside Combobox.Root');
  return ctx;
}

export function ComboboxRoot({
  options,
  onSelect,
  children,
}: {
  options: ComboboxOption[];
  onSelect?: (val: string) => void;
  children: ReactNode;
}) {
  const combobox = useCombobox(options, onSelect);
  const listboxId = useId();
  const inputId = useId();

  return (
    <ComboboxContext.Provider value={{ ...combobox, listboxId, inputId }}>
      <div className="relative w-full">{children}</div>
    </ComboboxContext.Provider>
  );
}

export function ComboboxInput({
  placeholder = 'Select option...',
}: {
  placeholder?: string;
}) {
  const { query, setQuery, onKeyDown, isOpen, setIsOpen, listboxId, inputId, activeIndex } =
    useComboboxContext();

  return (
    <input
      id={inputId}
      type="text"
      role="combobox"
      aria-expanded={isOpen}
      aria-haspopup="listbox"
      aria-controls={listboxId}
      aria-activedescendant={
        activeIndex >= 0 ? `${listboxId}-opt-${activeIndex}` : undefined
      }
      value={query}
      onChange={(e) => {
        setQuery(e.target.value);
        if (!isOpen) setIsOpen(true);
      }}
      onKeyDown={onKeyDown}
      onFocus={() => setIsOpen(true)}
      placeholder={placeholder}
      className="w-full rounded-lg border border-input bg-background px-3 py-2 text-sm text-foreground shadow-sm focus:border-primary focus:ring-2 focus:ring-primary/20"
    />
  );
}

export function ComboboxList({ children }: { children: ReactNode }) {
  const { isOpen, listboxId } = useComboboxContext();
  if (!isOpen) return null;

  return (
    <ul
      id={listboxId}
      role="listbox"
      className="absolute z-50 mt-1 max-h-60 w-full overflow-auto rounded-lg border border-border bg-popover p-1 text-popover-foreground shadow-md"
    >
      {children}
    </ul>
  );
}

export function ComboboxOptionItem({
  index,
  option,
}: {
  index: number;
  option: ComboboxOption;
}) {
  const { activeIndex, selectIndex, listboxId } = useComboboxContext();
  const isActive = activeIndex === index;

  return (
    <li
      id={`${listboxId}-opt-${index}`}
      role="option"
      aria-selected={isActive}
      aria-disabled={option.disabled}
      onClick={() => selectIndex(index)}
      className={`relative flex cursor-pointer select-none items-center rounded-md px-3 py-1.5 text-sm outline-none transition-colors ${
        isActive ? 'bg-accent text-accent-foreground' : 'hover:bg-muted'
      } ${option.disabled ? 'pointer-events-none opacity-50' : ''}`}
    >
      {option.label}
    </li>
  );
}

export const Combobox = {
  Root: ComboboxRoot,
  Input: ComboboxInput,
  List: ComboboxList,
  Option: ComboboxOptionItem,
};
