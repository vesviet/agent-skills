// Modular Behavior Tree & Utility AI in TypeScript (2026)
// Demonstrates stateless tree execution, typed blackboards, and squad tokens.

export enum NodeStatus {
  SUCCESS = 'SUCCESS',
  FAILURE = 'FAILURE',
  RUNNING = 'RUNNING',
}

export interface Blackboard {
  health: number;
  maxHealth: number;
  targetDistance: number;
  hasAttackToken: boolean;
  cooldownSeconds: number;
}

export interface BTNode {
  tick(bb: Blackboard, delta: number): NodeStatus;
}

// Composite Node: Sequence (AND)
export class SequenceNode implements BTNode {
  constructor(private children: BTNode[]) {}

  tick(bb: Blackboard, delta: number): NodeStatus {
    for (const child of this.children) {
      const status = child.tick(bb, delta);
      if (status !== NodeStatus.SUCCESS) {
        return status;
      }
    }
    return NodeStatus.SUCCESS;
  }
}

// Composite Node: Selector (OR / Fallback)
export class SelectorNode implements BTNode {
  constructor(private children: BTNode[]) {}

  tick(bb: Blackboard, delta: number): NodeStatus {
    for (const child of this.children) {
      const status = child.tick(bb, delta);
      if (status !== NodeStatus.FAILURE) {
        return status;
      }
    }
    return NodeStatus.FAILURE;
  }
}

// Condition Node: Check if in Attack Range
export class IsTargetInRangeNode implements BTNode {
  constructor(private maxRange: number) {}

  tick(bb: Blackboard): NodeStatus {
    return bb.targetDistance <= this.maxRange ? NodeStatus.SUCCESS : NodeStatus.FAILURE;
  }
}

// Utility AI Action Node: Evaluates Response Curve for Melee Attack
export class MeleeAttackAction implements BTNode {
  tick(bb: Blackboard, delta: number): NodeStatus {
    if (!bb.hasAttackToken) {
      return NodeStatus.FAILURE;
    }
    if (bb.cooldownSeconds > 0) {
      bb.cooldownSeconds = Math.max(0, bb.cooldownSeconds - delta);
      return NodeStatus.RUNNING;
    }

    // Execute attack logic
    console.log('NPC executes telegraphed melee attack strike!');
    bb.cooldownSeconds = 1.5; // Reset cooldown
    return NodeStatus.SUCCESS;
  }
}

// Squad Combat Token Coordinator (Limits simultaneous attackers)
export class SquadTokenPool {
  private availableTokens: number;

  constructor(maxSimultaneousAttackers: number = 2) {
    this.availableTokens = maxSimultaneousAttackers;
  }

  public requestToken(): boolean {
    if (this.availableTokens > 0) {
      this.availableTokens--;
      return true;
    }
    return false;
  }

  public releaseToken(): void {
    this.availableTokens++;
  }
}
