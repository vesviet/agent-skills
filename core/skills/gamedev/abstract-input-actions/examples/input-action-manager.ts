// Input Action Manager & Scaled Radial Deadzone in TypeScript (2026)

export interface Vector2 {
  x: number;
  y: number;
}

export interface ActionState {
  pressed: boolean;
  value: number | Vector2;
}

export type InputContext = 'Gameplay' | 'UI' | 'Dialogue';

export class InputActionManager {
  private activeContext: InputContext = 'Gameplay';
  private deadzoneMin = 0.15;
  private deadzoneMax = 0.95;
  private actions: Map<string, ActionState> = new Map();

  constructor() {
    this.registerAction('Jump', { pressed: false, value: 0 });
    this.registerAction('Move', { pressed: false, value: { x: 0, y: 0 } });
    this.registerAction('Confirm', { pressed: false, value: 0 });
  }

  public registerAction(name: string, initial: ActionState) {
    this.actions.set(name, initial);
  }

  public setContext(context: InputContext) {
    this.activeContext = context;
  }

  // Scaled Radial Deadzone filtering for analog thumbsticks
  public filterRadialDeadzone(rawX: number, rawY: number): Vector2 {
    const magnitude = Math.sqrt(rawX * rawX + rawY * rawY);
    if (magnitude <= this.deadzoneMin) {
      return { x: 0, y: 0 };
    }

    const normalizedX = rawX / magnitude;
    const normalizedY = rawY / magnitude;

    if (magnitude >= this.deadzoneMax) {
      return { x: normalizedX, y: normalizedY };
    }

    const scaledMag = (magnitude - this.deadzoneMin) / (this.deadzoneMax - this.deadzoneMin);
    return {
      x: normalizedX * scaledMag,
      y: normalizedY * scaledMag,
    };
  }

  public updateAnalogStick(rawX: number, rawY: number) {
    if (this.activeContext !== 'Gameplay') {
      return;
    }
    const filtered = this.filterRadialDeadzone(rawX, rawY);
    const action = this.actions.get('Move');
    if (action) {
      action.pressed = filtered.x !== 0 || filtered.y !== 0;
      action.value = filtered;
    }
  }

  public getAction(name: string): ActionState | undefined {
    return this.actions.get(name);
  }

  public handleControllerDisconnect() {
    console.warn('Primary controller disconnected! Triggering pause safeguard.');
    // Reset all pressed states
    this.actions.forEach((act) => {
      act.pressed = false;
      if (typeof act.value === 'object') {
        act.value = { x: 0, y: 0 };
      } else {
        act.value = 0;
      }
    });
    this.setContext('UI');
  }
}
